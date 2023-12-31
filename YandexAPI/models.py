from django.db import models
from django.contrib.auth.models import User


# Key YandexAPI IoT
class OAuthKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=50)


class DeviceManager(models.Manager):
    def get_next_device_id(self):
        last_device = self.order_by('-id').first()
        if last_device:
            return last_device.id + 1
        else:
            return 0


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=50)
    device_name = models.CharField(max_length=50)
    device_type = models.CharField(max_length=50)
    
    objects = DeviceManager()

    def save(self, *args, **kwargs):
        if not self.device_id:
            self.device_id = self.objects.get_next_device_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.device_name
