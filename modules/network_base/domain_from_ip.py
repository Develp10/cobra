"""
Возвращает доменное имя в случае его нахождения,
или ptr запись arpa.
Для работы установки сторонних библиотек не требуется.
"""
from ipaddress import IPv4Address
from _socket import gethostbyaddr


def domain_ip(ip) -> (str, None):
    """
    Получение домена по ip-адресу.
    Работает не всегда корректно. Зачастую возвращается
    reverse dns.

    :return: домен или False в случае неудачи.
    """
    try:
        IPv4Address(ip)
    except Exception:
        return
    try:
        return gethostbyaddr(ip)[0]
    except Exception:
        return
