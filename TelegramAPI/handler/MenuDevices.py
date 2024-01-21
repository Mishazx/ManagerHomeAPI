from TelegramAPI.views import bot
from django.contrib.auth.models import User
from TelegramAPI.keyboard import create_DeviceKeyboard, create_DevicesKeyboard
from YandexAPI.models import Device
from YandexAPI.utils import control_device, get_capabilities_on_off, get_reconnect_device


# Function menu device list
@bot.message_handler(func=lambda message: "Все устройства 'Яндекс'" in message.text)
def settingsMenu(message):
    try:        
        keyboard = create_DevicesKeyboard(message.chat.username)
        bot.send_message(message.chat.id, f"Вы находитесь в меню\nВсе устройства 'Яндекс'", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")    


# Handler menu device
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
            bot.answer_callback_query (
                callback_query_id=call.id, 
                text="Устройство офлайн.\nПроверьте устройство или нажмите кнопку обновить.", 
                show_alert=True
            )
            
        else:

            data, data_device = get_reconnect_device(username, device_id)
            keyboard = create_DeviceKeyboard(data_device)

            bot.edit_message_text (
                chat_id=call.from_user.id, 
                message_id=call.message.message_id, 
                text=data, 
                reply_markup=keyboard
            ) 
                
            

    except User.DoesNotExist:
        bot.send_message(call.from_user.id, "Пользователь не найден в базе данных.")
    except Device.DoesNotExist:
        bot.send_message(call.from_user.id, "Устройства пользователя не найдены в базе данных.")
    except Exception as e:
        import traceback
        bot.send_message(call.from_user.id, f'{traceback.format_exc()}')
        bot.send_message(call.from_user.id, f"Ошибка: {e}")        

        
# Handler cmd control device
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
            control_device(username, device_id_value, True) # ВКЛЮЧИТЬ ДЛЯ РЕАЛЬНО ИСПОЛЬЗОВАНИЯ
            bot.answer_callback_query(callback_query_id=call.id, 
                                      text=f"Включили устройство '{device_name}'")

        else:
            control_device(username, device_id_value, False) # ВКЛЮЧИТЬ ДЛЯ РЕАЛЬНО ИСПОЛЬЗОВАНИЯ
            bot.answer_callback_query(callback_query_id=call.id, 
                                      text=f"Выключили устройство '{device_name}'")
            

        data, data_device = get_reconnect_device(username, device_id_value)
        keyboard = create_DeviceKeyboard(data_device)

        bot.edit_message_text (
            chat_id=call.from_user.id, 
            message_id=call.message.message_id, 
            text=data, 
            reply_markup=keyboard
        )            # Отправляем сообщение о статусе устройства
        # поменять информацию

    except Device.DoesNotExist:
        bot.send_message(call.from_user.id, f"Устройство с именем {device_name} не найдено.")
    except Exception as e:
        import traceback
        bot.send_message(call.from_user.id, f'{traceback.format_exc()}')
        bot.send_message(call.from_user.id, f"Ошибка: {e}")
        

# Function handle 'back' in devices list
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back_callback(call):
    try:
        keyboard = create_DevicesKeyboard(call.from_user.username)
        bot.edit_message_text (
            chat_id=call.from_user.id, 
            message_id=call.message.message_id, 
            text=f"Вы находитесь в меню\nВсе устройства 'Яндекс'", 
            reply_markup=keyboard
        )
        
    except Exception as e:
        bot.send_message(call.from_user.id, f"Ошибка: {e}")