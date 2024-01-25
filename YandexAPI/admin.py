from django.contrib import admin
from .models import OAuthKey, Device, Scenario


@admin.register(OAuthKey)
class OAuthKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'expires_in', 'refresh_token', 'token_type')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ( 'device_name', 'device_id', 'device_type', 'user', 'online')
    search_fields = ('device_name', 'device_id')
    
class ScenarionAdmin(admin.ModelAdmin):
    list_display = ('scenario_name', 'scenario_id', 'user', 'status')
    
    
admin.site.register(Device, DeviceAdmin)
admin.site.register(Scenario, ScenarionAdmin)