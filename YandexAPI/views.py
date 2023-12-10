import json
import requests
from functools import wraps

from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings

from rest_framework.authtoken.models import Token

from .models import OAuthKey

CLIENT_ID = settings.YANDEX_OAUTH2_CLIENT_ID
SECRET_KEY = settings.YANDEX_OAUTH2_SECRET_KEY
REDIRECT_URI = settings.YANDEX_OAUTH2_REDIRECT_URI


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
    
    token = request.GET.get('token')
    tkn = Token.objects.get(key=token)

    OAuthKey.objects.get_or_create(
        user=tkn.user,
        defaults=token_data
    )

    return JsonResponse({'status': 'success', 'message': 'Keys added'})
