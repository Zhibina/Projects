from typing import Dict, Optional
import json
import requests
from config_data.config import RAPID_API_KEY


def search_properties(region: str, check_in: str, check_out: str,
                      price_sort: str, max_price: int =150, min_price: int =100) -> Optional[Dict]:
    """ Функция принимает id региона, дату заселения, дату выселения и параметр сортировки
    Отправляет запрос на url-адрес вместе с необходимыми параметрами и HTTP-заголовками
    и записывает ответ в переменную response.

    params:

        region(str): id региона
        check_in(str): дата заселения
        check_out(str): дата выселения
        price_sort(str): параметр сортировки

    :return hotels(dict): словарь с информацией по отелю.
    """
    day_in, month_in, year_in = map(int, check_in.split('-'))
    day_out, month_out, year_out = map(int, check_out.split('-'))

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": region},
        "checkInDate": {
            "day": day_in,
            "month": month_in,
            "year": year_in
        },
        "checkOutDate": {
            "day": day_out,
            "month": month_out,
            "year": year_out
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": price_sort,
        "filters": {"price": {
                "max": max_price,
                "min": min_price
            }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        """ Если запрос проведён успешно, мы десериализируем текстовый объект response
        и работаем со словарём data. Достаём и записываем полученные значения
        (id отеля, ссылку на отель, цену отеля, расстояние от центра) в словарь hotels"""
        hotels = {}
        data = json.loads(response.text)
        for index, i_property in enumerate(data['data']['propertySearch']['properties']):
            for hotel_info, value in i_property.items():
                if hotel_info == 'id':
                    hotels[index + 1] = {'property_id': value}
                    hotels[index + 1]['hotel_url'] = 'https://www.hotels.com/ho' + str(value)
            hotels[index + 1]['hotel_price'] = i_property['price']['lead']['formatted']
            hotels[index + 1]['hotel_distance'] = i_property['destinationInfo']['distanceFromDestination']['value']
        return hotels
    else:
        return dict()
