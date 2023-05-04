from telebot import types

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: types.Message):
    """ Функция-хэндлер bot_help, реализует комманду help.
     Отправляет пользователю справку с названями и описаниями комманд."""
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
