from YandexAPI.utils import get_info_scenarios
from telebot import types
from django.contrib.auth.models import User

from YandexAPI.models import Device, OAuthKey, Scenario


# Func create Main Keyboard
def create_MainKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)

    ButtonDevices = types.KeyboardButton("Все устройства 'Яндекс'")
    Buttonscenario = types.KeyboardButton("Все сценарии")
    ButtonSettings = types.KeyboardButton("Настройки")

    keyboard.add(ButtonDevices) 
    keyboard.add(Buttonscenario, ButtonSettings)
    
    return keyboard


# def create_DevicesKeyboard(username):
#     user = User.objects.get(username=username)
#     user_devices = Device.objects.filter(user=user)
    
#     device_names = user_devices.values_list('device_name', flat=True)
#     device_status = user_devices.values_list('online', flat=True)
    
#     device_button_list = []
    
#     for item, item_status in zip(list(device_names), list(device_status)):
#         if item_status == True:
#             item_status = '✅'
#         else:
#             item_status = '❌'
#         device_button_list.append(types.InlineKeyboardButton(f"{item} {item_status}", callback_data=f"device_callback_{item_status}_{item}"))

#     markup = types.InlineKeyboardMarkup(row_width=1)
#     markup.add(*device_button_list)

#     return markup


# Func create Devices Keyboard
def create_DevicesKeyboard(username, page=1, items_per_page=5):
    user = User.objects.get(username=username)
    user_devices = Device.objects.filter(user=user)
    
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    
    device_names = user_devices.values_list('device_name', flat=True)[start_index:end_index]
    device_status = user_devices.values_list('online', flat=True)[start_index:end_index]
        
    device_button_list = []
    
    for item, item_status in zip(list(device_names), list(device_status)):
        if item_status == True:
            item_status = '✅'
        else:
            item_status = '❌'
        device_button_list.append(types.InlineKeyboardButton(f"{item} {item_status}", callback_data=f"device_callback_{item_status}_{item}"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*device_button_list)
    
    total_devices = user_devices.count()
    total_pages = (total_devices // items_per_page) + (1 if total_devices % items_per_page > 0 else 0)

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(types.InlineKeyboardButton(text="⬅️", callback_data=f'device_page_{page - 1}'))
    if page < total_pages:
        pagination_buttons.append(types.InlineKeyboardButton(text="➡️", callback_data=f'device_page_{page + 1}'))
    if pagination_buttons:
        keyboard.row(*pagination_buttons)

    return keyboard


# Func create Device Keyboard
def create_DeviceKeyboard(device_data):
    keyboard = types.InlineKeyboardMarkup()
    device_name = device_data[0]
    print(device_data)
    if len(device_data) > 2:
        if device_data[2]:
            keyboard.add(types.InlineKeyboardButton(text="Выключить", callback_data=f"off_{device_name}"))
        else:
            keyboard.add(types.InlineKeyboardButton(text="Включить", callback_data=f"on_{device_name}"))

    keyboard.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data="back"))
    return keyboard


# def create_ScenariosKeyboard(username):
#     user = User.objects.get(username=username)
#     scenarios = Scenario.objects.filter(user=user)
    
#     scenarios_button_list = []
    
#     scenario_name = scenarios.values_list('scenario_name', flat=True)
    
#     for item in list(scenario_name):
#         scenarios_button_list.append(types.InlineKeyboardButton(text=item, callback_data=f'scenario_callback_{item}'))

#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*scenarios_button_list)    

#     return keyboard


# Func create Scenarios Keyboard
def create_ScenariosKeyboard(username, page=1, items_per_page=5):
    user = User.objects.get(username=username)
    scenarios = Scenario.objects.filter(user=user)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    scenarios_button_list = []

    scenario_name = scenarios.values_list('scenario_name', flat=True)[start_index:end_index]

    for item in list(scenario_name):
        scenarios_button_list.append(types.InlineKeyboardButton(text=item, callback_data=f'scenario_callback_{item}'))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*scenarios_button_list)

    total_scenarios = scenarios.count()
    total_pages = (total_scenarios // items_per_page) + (1 if total_scenarios % items_per_page > 0 else 0)

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(types.InlineKeyboardButton(text="<<", callback_data=f'scenario_page_{page - 1}'))
    if page < total_pages:
        pagination_buttons.append(types.InlineKeyboardButton(text=">>", callback_data=f'scenario_page_{page + 1}'))
    if pagination_buttons:
        keyboard.add(*pagination_buttons)

    return keyboard


# Func create Settings Keyboard
def create_SettingsKeyboard(username):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    user = User.objects.get(username=username)
    oauth_key = OAuthKey.objects.filter(user=user).exists()

    if oauth_key:
        buttonUnlink = types.KeyboardButton("Отвязать аккаунт 'Яндекс'")
        buttonRegisterDevices = types.KeyboardButton("Перерегистрировать все устройства")
        buttonRegisterScenarios = types.KeyboardButton("Перерегистрировать все сценарии")
        keyboard.add(buttonUnlink)
        keyboard.add(buttonRegisterDevices, buttonRegisterScenarios)
        
    else:
        buttonLink = types.KeyboardButton("Привязать аккаунт 'Яндекс'")
        keyboard.add(buttonLink)

    buttonMain = types.KeyboardButton("Главное меню")
    keyboard.add(buttonMain)

    return keyboard