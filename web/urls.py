from django.urls import path, include
from .views import *


urlpatterns = [

    path('login/', web_login, name='web_login'),
    #path('mfa-status/',APIMfaStatusView.as_view(), name='api_mfa_status')
]
