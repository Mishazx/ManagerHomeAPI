from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from telebot import TeleBot, types

from YandexAPI.models import Device, OAuthKey
from YandexAPI.utils import control_device, get_reconnect_device, register_allDevice

from .keyboard import create_DeviceKeyboard, create_MainKeyboard, create_SettingsKeyboard, create_DevicesKeyboard

from .utils import create_token_for_user


token = settings.TELEGRAM_BOT_TOKEN
url_domain = settings.DOMAIN_URL


bot = TeleBot(token)
url_tg_webhook = f'{url_domain}/tg/webhook/'
bot.set_webhook(url=url_tg_webhook)


class UpdateBot(View):
    def post(self, request):
        try:
            json_str = request.body.decode('UTF-8')
            update = types.Update.de_json(json_str)
            bot.process_new_updates([update])

            return JsonResponse({'code': 200})
        except Exception as e:
            print(f"Error processing update: {e}")
            return JsonResponse({'code': 500, 'error': str(e)})


@bot.message_handler(commands=['start'])
def start_message(message):
    text = '<b>Бот успешно запущен!</b>\n\n'
    text += "Чтобы начать использовать бота и настроить его нажмите '🖊️ Начать', .\n\n"
 
    keyboard = types.InlineKeyboardMarkup()
    key_begin = types.InlineKeyboardButton(text='🖊️ Начать', callback_data='runbot')
    keyboard.add(key_begin)
 
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')        
    
    
# Register user on the System
@bot.callback_query_handler(func=lambda call: call.data == 'runbot')
def handle_begin_callback(call):
    try:
        username = call.from_user.username
        first_name = call.from_user.first_name
        last_name = call.from_user.last_name
        last_name = last_name if last_name is not None else ''

        try:
            user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name)
        except IntegrityError:
            user = User.objects.get(username=username)
            created = False
            
        create_token_for_user(call.from_user.username)

        if created:
            print(f'Пользователь (user) {username} был успешно создан.')

        else:
            print('Пользователь не создался')
            
        keyboard = create_MainKeyboard()
        
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f'Доброго {username}',reply_markup=keyboard)
       
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка: {e}")
        import traceback
        bot.send_message(call.message.chat.id, f'{traceback.format_exc()}')


@bot.message_handler(func=lambda message: "Все устройства 'Яндекс'" in message.text)
def settingsMenu(message):
    try:        
        keyboard = create_DevicesKeyboard(message.chat.username)
        bot.send_message(message.chat.id, f"Вы находитесь в меню\nВсе устройства 'Яндекс'", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")    


@bot.callback_query_handler(func=lambda call: call.data.startswith('device_callback_'))
def handle_device_run_callback(call):
    device_name_from_callback = call.data.split('_')[-1]
    status = call.data.split('_')[-2]
    username = call.from_user.username

    try:
        user = User.objects.get(username=username)
        user_device = Device.objects.get(user=user, device_name=device_name_from_callback)
        device_id = user_device.device_id
        
        if status == '❌':
            # СЮДА УВЕДОМЛЕНИЕ СДЕЛАТЬ
            bot.answer_callback_query(callback_query_id=call.id, text="Устройство офлайн.\nПроверьте устройство или нажмите кнопку обновить.", show_alert=True)
            
        else:
            data, state = get_reconnect_device(username, device_id, device_name_from_callback)


            keyboard = create_DeviceKeyboard(device_name_from_callback, state)


            bot.edit_message_text(
                chat_id=call.from_user.id, 
                message_id=call.message.message_id, 
                text=data, 
                reply_markup=keyboard
                )            # Отправляем сообщение о статусе устройства

    except User.DoesNotExist:
        bot.send_message(call.from_user.id, "Пользователь не найден в базе данных.")
    except Device.DoesNotExist:
        bot.send_message(call.from_user.id, "Устройства пользователя не найдены в базе данных.")
    except Exception as e:
        import traceback
        bot.send_message(call.from_user.id, f'{traceback.format_exc()}')
        bot.send_message(call.from_user.id, f"Ошибка: {e}")




# Обработка команд для управления устройством
@bot.callback_query_handler(func=lambda call: call.data.startswith(('on_', 'off_')))
def handle_device_control_callback(call):
    
    try:
        username = call.from_user.username
        command, device_name = call.data.split('_')[:2]
        user = User.objects.get(username=username)
        device_instance = Device.objects.get(user=user, device_name=device_name)
                
        # Запрос на сервер яндекс о статусе и времени
        # bot.send_message(call.from_user.id, f'DATA! device: {on_off_state} !! {dt_object}')

        device_id_value = device_instance.device_id
        if command == 'on':
            msg = control_device(username, device_id_value, True) # ВКЛЮЧИТЬ ДЛЯ РЕАЛЬНО ИСПОЛЬЗОВАНИЯ
            bot.answer_callback_query(callback_query_id=call.id, 
                                      text=f"Включили устройство '{device_name}'")
            # bot.send_message(call.from_user.id, str(msg))

        # elif command == 'off':
        else:
            msg = control_device(username, device_id_value, False) # ВКЛЮЧИТЬ ДЛЯ РЕАЛЬНО ИСПОЛЬЗОВАНИЯ
            bot.answer_callback_query(callback_query_id=call.id, 
                                      text=f"Выключили устройство '{device_name}'")
            # bot.send_message(call.from_user.id, str(msg))


        data, state = get_reconnect_device(username, device_id_value, device_name)

        keyboard = create_DeviceKeyboard(device_name, state)

        bot.edit_message_text(
                chat_id=call.from_user.id, 
                message_id=call.message.message_id, 
                text=data, 
                reply_markup=keyboard
                )            # Отправляем сообщение о статусе устройства
        # поменять информацию

               
    except Device.DoesNotExist:
        bot.send_message(call.from_user.id, f"Устройство с именем {device_name} не найдено.")

    except Exception as e:
        bot.send_message(call.from_user.id, f"Ошибка: {e}")



@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back_callback(call):
    try:
        keyboard = create_DevicesKeyboard(call.from_user.username)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f"Вы находитесь в меню\nВсе устройства 'Яндекс'", reply_markup=keyboard)            # Отправляем сообщение о статусе устройства
    except Exception as e:
        bot.send_message(call.from_user.id, f"Ошибка: {e}")


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


@bot.callback_query_handler(func=lambda call: call.data == 'link_yandex')
def link_yandex(call):
    try:
        username = call.from_user.username
        user = User.objects.get(username=username)
        oauth_key = OAuthKey.objects.filter(user=user).exists()
                
        if oauth_key:
            keyboard = create_SettingsKeyboard(username)
            bot.send_message(call.message.chat.id, "Аккаунт 'Яндекс' успешно привязан", reply_markup=keyboard)
            register_allDevice(username)
                
        else:
            bot.send_message(call.message.chat.id, "Не удалось привязать аккаунт, попробуйте еще раз или попробуйте познее")
            
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка: {e}")


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


@bot.message_handler(func=lambda message: 'Главное меню' in message.text)
def mainMenu(message):
    try:
        keyboard = create_MainKeyboard()
        bot.send_message(message.chat.id, f'Вы находитесь в главном меню', reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(func=lambda message: 'Настройки' in message.text)
def settingsMenu(message):
    try:
        keyboard = create_SettingsKeyboard(message.chat.username)
        bot.send_message(message.chat.id, f'Вы находитесь в меню настроек',reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
