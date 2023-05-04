import telebot


TOKEN = '5822405479:AAE6_1Cp02yK3BxCzPTzoEK2pAw3aiM9fdg'

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def say_hallo(message: telebot.types.Message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Я бот, который реагирует на команду /hello_world,'
                              ' а также на текст «Hello».\n'
                              'Для помощи нажми - /help')


@bot.message_handler(content_types=['text'])
def answer(message: telebot.types.Message):
    user_id = message.from_user.id
    if message.text.lower() == 'hello' or message.text.lower() == 'привет':
        bot.send_message(user_id, f'Привет, {message.from_user.full_name}!')
    elif message.text == '/help':
        bot.send_message(user_id, 'Перейди по ссылке /hello_world или напиши «Привет»')
    elif message.text == '/hello_world':
        bot.send_message(user_id, 'Hello World, {}\nHave a good day!'.format(message.from_user.full_name))
    else:
        bot.send_message(user_id, "Я тебя не понимаю. Напиши /help.")


if __name__ == '__main__':  # todo: t.me/first_check_bot
    bot.polling()
