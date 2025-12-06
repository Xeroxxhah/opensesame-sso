from django.urls import path, include
from .views import *


urlpatterns = [
    # Standard login with password
    path('login/', web_login, name='web_login'),
    path('user-login/', web_login_v1, name='user_web_login'),
    path('user-logout/', user_logout, name='user_logout'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),

    # Service redirect
    path('redirect-to-service/<uuid:service_id>/', redirect_to_service, name='redirect_to_service'),

    # Passwordless login
    path('pla-login/', web_pla_login, name='web_pla_login'),

    # API Token Generator
    path('api-token-generator/', api_token_generator, name='api_token_generator'),

    # Success and error pages
    path('success/', success_page, name='success_page'),
    path('error/', error_page, name='error_page'),
]
