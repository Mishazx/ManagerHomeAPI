from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from YandexAPI.models import Device
from YandexAPI.serializers import DeviceSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         if not username:
#             return Response({'error': '!!Username is required.'}, status=400)
#         if username:
#             User = get_user_model()
#             user, created = User.objects.get_or_create(username=username)
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response({'error': 'Username is required.'}, status=400)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'device_name'

    @action(detail=True, methods=['post'])
    def toggle_online(self, request, pk=None):
        device = self.get_object()
        device.online = not device.online
        device.save()
        serializer = self.get_serializer(device)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['status'] = 'success'  # Пример добавления ID пользователя в ответ
        else:
            response.data['status'] = 'error'
        return response