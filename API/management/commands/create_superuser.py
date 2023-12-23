import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 
                os.getenv("DJANGO_SUPERUSER_EMAIL"), 
                os.getenv("DJANGO_SUPERUSER_PASSWORD"))
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
