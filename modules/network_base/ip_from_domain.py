"""
Возвращает ip-адрес домена, если таковой удается получить.
Не требует для работы сторонних библиотек. Принимает в
качестве параметров строку с адресом, доменом или ip.
Установки сторонних библиотек не требуется.
"""
from ipaddress import IPv4Address
from socket import gethostbyname, gaierror


def ip_from_domain(domain: str) -> (str, None):
    """
    Производиться обработка поступившего от пользователя адреса.
    Удаление http(s) для дальнейшего получения ip домена.
    Запрашивается ip-адрес, который возвращается из функции,
    если его удалось получить. Если нет, возвращается None.

    :return: возвращает ip-адрес или None, если его не удалось получить.
    """
    try:
        IPv4Address(domain)
        return domain
    except Exception:
        if domain.startswith("http"):
            domain = domain.split("/")[2]
            if len(domain.split(".")) > 2:
                domain = ".".join(domain.split(".")[1:])

    try:
        ip_domain = gethostbyname(domain)
        return ip_domain
    except gaierror:
        return
