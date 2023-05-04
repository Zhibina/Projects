import time
from datetime import datetime
from telebot import types

from loader import bot
from commands.start import bot_start
from rapid_requests.locations import search_locations
from rapid_requests.properties import search_properties
from rapid_requests.details import search_details, search_photos
from commands.history import db_write, History, db

user_data = {}


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: types.Message):
    """ Функция-хэндлер, реализует комманду lowprice. Запрашивает у пользователя
     хочет ли он увидеть отели по наименьшей стоимости и вызывает указанную функцию """
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    butt_yes = types.KeyboardButton(text='да')
    butt_no = types.KeyboardButton(text='нет')
    keyboard.add(butt_yes, butt_no)

    msg = bot.send_message(message.from_user.id, 'Если хотите увидеть отели по наименьшей стоимости, нажмите "да".'
                                                 '\nВ ином случае, нажмите "нет".', reply_markup=keyboard)
    bot.register_next_step_handler(msg, check_city)


def check_city(message: types.Message):
    """ Функция check_city, ловит ответ пользователя и, в случае утвердительного ответа,
    запрашивает город, где будет проводиться поиск и вызывает указанную функцию"""
    answer = message.text
    if answer == 'да':
        msg = bot.reply_to(message, 'Введите название города, где будет производиться поиск')
        bot.register_next_step_handler(msg, location)
    else:
        bot.reply_to(message, ':(')


def location(message: types.Message):
    """ Функция location, ловит ответ пользователя и, если город введён корректно,
        запрашивает дату възда и вызывает указанную функцию"""
    city = message.text
    if not city.isalpha():
        msg = bot.reply_to(message, 'Возможно, вы ввели лишний символ, попробуйте ещё раз')
        bot.register_next_step_handler(msg, location)
        return

    user_data['city'] = city
    region_id = search_locations(user_data['city'])
    user_data['region_id'] = region_id
    msg = bot.reply_to(message, f'Укажите дату възда в формате: d-m-y\n'
                                f'Пример: 6-1-2023')
    bot.register_next_step_handler(msg, check_in)


def check_in(message: types.Message):
    """ Функция check_in, ловит ответ пользователя и, если формат даты введён корректно,
        записывает в словарь с данными информацию о въезде, запрашивает дату выезда и вызывает указанную функцию"""
    if not message.text.isalpha():
        day, month, year = map(int, message.text.split('-'))
        if day <= 31 and month <= 12 and year <= 2024:
            user_data['check_in'] = message.text
            msg = bot.reply_to(message, f'Укажите дату выезда в формате: d-m-y\n'
                                        f'Пример: 10-1-2023')
            bot.register_next_step_handler(msg, check_out)
        else:
            msg = bot.reply_to(message, 'Возможно вы ошиблись с датой, или форматом ввода, попробуйте ещё раз\n'
                                        'Пример: 6-1-2023')
            bot.register_next_step_handler(msg, check_in)
            return
    else:
        msg = bot.reply_to(message, 'Возможно, вы ввели лишний символ, попробуйте ещё раз\n'
                                    'Пример: 6-1-2023')
        bot.register_next_step_handler(msg, check_in)
        return


def check_out(message: types.Message):
    """ Функция check_out, ловит ответ пользователя и, если формат даты введён корректно,
        записывает в словарь с данными: информацию о выезде, словарь с информацией по отелям,
        полученный из search_properties (id отеля, ссылку на отель, цену отеля, расстояние от центра).
        Запрашивает необходимость вывода фотографий и вызывает указанную функцию """
    if not message.text.isalpha():
        day, month, year = map(int, message.text.split('-'))
        if day <= 31 and month <= 12 and year <= 2024:
            user_data['check_out'] = message.text
            try:
                hotels_list = search_properties(region=user_data['region_id'], check_in=user_data['check_in'],
                                                check_out=user_data['check_out'], price_sort="PRICE_LOW_TO_HIGH")

                user_data['hotels_list'] = hotels_list

                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                butt_yes = types.KeyboardButton(text='да')
                butt_no = types.KeyboardButton(text='нет')
                keyboard.add(butt_yes, butt_no)
                msg = bot.send_message(message.from_user.id, f'Нужно ли выводить фотографии отеля? ',
                                       reply_markup=keyboard)
                bot.register_next_step_handler(msg, photo)

            except Exception:
                msg = bot.send_message(message.from_user.id, f'Нет доступных отелей')
                bot.send_message(message.from_user.id, 'Если вы хотите просмотреть перечень комманд, нажмите на /start!')
                bot.register_next_step_handler(msg, bot_start)

        else:
            msg = bot.reply_to(message, 'Возможно вы ошиблись с датой, или форматом ввода, попробуйте ещё раз\n'
                                        'Пример: 23-1-2023')
            bot.register_next_step_handler(msg, check_in)
            return

    else:
        msg = bot.reply_to(message, 'Возможно, вы ввели лишний символ, попробуйте ещё раз\n'
                                    'Пример: 23-1-2023')
        bot.register_next_step_handler(msg, check_out)
        return


def photo(message: types.Message):
    """ Функция photo, ловит ответ пользователя и, если ответ утвердительный,
       помечает это в словаре с данными и запрашивает количество фотографий и вызывает указанную функцию.
        В ином случае запрашивает у пользователя количество отелей, которые необходимо вывести в результате
    """
    if message.text == 'да':
        user_data['photo_state'] = True
        msg = bot.reply_to(message, 'Укажите количество фотографий,'
                                    ' которые необходимо вывести в результате (не больше 5)?')
        bot.register_next_step_handler(msg, hotels_photo)
    else:
        user_data['photo_state'] = False
        total_len = len(user_data['hotels_list'])
        msg = bot.reply_to(message, f'Укажите количество отелей, которые необходимо вывести в результате '
                                    f'(не больше {total_len})')
        bot.register_next_step_handler(msg, result)


def hotels_photo(message: types.Message):
    """ Функция hotels_photo, ловит ответ пользователя и, если ответ соответствует критериям ввода,
        записывает в словарь с данными информацию о фотографиях и словарь с ссылками на них, полученный из
        функции search_photos. Затем запрашивает у пользователя количество отелей,
         которые необходимо вывести в результате """
    user_answer = message.text
    if user_answer.isdigit() and int(user_answer) <= 5:
        user_data['numbers_of_photo'] = int(user_answer)
        user_data['hotels_photo'] = search_photos(hotels=user_data['hotels_list'])
        total_len = len(user_data['hotels_list'])
        msg = bot.reply_to(message, f'Укажите количество отелей, которые необходимо вывести в результате '
                                    f'(не больше {total_len})')
        bot.register_next_step_handler(msg, result)
    else:
        msg = bot.reply_to(message, f'Нужно ввести цифру от 1 до 5, попробуйте ещё раз')
        bot.register_next_step_handler(msg, hotels_photo)
        return


def result(message: types.Message):
    """ Функция result, ловит ответ пользователя и, если ответ соответствует критериям ввода,
        записывает в словарь с данными информацию о количестве вывода отелей.
        Так же, записывает в словарь с данными информацию об отелях
        (название отеля, адрес, расположение на карте), полученную из search_details.
        Затем бот отправляет пользователю сообщение со всей информацией по отелю.
        Затем история поиска конкретного пользователя сохраняется в базу данных.
    """
    bot.send_message(message.from_user.id, 'Нужно будет подождать...')
    user_answer = message.text
    if user_answer.isdigit() and int(user_answer) <= len(user_data['hotels_list']):
        user_data['num_of_hotels'] = int(user_answer)
        hotels_info = search_details(user_data['hotels_list'])
        user_data['hotels_information'] = hotels_info
        hotels_names = []
        start_time = datetime.now().strftime("%H:%M - %d.%m.%Y")

        for i in range(user_data['num_of_hotels']):

            name = user_data['hotels_information'][i + 1]['hotel_name']
            address = user_data['hotels_information'][i + 1]['hotel_address']
            view_map = user_data['hotels_information'][i + 1]['hotel_url']
            url = user_data['hotels_list'][i + 1]['hotel_url']
            price = user_data['hotels_list'][i + 1]['hotel_price']
            distance = user_data['hotels_list'][i + 1]['hotel_distance']
            hotels_names.append(name)
            if user_data['photo_state']:
                photos = user_data['hotels_photo'][i + 1]
                photos = photos[:user_data['numbers_of_photo']]
                time.sleep(2)
                bot.send_message(message.from_user.id, f'Cсылка на страницу с отелем: {url}\n'
                                                       f'Название отеля: {name}\n'
                                                       f'Адрес: {address}\n'
                                                       f'Расстояние до центра: {distance} км\n'
                                                       f'Цена за ночь: {price}\n'
                                                       f'Смотреть на карте: {view_map}\n'
                                                       f'Фотографии:')
                for i_photo in photos[:user_data['numbers_of_photo']]:
                    bot.send_photo(message.chat.id, str(i_photo))
            else:
                time.sleep(2)
                bot.send_message(message.from_user.id, f'Cсылка на страницу с отелем: {url}\n'
                                                       f'Название отеля: {name}\n'
                                                       f'Адрес: {address}\n'
                                                       f'Расстояние до центра: {distance} км\n'
                                                       f'Цена за ночь: {price}\n'
                                                       f'Смотреть на карте: {view_map}')
        db_write(db, History, [{'chat_id': message.from_user.id, 'user_command': 'lowprice', 'created_at': start_time,
                                'user_hotels': ', '.join(elem for elem in hotels_names)}])
        bot.send_message(message.from_user.id, 'Если вы хотите просмотреть перечень комманд, нажмите на /help!')
    else:
        msg = bot.reply_to(message, f'Нужно ввести цифру от 1 до {len(user_data["hotels_list"])}, попробуйте ещё раз')
        bot.register_next_step_handler(msg, result)
        return
