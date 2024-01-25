from telebot import types
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from TelegramAPI.keyboard import create_SettingsKeyboard
from TelegramAPI.views import bot, url_domain
from YandexAPI.models import OAuthKey
from YandexAPI.utils import register_allDevice, register_allScenario


# Function link account Yandex
@bot.message_handler(func=lambda message: "Привязать аккаунт 'Яндекс'" in message.text)
def mainMenu(message):
    try:
        username = message.chat.username
        user = User.objects.get(username=username)
        token = Token.objects.get(user=user)
        token_key = token.key
        
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Кликните сюда", 
                                              url=f"{url_domain}/yaapi/oauth/?token={token_key}")
        markup.add(button)
        bot.send_message(message.chat.id, "Для перехода на сайт для привязки аккаунта", reply_markup=markup)
        
        markup = types.InlineKeyboardMarkup()
        button2 = types.InlineKeyboardButton("Проверить привязку аккаунта 'Яндекс'", 
                                               callback_data='link_yandex')
        markup.add(button2)
        bot.send_message(message.chat.id, 'После привязки нажмите сюда, для завершения', reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


# Function check link yandex, after actions user
@bot.callback_query_handler(func=lambda call: call.data == 'link_yandex')
def link_yandex(call):
    try:
        username = call.from_user.username
        user = User.objects.get(username=username)
        oauth_key = OAuthKey.objects.filter(user=user).exists()
                
        if oauth_key:
            keyboard = create_SettingsKeyboard(username)
            register_allDevice(username)
            register_allScenario(username)
            bot.send_message(call.message.chat.id, "Аккаунт 'Яндекс' успешно привязан", reply_markup=keyboard)

                
        else:
            bot.send_message(call.message.chat.id, "Не удалось привязать аккаунт, попробуйте еще раз или попробуйте познее")
            
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка: {e}")


# Unlink account Yandex
@bot.message_handler(func=lambda message: "Отвязать аккаунт 'Яндекс'" in message.text)
def unlinkYandex(message):
    username = message.chat.username
    user = User.objects.get(username=username)
    oauth_key_exists = OAuthKey.objects.filter(user=user).exists()
    if oauth_key_exists:
        oauth_key = OAuthKey.objects.get(user=user)
        oauth_key.delete()
        keyboard = create_SettingsKeyboard(username)
        bot.send_message(message.chat.id, "Аккаунт 'Яндекс' успешно отвязан", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так!")
