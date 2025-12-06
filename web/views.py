from django.shortcuts import render
from django.test import RequestFactory
from django.urls import reverse
from auth_provider.views import APILoginView
import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from auth_provider.models import ServiceProviderUser, ServiceProvider
from rest_framework.response import Response
from auth_provider.custom_jwt_backend import CustomJWTBackend
from django.http import HttpResponse
import json

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


def web_login(request):
    """Standard login page with username/password"""
    if settings.ENABLE_RECAPTCHA:
        return render(request, 'sso-login.html', {
            'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
            'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
        })
    return render(request, 'sso-login.html')


def web_login_v1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('user_dashboard')

        return Response({'error': 'Not Allowed'}, status=401)


    elif request.method == 'GET':
        return render(request, 'web-login.html')
    else:
        return Response({'error': 'Method Not Allowed'}, status=405)

@login_required
def user_dashboard(request):
    user_services = ServiceProviderUser.objects.filter(user=request.user)

    service_ids = []

    for service in user_services:
        service_ids.append(service.serviceprovider.service_id)
    
    return render(request, 'user_dashboard.html', {'services':service_ids})


@login_required
def redirect_to_service(request, service_id):
    service = ServiceProvider.objects.get(service_id=service_id)

    if not ServiceProviderUser.objects.filter(user=request.user,serviceprovider=service).exists():
        return Response({'error': 'Not Allowed'}, status=403)
    
    backend = CustomJWTBackend()
    access_token, refresh_token = backend.get_token_pair(user=request.user, service_id=service_id)

    redirect_url = service.redirect_url

    token_payload = {
        'access': str(access_token),
        'refresh': str(refresh_token),
    }

    json_payload = json.dumps(token_payload).replace('"', '&quot;')

    return HttpResponse(html_template.format(service_url=redirect_url,json_payload=json_payload),content_type='text/html')




def web_pla_login(request):
    """Passwordless login page"""
    if settings.ENABLE_RECAPTCHA:
        return render(request, 'sso-pla-login.html', {
            'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
            'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
        })
    return render(request, 'sso-pla-login.html')


def success_page(request):
    """Generic success page"""
    context = {
        'title': request.GET.get('title', 'Success!'),
        'message': request.GET.get('message', 'Your action was completed successfully.'),
    }
    return render(request, 'success.html', context)


def error_page(request):
    """Generic error page"""
    context = {
        'title': request.GET.get('title', 'Oops! Something Went Wrong'),
        'message': request.GET.get('message', 'We encountered an error while processing your request.'),
        'error_code': request.GET.get('error_code', None),
    }
    return render(request, 'error.html', context)


@login_required
def api_token_generator(request):
    """API Token Generator page for machine authentication"""
    # Get user's accessible services
    user_services = ServiceProviderUser.objects.filter(user=request.user)
    service_ids = [service.serviceprovider.service_id for service in user_services]

    context = {
        'services': service_ids,
        'access_timeout': settings.API_ACCESS_JWT_TIMEOUT,
        'refresh_timeout': settings.API_REFRESH_JWT_TIMEOUT,
    }
    return render(request, 'api_token_generator.html', context)


def user_logout(request):
    """Logout user and redirect to login page"""
    logout(request)
    return redirect('user_web_login')
