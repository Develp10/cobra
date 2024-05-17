"""
С помощью данного скрипта выполняется стандартный ping
определенного адреса или доменного имени. Работает так же,
как и стандартный модуль ОС. Не пингует адреса с защитой от
пинга, такие, как, для примера, "codeby.net".
Возможно использование для неглубокой проверки адресов.

Для работы требует установки библиотеки:
pip install ping3
"""
from ipaddress import IPv4Address

from ping3 import ping


def ping_addr(addr: str) -> bool:
    """
    Обычный пинг определенного ip-адреса или домена.
    Оригинальная функция возвращает в случае недоступности
    домена или адреса None. В случае успеха, время, за которое
    выполняется ping.
    В данной функции возвращаются булевы значения в случае
    успеха или неудачи.

    :param addr: ip-адрес или домен (без http(s)).
    :return: True или False в зависимости от результата ping.
    """
    try:
        IPv4Address(addr)
    except Exception:
        if addr.startswith("http"):
            addr = addr.split("/")[2]
            if len(addr.split(".")) > 2:
                addr = ".".join(addr.split(".")[1:])

    try:
        if ping(addr) is not None:
            return True
        return False
    except Exception:
        return False
