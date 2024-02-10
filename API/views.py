from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from YandexAPI.utils import control_device
from .serializers import ChangePasswordSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Вход выполнен успешно'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Ошибка входа'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            
            current_user = self.request.user
            if current_user.username == request.data.get('username'):
                current_user.set_password(new_password)
                current_user.save()
                return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Вы не можете изменить пароль другого пользователя'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class UserInfoView(APIView):
    authentication_classes = (SessionAuthentication,)
    def get(self, request, *args, **kwargs):
        try:
            user_data = {
                'status': 0,
                'username': request.user.username,
                'email': request.user.email,
                # Добавьте другие необходимые данные пользователя
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ 'status': 1, 'error': 'User not authenticated'}, status=status.HTTP_200_OK)


class ControlDeviceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.user.username
        device_id_value = request.data.get('device_id')
        result = control_device(username, device_id_value, True)

        return Response({'result': result}, status=status.HTTP_200_OK)
