from telebot import types

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: types.Message):
    """ Функция-хэндлер bot_start, реализует комманду start. Отправляет пользователю сообщение с приветствем. """
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"Чтобы увидеть перечень команд, нажми на /help!")
