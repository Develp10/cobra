"""
Возвращает локальный ip-адрес на всех ОС.
Не требует установки сторонних библиотек.
Код взят со SO.
"""
from socket import socket, AF_INET, SOCK_DGRAM


def local_ipv4() -> str:
    """
    Получаем локальный IP-адрес с помощью установки
    соединения на адрес 10.255.255.255. В ответ получаем
    имя сокета, которое и является адресом.

    :return: возвращает локальный IP-адрес или адрес локальной петли
    в случае возникновения исключения.
    """
    ip = None
    st = socket(AF_INET, SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        st.close()
        return ip
