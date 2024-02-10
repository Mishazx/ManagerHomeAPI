import requests
from functools import wraps

from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from YandexAPI.utils import control_device, register_allDevice

from .models import OAuthKey

CLIENT_ID = settings.YANDEX_OAUTH2_CLIENT_ID
SECRET_KEY = settings.YANDEX_OAUTH2_SECRET_KEY
REDIRECT_URI = settings.YANDEX_OAUTH2_REDIRECT_URI


from rest_framework import status
from .models import Device
from .serializers import DeviceSerializer, ScenarioSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets

from django.http import Http404


class DeviceViewSet(viewsets.ModelViewSet):
    # queryset = Device.objects.filter(user=self.request.user)
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        return self.control(request, *args, **kwargs)
    
    def control(self, request, pk=None):
        action_value = request.data.get('action', None)

        try:
            device = Device.objects.get(device_id=pk, user=request.user)
        except Device.DoesNotExist:
            return Response({'status': 'error', 'message': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        if action_value is not None:
            action = bool(action_value)
            control_device(request.user.username, pk, action)
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Missing action parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
        
    # @action(detail=True, methods=['post'])  # Removed 'detail=True'
    # def control(self, request, pk=None):
    #     # device_id = request.data.get('device_id', None)
    #     action_value = request.data.get('action', None)

    #     try:    
    #         device = Device.objects.get(device_id=pk, user=request.user)
    #     except Device.DoesNotExist:
    #         raise Http404("Custom Not Found Message")  # Custom Not Found Message

    #     if action_value is not None:
    #     #if device_id is not None and action_value is not None:
    #         action = bool(action_value)
    #         control_device(request.user.username, pk, action)
    #         return Response({'status': 'success'})
    #     else:
    #         return Response({'status': 'error', 'message': 'Missing device_id or action parameter'}, status=status.HTTP_400_BAD_REQUEST)    
        
    # def create(self, request, *args, **kwargs):
    #     return self.control(request, *args, **kwargs)
    
    
    
    
    # @action(detail=True, methods=['post'])
    # def control(self, request, pk=None):
    #     device = self.get_object()
    #     action_value = request.data.get('action', None)

    #     if action_value is not None:
    #         # Выполнить вашу команду control_device
    #         # Пример:
    #         control_device(request.user.username, device.id, action_value)
            
    #         return Response({'status': 'success'})
    #     else:
    #         return Response({'status': 'error', 'message': 'Missing action parameter'}, status=400)

        
class ScenarioViewSet(viewsets.ModelViewSet):
    # queryset = Device.objects.filter(user=self.request.user)
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class DeviceListView(APIView):
#     # queryset = Device.objects.all()
#     serializer_class = DeviceSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         queryset = Device.objects.all()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)
    
    # @action(detail=True, methods=['post'])
    # def toggle_online(self, request, pk=None):
    #     device = self.get_object()
    #     device.online = not device.online
    #     device.save()
    #     serializer = self.get_serializer(device)
    #     return Response(serializer.data)


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.GET.get("token")

        if not token:
            return JsonResponse({'error': 'no token'}, status=401)

        is_valid_token = Token.objects.filter(key=token).exists()

        if not is_valid_token:
            return JsonResponse({'error': 'no valid token'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


@custom_login_required
def get_authorization_code(request):
    yandex_oauth_url = "https://oauth.yandex.com/authorize"
    token = request.GET.get('token')
    
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    }

    authorization_url = f"{yandex_oauth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return redirect(f'{authorization_url}?token={token}')

@custom_login_required
def exchange_code_for_token(request):
    token_url = "https://oauth.yandex.com/token"
    authorization_code = request.GET.get('code', '')

    token_params = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": CLIENT_ID,
        "client_secret": SECRET_KEY,
        "redirect_uri": REDIRECT_URI,
        'Content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=token_params)
    token_data = response.json()
    print(token_data)
    
    token = request.GET.get('token')
    tkn = Token.objects.get(key=token)
    user = tkn.user

    OAuthKey.objects.get_or_create(
        user=user,
        defaults=token_data
    )
    
    tkn.delete()
    Token.objects.create(user=user)

    return JsonResponse({'status': 'success', 'message': 'Keys added'})

@custom_login_required
def register_all_devices(request):
    try:
        token = request.GET.get('token')
        tkn = Token.objects.get(key=token)
        user = tkn.user
        register_allDevice(user)
        tkn.delete()
        Token.objects.create(user=user)
        return JsonResponse({'status': 'success', 'message': 'Devices have been added successfully or already exist'})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
