from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from YandexAPI.models import Device
from YandexAPI.serializers import DeviceSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def toggle_online(self, request, pk=None):
        device = self.get_object()
        device.online = not device.online
        device.save()
        serializer = self.get_serializer(device)
        return Response(serializer.data)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['status'] = 'success'  # Пример добавления ID пользователя в ответ
        else:
            response.data['status'] = 'error'
        return response