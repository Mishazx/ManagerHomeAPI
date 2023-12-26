from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_token_for_user(username):
    user, created = User.objects.get_or_create(username=username)
    token, created = Token.objects.get_or_create(user=user)

    return token.key, user.id