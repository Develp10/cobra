"""
Возвращает ip-адрес роутера(шлюза) по-умолчанию на Linux и Windows машинах.

На некоторых linux-машинах требует установки пакета net-tools, т.к. без него
не работает команда route (пример: Ubuntu):
sudo apt install net-tools
"""

from ipaddress import IPv4Address
from socket import gethostbyname
from platform import system
from subprocess import check_output


def get_host(ip: str) -> str:
    """
    Попытка получения ip-адреса по доменному
    имени. В случае неудачи возвращает из
    функции переданное в нее значение.

    :param ip: доменное имя (или то, что было получено).
    :return: ip-адрес или полученное в функцию значение.
    """
    try:
        sock = gethostbyname(ip)
        return sock
    except Exception:
        return ip


def check_ip(ip: str) -> str:
    """
    Проверка на принадлежность полученного
    значения к ip-адресу. Если полученное значение
    не является ip-адресом, возникает исключение и
    полученное значение передается в функцию для получения
    адреса по доменному имени.
    Если же проверка проходит успешно, адрес возвращается
    из функции.

    :param ip: полученное значение (ip-адрес).
    :return: ip-адрес или значение, которое возвращает функция get_host.
    """
    try:
        IPv4Address(ip)
        return ip
    except Exception:
        return get_host(ip)


def router_ip() -> (str, None):
    """
    Определяется версия ОС, затем, с помощью библиотеки subprocess выполняется
    команда характерная для каждой из ОС, по определению адреса роутера.
    Затем полученное значение отправляется на проверку соответствия адресу.
    Если полученный адрес является IPv4, то он возвращается из функции.
    В случае, если адрес является доменным именем, а такие случаи могут
    быть, полученное имя передается в функцию, где выполняется попытка
    получения ip-адреса по доменному имени. Для примера, если в системе
    используется pfsence.

    :return: возвращает IP-адрес роутера или маршрутизатора, в случае исключения
    возвращает None.
    """
    if system() == "Linux":
        try:
            ip_route = str(check_output('route -n | grep UG', shell=True).decode().split()[1])
            return check_ip(ip_route)
        except Exception:
            return
    elif system() == "Windows":
        try:
            ip_route = check_output('route PRINT 0* -4 | findstr 0.0.0.0', shell=True).decode('cp866'). \
                split()[-3]
            return check_ip(ip_route)
        except Exception:
            return
