from django.shortcuts import render
from django.test import RequestFactory
from django.urls import reverse
from auth_provider.views import APILoginView
import json
from django.conf import settings
# Create your views here.





def web_login(request):

    if settings.ENABLE_RECAPTCHA:
        return render(request,'sso-login.html',{
        'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    })

    return render(request,'sso-login.html')




from django.conf import settings
from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html', {
        'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    })
