from django.contrib import admin
from django.urls import path, include

from .views import get_authorization_code, exchange_code_for_token


urlpatterns = [
    path('oauth/', get_authorization_code, name='get_authorization_code'),
    path('callback/', exchange_code_for_token, name='callback'), 

]
