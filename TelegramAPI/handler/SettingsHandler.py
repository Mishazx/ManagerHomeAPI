from TelegramAPI.views import bot
from YandexAPI.models import Device, Scenario
from django.contrib.auth.models import User

from YandexAPI.utils import register_allDevice, register_allScenario



# Function re-register device yandex
@bot.message_handler(func=lambda message: "Перерегистрировать все устройства" in message.text)
def settingsMenu(message):
    try:
        username = message.chat.username
        user = User.objects.get(username=username)     
        Device.objects.filter(user=user).delete()
        bot.send_message(message.chat.id, f"Устройства удалены")
        output = register_allDevice(username)
        if output == 'Success':
            bot.send_message(message.chat.id, f'Устройства успешно добавлены')
        else:
            bot.send_message(message.chat.id, output)
            
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")    
        
        
# Function re-register scenario yandex
@bot.message_handler(func=lambda message: "Перерегистрировать все сценарии" in message.text)
def settingsMenu(message):
    try:
        username = message.chat.username
        user = User.objects.get(username=username)
        Scenario.objects.filter(user=user).delete()
        bot.send_message(message.chat.id, f"Сценарии удалены")     
        output = register_allScenario(username)
        if output == 'Success':
            bot.send_message(message.chat.id, f'Сценарии успешно добавлены')
        else:
            bot.send_message(message.chat.id, output)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")    