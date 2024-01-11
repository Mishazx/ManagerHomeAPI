from telebot import types
from django.contrib.auth.models import User

from YandexAPI.models import Device, OAuthKey


def create_MainKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)

    button1 = types.KeyboardButton("Все устройства 'Яндекс'")
    button2 = types.KeyboardButton("Настройки")

    keyboard.add(button1, button2)
    
    return keyboard


def create_DevicesKeyboard(username):
    user = User.objects.get(username=username)
    user_devices = Device.objects.filter(user=user)
    
    device_names = user_devices.values_list('device_name', flat=True)
    device_status = user_devices.values_list('online', flat=True)
    
    device_button_list = []
    
    for item, item_status in zip(list(device_names), list(device_status)):
        if item_status == True:
            item_status = '✅'
        else:
            item_status = '❌'
        device_button_list.append(types.InlineKeyboardButton(f"{item} {item_status}", callback_data=f"device_callback_{item_status}_{item}"))

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(*device_button_list)    
    
    button_what_on = types.InlineKeyboardButton(f"Что у меня включено?", callback_data='what_is_on')
    button_update_device = types.InlineKeyboardButton(f"Обновить", callback_data='update_devices')

    markup.add(button_what_on, button_update_device)

    return markup


def create_DeviceKeyboard(device_name_from_callback, state):
    keyboard = types.InlineKeyboardMarkup()
    if state:
        keyboard.add(types.InlineKeyboardButton(text="Выключить", callback_data=f"off_{device_name_from_callback}"))
    else:
        keyboard.add(types.InlineKeyboardButton(text="Включить", callback_data=f"on_{device_name_from_callback}"))
    keyboard.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data="back"))
    
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