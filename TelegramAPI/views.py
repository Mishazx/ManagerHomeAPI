from django.views import View
from django.http import JsonResponse

from django.conf import settings

from django.contrib.auth.models import User
from django.db import IntegrityError

from telebot import TeleBot, types

from .keyboard import create_MainKeyboard

from .utils import create_token_for_user


token = settings.TELEGRAM_BOT_TOKEN

bot = TeleBot(token)


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

bot.set_webhook(url=f"https://iot.mishazx.ru/tg/webhook/")