"""
Возвращает адрес по переданным координатам.
Координаты необходимо передать в виде списка.
То есть, учитывать возможность передачи пользователем
в скрипт в виде списка через запятую, но для отправки в функцию
обязательно формировать список.

Для работы скрипта необходима установка библиотеки:
pip install geopy
"""
from geopy.geocoders import Nominatim


def get_addr(location=None) -> (str, bool):
    """
    Получение адреса по координатам (обратная геолокация).

    :param location: координаты (широта и долгота).
    :return: адрес локации.
    """
    if location is None:
        return
    try:
        return Nominatim(user_agent="GetLoc").reverse(location).address
    except Exception:
        return
