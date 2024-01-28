from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = 'Show active sessions'

    def handle(self, *args, **options):
        sessions = Session.objects.filter(expire_date__gt=timezone.now())

        for session in sessions:
            self.stdout.write(self.style.SUCCESS(f"Session Key: {session.session_key}"))
            self.stdout.write(self.style.SUCCESS(f"    Expire Date: {session.expire_date}"))
            self.stdout.write(self.style.SUCCESS(f"    Session Date: {session.get_decoded()}"))
            self.stdout.write(self.style.SUCCESS(""))

        self.stdout.write(self.style.SUCCESS(f"Total active sessions: {sessions.count()}"))
