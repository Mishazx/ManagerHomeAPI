from django.contrib import admin
from django.urls import path, include

from .views import get_authorization_code, exchange_code_for_token, register_all_devices


urlpatterns = [
    path('oauth/', get_authorization_code, name='get_authorization_code'),
    path('callback/', exchange_code_for_token, name='callback'), 
    path('register/', register_all_devices, name='register_all_devices'),

]
