from django.shortcuts import render
from django.test import RequestFactory
from django.urls import reverse
from auth_provider.views import APILoginView
import json
from django.conf import settings


def web_login(request):
    """Standard login page with username/password"""
    if settings.ENABLE_RECAPTCHA:
        return render(request, 'sso-login.html', {
            'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
            'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
        })
    return render(request, 'sso-login.html')


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
