import jwt
from django.contrib.auth import get_user_model
from .models import ServiceProvider
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import datetime, timedelta
import uuid

class ServiceIDEmpty(Exception):
    def __init__(self, msg='Service ID is empty or None'):
        self.msg = msg
        super().__init__(self.msg)

class ServiceNotFound(Exception):
    def __init__(self, msg='Service not found'):
        self.msg = msg
        super().__init__(self.msg)

ACCESS_TOKEN = 'access'
REFRESH_TOKEN = 'refresh'


class CustomJWTBackend:


    def __init__(self, secret=None, algorithm='HS256'):
        self.__secret = secret
        self.algorithm = algorithm


    def _serialize_payload(self, payload):
        if isinstance(payload, dict):
            return {key: self._serialize_payload(value) for key, value in payload.items()}
        elif isinstance(payload, list):
            return [self._serialize_payload(item) for item in payload]
        elif isinstance(payload, uuid.UUID):
            return str(payload)
        return payload


    def get_requested_claims_from_user(self, user, service_id):
        requested_claims = {}
        service = get_object_or_404(ServiceProvider, service_id=service_id)
        claims_required = service.claims_required

        for key in claims_required.keys():
            if hasattr(user, key):
                value = getattr(user, key)
                if isinstance(value, uuid.UUID):
                    value = str(value)
                requested_claims.update({key: value})

        return requested_claims


    def get_token_pair(self, user, service_id=None, custom_claims=None):
        now = datetime.utcnow()

        if not service_id:
            raise ServiceIDEmpty()
        
        service_id = str(service_id)

        try:
            service = ServiceProvider.objects.get(service_id=service_id)
        except ServiceProvider.DoesNotExist:
            raise ServiceNotFound()

        self.__secret = service.service_secret

        base_payload = self.get_requested_claims_from_user(user, service_id)

        if custom_claims:
            base_payload.update(custom_claims)
        
        base_payload.update({
            'service_id': str(service_id),
            'iat': now,
            'exp': now + timedelta(minutes=settings.ACCESS_JWT_TIMEOUT or 1440)
        })

        access_payload = base_payload.copy()
        access_payload.update({
            'token_type': ACCESS_TOKEN, 
            'service_id': str(service_id), 
            'exp': now + timedelta(minutes=settings.ACCESS_JWT_TIMEOUT or 1440)
        })
        
        refresh_payload = base_payload.copy()
        refresh_payload.update({
            'token_type': REFRESH_TOKEN, 
            'service_id': str(service_id), 
            'exp': now + timedelta(minutes=settings.REFRESH_JWT_TIMEOUT or 2880)
        })
        
        access_payload = self._serialize_payload(access_payload)
        refresh_payload = self._serialize_payload(refresh_payload)

        access_token = jwt.encode(access_payload, self.__secret, self.algorithm)
        refresh_token = jwt.encode(refresh_payload, self.__secret, self.algorithm)

        del service

        return access_token, refresh_token


    def verify_token(self, token, secret, token_type=ACCESS_TOKEN):
        try:
            payload = jwt.decode(token, secret, algorithms=[self.algorithm])
            
            if payload.get('token_type') != token_type:
                return None
            
            return payload

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


    def get_service_secret(self, service_id):
        service = get_object_or_404(ServiceProvider, service_id=service_id)
        return service.service_secret


    def refresh_access_token(self, refresh_token, secret, service_id):
        try:
            now = datetime.utcnow()

            payload = self.verify_token(refresh_token, secret, token_type=REFRESH_TOKEN)
            
            if not payload:
                return None, None

            User = get_user_model()

            try:
                user = User.objects.get(email=payload.get('email'))
            except User.DoesNotExist:
                return None, None

            claims = self.get_requested_claims_from_user(user=user, service_id=service_id)

            access_payload = claims.copy()

            access_payload.update({
                'token_type': 'access', 
                'service_id': str(service_id),
                'exp': now + timedelta(minutes=settings.ACCESS_JWT_TIMEOUT or 1440)
            })
            
            refresh_payload = claims.copy()
            
            refresh_payload.update({
                'token_type': 'refresh', 
                'service_id': str(service_id),
                'exp': now + timedelta(minutes=settings.REFRESH_JWT_TIMEOUT or 2880)
            })

            access_payload = self._serialize_payload(access_payload)
            refresh_payload = self._serialize_payload(refresh_payload)

            access_token = jwt.encode(access_payload, self.__secret, self.algorithm)
            new_refresh_token = jwt.encode(refresh_payload, self.__secret, self.algorithm)

            return access_token, new_refresh_token
            
        except Exception:
            return None, None