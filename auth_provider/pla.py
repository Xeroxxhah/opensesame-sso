import secrets
from .models import PasswordLessAuthModel
import hashlib
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


class PasswordLessAuth:


    def __init__(self):
        pass
    

    def generate_pla_code(self, user):
        # Generate a 6-digit code
        self.__code = f"{secrets.randbelow(10)}{secrets.randbelow(10)}{secrets.randbelow(10)}{secrets.randbelow(10)}{secrets.randbelow(10)}{secrets.randbelow(10)}"
        hashed_code = hashlib.sha256(self.__code.encode()).hexdigest()

        # Delete existing code if present (OneToOne relationship)
        PasswordLessAuthModel.objects.filter(user=user).delete()

        # Create new code
        PasswordLessAuthModel.objects.create(
            user=user,
            hashed_code=hashed_code,
        )

        return {
            "user": user.email,
            "code": self.__code
        }
    
    def send_otp_email(self, user, otp_code):
    
        context = {
            'user': user,
            'otp_code': otp_code,
            'expiry_minutes': settings.PLA_CODE_EXP,
            'company_name': settings.COMP_CONF['name'],
            'website_url': settings.COMP_CONF['website'],
            'support_url': settings.COMP_CONF['website'],
            'privacy_url': settings.COMP_CONF['website'],
        }
        
        html_content = render_to_string('email/otp_email.html', context)
        
        email = EmailMessage(
            subject=f'Your Verification Code: {otp_code}',
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        
        email.content_subtype = 'html'
        email.send(fail_silently=False)

    
    def pla_authenticate(self, user, code):
        try:
            pla_obj = PasswordLessAuthModel.objects.get(user=user)

            if pla_obj and not pla_obj.is_used:

                if timezone.now() >= pla_obj.expired_at or pla_obj.attempts >= settings.PLA_MAX_ATTEMPTS:
                    return False
                else:
                    hashed_code = hashlib.sha256(code.encode()).hexdigest()

                    if pla_obj.hashed_code == hashed_code:
                        pla_obj.is_used = True
                        pla_obj.save()
                        return True
                    else:
                        pla_obj.attempts += 1
                        pla_obj.save()

            return False

        except PasswordLessAuthModel.DoesNotExist:
            return False





    
    



