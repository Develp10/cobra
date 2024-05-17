"""
Скрипт получает внешний ip-адрес компьютера, с которого
отправляется запрос.
Возможно использовать для тестирования proxy.

Для работы требует установки библиотеки requests:
pip install requests
"""
from requests import get


def public_ip() -> str:
    """
    Получение внешнего ip-адреса путем обращения к api сервиса:
    https://api.ipify.org/

    :return: возвращает полученный внешний ip-адрес.
    """
    try:
        return get('https://api.ipify.org/').text
    except Exception:
        return '127.0.0.1'
