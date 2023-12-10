import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Device, OAuthKey


def register_allDevice(username):
    try:
        user = User.objects.get(username=username)
        auth_key = OAuthKey.objects.get(user=user)

        access_token = auth_key.access_token
        
        url = f'https://api.iot.yandex.net/v1.0/user/info'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        
        device_id_list = [i['id'] for i in data['devices']]
        device_name_list = [i['name'] for i in data['devices']]
        device_type_list = [i['type'] for i in data['devices']]
        
        for device_id, device_name, device_type in zip(device_id_list, device_name_list, device_type_list):
            existing_device = Device.objects.filter(device_id=device_id, user=user).first()
            if not existing_device:
                Device.objects.create(
                    user=user,
                    device_id=device_id,
                    device_name=device_name,
                    device_type=device_type
                )
        
        return 'Success'
    
    except Exception as e:
        return e
