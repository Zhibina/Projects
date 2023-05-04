from typing import Union
import requests
import json
from config_data.config import RAPID_API_KEY


def search_locations(city: str) -> Union[str, None]:
    """ Функция принимает параметр city в качестве аргумента и передаёт ключу "q"
        Отправляет запрос на url-адрес вместе с необходимыми параметрами и HTTP-заголовками
        и записывает ответ в переменную response.
        params:
            city(str) - название города
        :return location_search['regionId']. (id региона)
         """
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city,  "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)  # todo: object

    if response.status_code == 200:
        """ Если запрос проведён успешно, мы десериализируем текстовый объект response
                и работаем со словарём data. Достаём id региона и записываем его значение в словарь """
        locations_search = {}
        data = json.loads(response.text)  # десериализация JSON; преобразуем текстовый объект к словарю
        # print(data)

        for i in data['sr']:
            if i['index'] == '0':
                try:
                    locations_search["regionId"] = i['gaiaId']
                except KeyError:
                    print(i['cityId'])
                    locations_search["regionId"] = i['cityId']
        result = locations_search['regionId']

        return result

    else:
        return None
