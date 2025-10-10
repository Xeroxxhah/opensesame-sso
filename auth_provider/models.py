from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from uuid import uuid4
import pyAesCrypt
from io import BytesIO
import secrets
from django.conf import settings
from datetime import timedelta


class CustomUserModel(AbstractUser):
    user_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)    
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=15, blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=15, blank=True, null=True)
    is_mfa_enabled = models.BooleanField(default=False)
    is_pla_enabled = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class ServiceProvider(models.Model):
    service_id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    service_name = models.CharField(max_length=120, blank=False, null=False)
    claims_required = models.JSONField(default=dict)
    redirect_url = models.URLField(blank=False, null=False)
    _service_secret = models.BinaryField()

    def __str__(self):
        return f'{self.service_name} - {self.service_id}'


    @property
    def service_secret(self):
        if not self._service_secret:
            return None
            
        encrypted_key = BytesIO(self._service_secret)
        decrypted_key = BytesIO()

        try:
            pyAesCrypt.decryptStream(encrypted_key, decrypted_key, settings.ENCRYPTION_KEY, 64 * 1024)
            return decrypted_key.getvalue().decode()
        except ValueError:
            return None        


    @service_secret.setter
    def service_secret(self, val):
        if val:
            plain_text = BytesIO(val.encode())
            encrypted_out = BytesIO()
            pyAesCrypt.encryptStream(plain_text, encrypted_out, settings.ENCRYPTION_KEY, 64 * 1024)
            self._service_secret = encrypted_out.getvalue()


    def save(self, *args, **kwargs):  
        if not self._service_secret:
            self.service_secret = secrets.token_urlsafe(90)
        super().save(*args, **kwargs)


class ServiceProviderUser(models.Model):
    serviceprovider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    granted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.serviceprovider} - {self.user}'
    
    class Meta:
        unique_together = ['serviceprovider', 'user']


class PasswordLessAuthModel(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    hashed_code = models.CharField(max_length=150)
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=settings.PLA_CODE_EXP or 5)
        super().save(*args, **kwargs)

