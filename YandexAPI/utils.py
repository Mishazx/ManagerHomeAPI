import requests
from requests.exceptions import RequestException
import threading
import time
from datetime import datetime, timedelta
from queue import Queue
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Device, OAuthKey


def control_device(username, id, flag, max_retries=5):
    for attempt in range(max_retries):
        try:
            user = User.objects.get(username=username)
            auth_key = OAuthKey.objects.get(user=user)
            access_token = auth_key.access_token
            
            if not isinstance(flag, bool):
                return 'flag != bool'


            url = 'https://api.iot.yandex.net/v1.0/devices/actions'

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            data = {
                "devices": [
                    {
                        "id": id,
                        "actions": [{
                                "type": "devices.capabilities.on_off",
                                "state": {
                                    "instance": "on",
                                    "value": flag
                                }
                            }]
                        }
                    ]
                }
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        
        except RequestException as e:
            time.sleep(0.7)
    return None


def get_reconnect_device(username, device_id, device_name):
    data_device = get_device(username, device_id)
    on_off_capability = next(cap for cap in data_device['capabilities'] if cap['type'] == 'devices.capabilities.on_off')
    on_off_bool = on_off_capability['state']['value']
    on_off_last_updated = on_off_capability['last_updated']
    dt_object = datetime.fromtimestamp(on_off_last_updated) + timedelta(hours=3)
    dt_object = dt_object.replace(microsecond=0).strftime("%H:%M:%S %d-%m-%Y")
    
    if on_off_bool:
        on_off_state = 'Включено'
    else:
        on_off_state = 'Выключено'

    
    text = f"Статус устройства '{device_name}' \nНа {dt_object} \n{on_off_state}"
    
    return text, on_off_bool


def get_device(username, device_id, max_retries=5):
    for attempt in range(max_retries):
        try:
            user = User.objects.get(username=username)
            auth_key = OAuthKey.objects.get(user=user)
            access_token = auth_key.access_token
            url = f'https://api.iot.yandex.net/v1.0/devices/{device_id}'
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url, headers=headers)
            return response.json()

        except RequestException as e:
            time.sleep(0.7)

    return None


def for_thread_getdevice(username, device, result_queue):
    data = get_device(username, device)
    result_queue.put(data)


def get_data_devices(username, device_id_list):
        data = []
        threads = []
        result_queue = Queue()

        for device in device_id_list:
            th = threading.Thread(target=for_thread_getdevice, args=(username, device, result_queue))
            threads.append(th)
            th.start()

        for thread in threads:
            thread.join()
            
        while not result_queue.empty():
            data.append(result_queue.get())
        return data


def get_all_info(username):
    user = User.objects.get(username=username)
    auth_key = OAuthKey.objects.get(user=user)

    access_token = auth_key.access_token

    url = 'https://api.iot.yandex.net/v1.0/user/info'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    response = requests.get(url, headers=headers)
    return response.json()


def register_allDevice(username):
    try:
        user = User.objects.get(username=username)
        
        data = get_all_info(username)
        device_id_list = [i['id'] for i in data['devices']]

        combined_list = [(item['name'], item['id'], item['state'], item['type']) for item in get_data_devices(username, device_id_list)]

        for device_name, device_id, device_online, device_type in combined_list:
            existing_device = Device.objects.filter(device_id=device_id, user=user).first()
            if not existing_device:
                if device_online == 'online':
                    device_online = True
                else:
                    device_online = False
                Device.objects.create(
                    user=user,
                    device_id=device_id,
                    device_name=device_name,
                    device_type=device_type,
                    online=device_online
                    
                )
        
        return 'Success'
    
    except Exception as e:
        return e
