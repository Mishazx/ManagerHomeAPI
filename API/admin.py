from django.contrib import admin
from django.core.management import call_command
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    actions = ['show_active_sessions']

    def show_active_sessions(modeladmin, request, queryset):
        call_command('show_sessions')

admin.site.register(Session, SessionAdmin)
