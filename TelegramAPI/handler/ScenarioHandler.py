from django.contrib.auth.models import User
from TelegramAPI.keyboard import create_ScenariosKeyboard
from TelegramAPI.views import bot
from YandexAPI.models import Scenario
from YandexAPI.utils import get_info_scenarios, start_scenario

# Function re-register device yandex
@bot.message_handler(func=lambda message: "Все сценарии" in message.text)
def scenarioMenu(message):
    try:
        keyboard = create_ScenariosKeyboard(message.chat.username)
        bot.send_message(message.chat.id, 'Все сценарии', reply_markup=keyboard)
            
    except Exception as e:
        import traceback
        bot.send_message(message.chat.id, f'{traceback.format_exc()}')
        bot.send_message(message.chat.id, f"Ошибка: {e}")
        
# Handler menu scenario
@bot.callback_query_handler(func=lambda call: call.data.startswith('scenario_callback_'))
def handle_scenario_run_callback(call):
    scenario_name_from_callback = call.data.split('_')[-1]
    username = call.from_user.username

    try:
        user = User.objects.get(username=username)
        user_scenario = Scenario.objects.get(user=user, scenario_name=scenario_name_from_callback)
        scenario_id = user_scenario.scenario_id
        
        data = start_scenario(username, scenario_id)
        data = data['status']
        
        keyboard = create_ScenariosKeyboard(username)
        
        if data == 'ok':
            bot.edit_message_text(chat_id=call.from_user.id, 
                                  message_id=call.message.message_id,
                                  text=f"Сценарий '{scenario_name_from_callback}' был запущен",
                                  reply_markup=keyboard
                                  )
        else:
            bot.edit_message_text(chat_id=call.from_user.id, 
                                  message_id=call.message.message_id,
                                  text=f"Сценарий '{scenario_name_from_callback}' небыл отработан",
                                  reply_markup=keyboard
                                  )
        
        
    except Scenario.DoesNotExist:
        bot.send_message(call.from_user.id, "Сценарий не найден в базе данных.")
    except Exception as e:
        import traceback
        bot.send_message(call.from_user.id, f'{traceback.format_exc()}')
        bot.send_message(call.from_user.id, f"Ошибка: {e}")

# Handler page scenario
@bot.callback_query_handler(func=lambda call: call.data.startswith('scenario_page_'))
def handle_scenario_run_callback_page(call):
    page_number = int(call.data.split('_')[-1])
    keyboard = create_ScenariosKeyboard(call.from_user.username, page=page_number)
    bot.answer_callback_query(callback_query_id=call.id, text="")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id,
                                reply_markup=keyboard)