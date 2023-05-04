import commands
from loader import bot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


if __name__ == '__main__':  # todo: t.me/search_hotellls_bot
    set_default_commands(bot)
    bot.infinity_polling()
