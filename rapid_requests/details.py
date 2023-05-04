from typing import Dict, Optional
import requests
import json
from config_data.config import RAPID_API_KEY


def details(id: str):
    """
    Функция принимает id отеля, отправляет запрос на url-адрес вместе с необходимыми параметрами
     и HTTP-заголовками и возвращает текстовый объект с информацией по отелю.
     params:
        id(str): id отеля
     :return responce(object): текстовый объект с информацией по отелю
     """
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response


def search_details(hotels: Dict) -> Optional[Dict]:
    """ Функция search_details принимает список отелей и передаёт в функцию details
        id отеля. Функция details в свою очередь возвращает текстовый объект(details_response)
        с информацией по отелю. Если запрос проведён успешно, мы десериализируем этот объект(data)
        Достаём и записываем полученную информацию(название отеля, адрес, расположение на карте)
         в словарь hotels_details
        params: hotels(dict)
        :return hotels_details(dict): возвращает словарь с названием отеля, адресом, расположением на карте.
    """
    hotels_details = {}

    for i in range(len(hotels)):
        details_response = details(hotels[i+1]['property_id'])
        if details_response.status_code == 200:
            data = json.loads(details_response.text)
            for hotel_info, value in data['data']['propertyInfo']['summary'].items():
                if hotel_info == 'name':
                    hotels_details[i + 1] = {'hotel_name': value}

                elif hotel_info == 'location':
                    for elem_name, address in data['data']['propertyInfo']['summary']['location']['address'].items():
                        if elem_name == 'addressLine':
                            hotels_details[i + 1]['hotel_address'] = address
                    for elem_name, url in data['data']['propertyInfo']['summary']['location']['staticImage'].items():
                        if elem_name == 'url':
                            hotels_details[i + 1]['hotel_url'] = url
            result = hotels_details
        else:
            result = {}

        return result


def search_photos(hotels: Dict) -> Optional[Dict]:
    """ Функция search_photos принимает список отелей и передаёт в функцию details
        id отеля. Функция details в свою очередь возвращает текстовый объект(details_response)
        с информацией по отелю. Если запрос проведён успешно, мы десериализируем этот объект
        и работаем со словарём data. Достаём и записываем полученные значения(ссылки на фото)
         в словарь hotels_photos (у каждого отеля свой список фотографий)
     params: hotels(dict)
     :return hotels_photos(dict): возвращает словарь со списком фотографий
    """
    hotels_photos = {}
    for i in range(len(hotels)):
        details_response = details(hotels[i + 1]['property_id'])
        if details_response.status_code == 200:
            data = json.loads(details_response.text)
            hotels_photos[i + 1] = list()
            for i_dict in data['data']['propertyInfo']['propertyGallery']['images']:
                url = i_dict['image']['url']
                hotels_photos[i + 1].append(url)

        else:
            return {}
    return hotels_photos
