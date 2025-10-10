from django.urls import path, include
from .views import *


urlpatterns = [
    # Standard login with password
    path('login/', web_login, name='web_login'),

    # Passwordless login
    path('pla-login/', web_pla_login, name='web_pla_login'),

    # Success and error pages
    path('success/', success_page, name='success_page'),
    path('error/', error_page, name='error_page'),
]
