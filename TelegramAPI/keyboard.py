from telebot import types
from django.contrib.auth.models import User

from YandexAPI.models import Device, OAuthKey


def create_MainKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)

    button1 = types.KeyboardButton("Все устройства 'Яндекс'")
    button2 = types.KeyboardButton("Настройки")

    keyboard.add(button1, button2)
    
    return keyboard

def create_SettingsKeyboard(username):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    
    user = User.objects.get(username=username)
    oauth_key = OAuthKey.objects.filter(user=user).exists()

    if oauth_key:
        buttonUnlink = types.KeyboardButton("Отвязать аккаунт 'Яндекс'")
        buttonRegisterDevices = types.KeyboardButton("Перерегистрировать все устройства")

        keyboard.add(buttonUnlink, buttonRegisterDevices)
        
    else:
        buttonLink = types.KeyboardButton("Привязать аккаунт 'Яндекс'")
        keyboard.add(buttonLink)

    buttonMain = types.KeyboardButton("Главное меню")
    keyboard.add(buttonMain)

    return keyboard