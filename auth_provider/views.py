from django.contrib.auth import authenticate, login
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .custom_jwt_backend import CustomJWTBackend
from .models import ServiceProvider, ServiceProviderUser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from django.conf import settings
import uuid
import logging
import traceback
import json

logger = logging.getLogger(__name__)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Authentication - Redirecting</title>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        
        .redirect-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
            width: 90%;
            position: relative;
            overflow: hidden;
        }}
        
        .redirect-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
            background-size: 200% 100%;
            animation: gradient-shift 3s ease-in-out infinite;
        }}
        
        @keyframes gradient-shift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .security-icon {{
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .security-icon svg {{
            width: 40px;
            height: 40px;
            fill: white;
        }}
        
        h1 {{
            color: #2d3748;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        p {{
            color: #718096;
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 2rem;
        }}
        
        .loading-spinner {{
            width: 40px;
            height: 40px;
            margin: 1rem auto;
            border: 3px solid #e2e8f0;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .security-badges {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .badge {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 0.25rem 0.75rem;
            font-size: 0.75rem;
            color: #4a5568;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .badge-icon {{
            width: 12px;
            height: 12px;
            fill: #48bb78;
        }}
        
        .manual-continue {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }}
        
        .manual-continue:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }}
        
        .manual-continue:active {{
            transform: translateY(0);
        }}
        
        @media (max-width: 480px) {{
            .redirect-container {{
                padding: 2rem;
                margin: 1rem;
            }}
            
            .security-badges {{
                flex-direction: column;
                gap: 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="redirect-container">
        <div class="security-icon">
            <svg viewBox="0 0 24 24">
                <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,7C13.4,7 14.8,8.6 14.8,10.1V11.1C15.4,11.4 16,12 16,12.8V16.2C16,17.1 15.1,18 14.2,18H9.8C8.9,18 8,17.1 8,16.2V12.8C8,12 8.4,11.4 9,11.1V10.1C9,8.6 10.6,7 12,7M12,8.2C11.2,8.2 10.2,9.2 10.2,10.1V11.1H13.8V10.1C13.8,9.2 12.8,8.2 12,8.2Z"/>
            </svg>
        </div>
        
        <h1>Secure Authentication</h1>
        <p>You are being securely redirected to your requested service. Your authentication tokens are being transmitted using industry-standard security protocols.</p>
        
        <div class="loading-spinner"></div>
        
        <form id="tokenForm" method="POST" action="{service_url}" style="display: none;" referrerpolicy="no-referrer">
            <input type="hidden" name="tokens" value="{json_payload}">
            <input type="hidden" name="content_type" value="application/json">
        </form>
        
        <noscript>
            <p style="color: #e53e3e; margin: 1rem 0;">JavaScript is required for automatic redirection.</p>
            <button type="button" class="manual-continue" onclick="document.getElementById('tokenForm').submit();">
                Continue Manually
            </button>
        </noscript>
        
        <div class="security-badges">
            <div class="badge">
                <svg class="badge-icon" viewBox="0 0 24 24">
                    <path d="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z"/>
                </svg>
                JWT Secured
            </div>
            <div class="badge">
                <svg class="badge-icon" viewBox="0 0 24 24">
                    <path d="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z"/>
                </svg>
                Encrypted
            </div>
            <div class="badge">
                <svg class="badge-icon" viewBox="0 0 24 24">
                    <path d="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z"/>
                </svg>
                Time-Limited
            </div>
        </div>
    </div>
    
    <script>
        // Enhanced security measures
        (function() {{
            'use strict';
            
            // Prevent back button
            history.pushState(null, null, location.href);
            window.onpopstate = function() {{
                history.go(1);
            }};
            
            // Clear referrer
            //document.referrer = '';
            
            // Auto-submit with delay and security checks
            let submitted = false;
            
            function secureSubmit() {{
                if (submitted) return;
                
                // Verify form integrity
                const form = document.getElementById('tokenForm');
                if (!form) {{
                    console.error('Security error: Form not found');
                    return;
                }}
                
                // Mark as submitted to prevent double submission
                submitted = true;
                
                // Submit form
                form.submit();
                
                // Clear form data from memory after submission
                setTimeout(() => {{
                    const inputs = form.querySelectorAll('input[type="hidden"]');
                    inputs.forEach(input => input.value = '');
                }}, 100);
            }}
            
            // Auto-submit after security delay
            setTimeout(() => {{
                secureSubmit();
            }}, 1500);
            
            // Fallback manual submit
            window.manualSubmit = secureSubmit;
            
            // Security: Clear sensitive data on page unload
            window.addEventListener('beforeunload', function() {{
                const form = document.getElementById('tokenForm');
                if (form) {{
                    const inputs = form.querySelectorAll('input[type="hidden"]');
                    inputs.forEach(input => input.value = '');
                }}
            }});
            
            // Disable right-click and key combinations in production
            document.addEventListener('contextmenu', e => e.preventDefault());
            document.addEventListener('keydown', function(e) {{
                // Disable F12, Ctrl+Shift+I, Ctrl+U, etc.
                if (e.keyCode === 123 || 
                    (e.ctrlKey && e.shiftKey && e.keyCode === 73) ||
                    (e.ctrlKey && e.keyCode === 85)) {{
                    e.preventDefault();
                    return false;
                }}
            }});
        }})();
    </script>
</body>
</html>"""

# Usage example:
# return HttpResponse(html_template.format(
#     service_url=service_url,
#     json_payload=json_payload
# ), content_type='text/html')


@method_decorator(csrf_exempt, name='dispatch')
class APIMfaStatusView(APIView):
    """
    Checks if MFA is enabled for a user after validating credentials.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        service_id = request.data.get('service_id')
        service = get_object_or_404(ServiceProvider, service_id=service_id)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        return Response({'mfa_required': user.is_mfa_enabled})



@method_decorator(csrf_exempt, name='dispatch')
class APILoginView(APIView):
    """
    Handles login. If MFA is enabled, requires MFA token.
    Issues JWT with custom claims.
    """
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            mfa_token = request.data.get('mfa_token')
            service_id = request.data.get('service_id')


            if settings.ENABLE_RECAPTCHA:
                recaptcha_response = request.data.get('g-recaptcha-response')
                print(recaptcha_response)
                data = {
                    'secret': settings.RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()

                print(result)

                if not result.get('success'):
                    return Response({'error': 'Invalid Captcha,Try Again'}, status=401)

            if not service_id:
                return Response({'error': 'Service ID not found or malformed'}, status=400)

            # Convert service_id to string if it's a UUID
            try:
                if isinstance(service_id, uuid.UUID):
                    service_id = str(service_id)
                elif service_id:
                    service_id = str(uuid.UUID(service_id))  # Ensure valid UUID format
            except (ValueError, TypeError):
                return Response({'error': 'Invalid service ID format'}, status=400)

            user = authenticate(username=username, password=password)
            service = get_object_or_404(ServiceProvider, service_id=service_id)

            if not user:
                return Response({'error': 'Invalid credentials'}, status=401)

            if user.is_mfa_enabled:
                print(1)
                if not mfa_token:
                    print(2)
                    return Response({'error': 'MFA token required'}, status=403)
                
                # FIXED: Call verify_mfa_status only ONCE
                mfa_verification_result = verify_mfa_status(request, user, mfa_token)
                print(f"MFA verification result: {mfa_verification_result}")
                
                if not mfa_verification_result:
                    print(3)
                    return Response({'error': 'Invalid MFA token'}, status=403)

            if not ServiceProviderUser.objects.filter(
                user=user,
                serviceprovider=service
            ).exists():
                return Response({'error': 'Not Allowed'}, status=403)

            backend = CustomJWTBackend()
            access_token, refresh_token = backend.get_token_pair(user=user, service_id=service_id)

            redirect_url = service.redirect_url

            #return redirect

            token_payload = {
                'access': str(access_token),
                'refresh': str(refresh_token),
            }

            json_payload = json.dumps(token_payload).replace('"', '&quot;')


            return HttpResponse(html_template.format(
            service_url=redirect_url,
            json_payload=json_payload),
            content_type='text/html')

        except Exception as e:
            logger.error(f"Login error: {str(e)}\n{traceback.format_exc()}")
            # Ensure error message is JSON-serializable
            error_message = str(e)
            if service_id:
                error_message = error_message.replace(str(service_id), str(service_id))
            return Response({'error': f'An unexpected error occurred: {error_message}'}, status=500)





@method_decorator(csrf_exempt, name='dispatch')
class APIRefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            service_id = request.data.get('service_id')

            backend = CustomJWTBackend()

            if not service_id:
                return Response({'error': 'Service ID not found or malformed'}, status=400)

            try:
                if isinstance(service_id, uuid.UUID):
                    service_id = str(service_id)
                elif service_id:
                    service_id = str(uuid.UUID(service_id))  # Ensure valid UUID format
            except (ValueError, TypeError):
                return Response({'error': 'Invalid service ID format'}, status=400)

            service = get_object_or_404(ServiceProvider, service_id=service_id)

            payload = backend.verify_token(refresh_token, service.service_secret, CustomJWTBackend.REFRESH_TOKEN)

            User = get_user_model()

            user = get_object_or_404(User, email=str(payload.get('email')))
            
            if not ServiceProviderUser.objects.filter(
                user=user,
                serviceprovider=service
            ).exists():
                return Response({'error': 'Not Allowed'}, status=403)
             

            
            access_token, refresh_token = backend.refresh_access_token(refresh_token=refresh_token, secret=service.service_secret, service_id=service_id)

            return Response({
                'access': str(access_token),
                'refresh': str(refresh_token),
            })

        except Exception as e:
            logger.error(f"Login error: {str(e)}\n{traceback.format_exc()}")
            # Ensure error message is JSON-serializable
            error_message = str(e)
            if service_id:
                error_message = error_message.replace(str(service_id), str(service_id))
            return Response({'error': f'An unexpected error occurred: {error_message}'}, status=500)


def verify_mfa_status(request, user, mfa_token):
    """
    Verifies the MFA token using django-otp.
    Logs the user in if the token is valid.
    """
    print(5)
    if not user.is_mfa_enabled:
        print(6)
        return True  # MFA not required

    try:
        print(8)
        device = TOTPDevice.objects.get(user=user)
        print(device)
        
        # Store result in variable to avoid double verification
        is_valid = device.verify_token(mfa_token)
        print(f'MFA verification result: {is_valid}')
        
        if is_valid:
            print(9)
            login(request, user)
            return True
        else:
            return False
            
    except ObjectDoesNotExist:
        return False
    except Exception as e:
        logger.error(f"Login error: {str(e)}\n{traceback.format_exc()}")
        return False




