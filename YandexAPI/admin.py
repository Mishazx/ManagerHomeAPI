from django.contrib import admin
from .models import OAuthKey


@admin.register(OAuthKey)
class OAuthKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'expires_in', 'refresh_token', 'token_type')
