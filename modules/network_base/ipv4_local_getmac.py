"""
Возвращает локальный ip-адрес на Linux и Windows машинах.
К сожалению, обойтись стандартными библиотеками в данном
случае не удалось.

Для работы скрипта необходима установка библиотек:
pip install getmac netifaces

Из-за сложностей компилирования библиотеки netifaces
в ОС Windows установка стандартными способами оканчивается
ошибкой. Для установки данной библиотеки необходимо скачать
ее скомпилированную версию с сайта: https://www.lfd.uci.edu/~gohlke/pythonlibs/#netifaces,
после чего установить командой:
pip install modul_name.whl

Для примера: pip install netifaces-0.11.0-cp39-cp39-win_amd64.whl

Однако, на данный момент на сайте присутствуют библиотеки только для python 3.9.
Установка на python более поздних версий окончиться неудачей.
В Linux подобной проблемы не наблюдается. Все библиотеки устанавливаются стандартно.
Есть возможность скачать из репозитория PyPi архив и создать пакет самостоятельно.
"""

from platform import system
from subprocess import check_output

from getmac.getmac import get_mac_address
from netifaces import ifaddresses, AF_INET


def local_ipv4() -> str:
    """
    Выполняется определение версии ОС. В зависимости от этого
    запускается код по получению локального ip-адреса.

    Для ОС Linux название сетевого интерфейса получаем с помощью
    модуля _get_default_iface_linux библиотеки getmac.
    Затем, полученное имя передается в функцию ifaddresses библиотеки
    netifaces, откуда и забирается вывод.

    Для ОС Windows имя сетевого интерфейса получаем не совсем стандартным
    способом. Для начала, с помощью функции get_mac_address библиотеки getmac
    получаем mac-адрес интерфейса по-умолчанию. Затем, чтобы получить имя сетевого
    интерфейса выполняем команду getmac и парсим вывод, забирая только те данные
    в которых есть mac-адрес полученный ранее. Далее, полученное имя интерфейса
    передаем в функцию ifaddresses и забираем вывод.

    :return: возвращает локальный ip-адрес или адрес локальной петли в случае ошибки
    получения данных.
    """
    if system() == "Linux":
        try:
            return ifaddresses(_get_default_iface_linux()).setdefault(AF_INET)[0]['addr']
        except Exception:
            return '127.0.0.1'
    elif system() == "Windows":
        try:
            mac_address = get_mac_address().replace(":", "-").upper()
            interface_temp = check_output('getmac /FO csv /NH /V', shell=False).decode('cp866').split("\r\n")
            for face in interface_temp:
                if mac_address in face:
                    return ifaddresses(face.split(",")[-1].replace('"', '').split("_")[-1]). \
                        setdefault(AF_INET)[0]['addr']
        except Exception:
            return '127.0.0.1'
