from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
