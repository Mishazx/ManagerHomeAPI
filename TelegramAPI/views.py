from django.views import View
from django.http import JsonResponse

from django.conf import settings

from telebot import TeleBot, types


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