from TelegramAPI.views import bot
from TelegramAPI.keyboard import create_MainKeyboard, create_SettingsKeyboard

# Function handle 'Main menu"
@bot.message_handler(func=lambda message: 'Главное меню' in message.text)
def mainMenu(message):
    try:
        keyboard = create_MainKeyboard()
        bot.send_message(message.chat.id, f'Вы находитесь в главном меню', reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


# Function handle 'Settings menu'
@bot.message_handler(func=lambda message: 'Настройки' in message.text)
def settingsMenu(message):
    try:
        keyboard = create_SettingsKeyboard(message.chat.username)
        bot.send_message(message.chat.id, f'Вы находитесь в меню настроек',reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")