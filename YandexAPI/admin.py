from django.contrib import admin
from .models import OAuthKey, Device


@admin.register(OAuthKey)
class OAuthKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'expires_in', 'refresh_token', 'token_type')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'device_id', 'device_name', 'device_type')
    search_fields = ('device_name', 'device_id')
    
    
admin.site.register(Device, DeviceAdmin)