from telebot.types import Message

from loader import bot
from database.common.models import db, History
from database.utils.core import crud

db_write = crud.store()
db_read = crud.retrieve()


@bot.message_handler(commands=['history'])
def bot_history(message: Message):
    """ Функция-хэндлер bot_history, реализует комманду history.
         Отправляет пользователю историю поиска отелей """
    retrieved = db_read(db, History, History.user_command, History.created_at,
                        History.user_hotels).where(History.chat_id == message.from_user.id)

    for elem in retrieved:
        bot.send_message(message.from_user.id, f'Команда, которая была введена: {elem.user_command}\n'
                                               f'Дата и время ввода команды: {elem.created_at}\n'
                                               f'Отели, которые были найдены: {elem.user_hotels}')
