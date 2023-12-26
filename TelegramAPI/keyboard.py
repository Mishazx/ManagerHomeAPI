from telebot import types


def create_MainKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)

    button1 = types.KeyboardButton("Все устройства 'Яндекс'")
    button2 = types.KeyboardButton("Настройки")

    keyboard.add(button1, button2)
    
    return keyboard