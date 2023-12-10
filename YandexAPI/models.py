from django.db import models
from django.contrib.auth.models import User


# Key YandexAPI IoT
class OAuthKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=50)
