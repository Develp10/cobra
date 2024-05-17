"""
Скрипт возвращает результат парсинга выполнения стандартных
команд Linux и Windows. Возвращается словарь с базовыми
параметрами сетевого интерфейса используемого по-умолчанию.
К базовым параметрам здесь относятся: имя сетевого интерфейса,
локальные ip-адреса v4 и v6, адрес шлюза по-умолчанию,
mac-адрес сетевого интерфейса.

На некоторых linux-машинах требует установки пакета net-tools,
т.к. без него не работает команда route (пример: Ubuntu):
sudo apt install net-tools

Кроме вышеуказанного пакета, сторонних библиотек
для работы скрипта не требуется.
"""

from ipaddress import IPv4Address
from socket import gethostbyname
from platform import system
from subprocess import check_output


def network_param() -> dict:
    """
    Получаем базовые параметры сети, такие как:
    - имя сетевого интерфейса по-умолчанию;
    - адреса: IPv4 и IPv6;
    - адрес шлюза по-умолчанию;
    - mac-адрес сетевого интерфейса по-умолчанию.
    :return: словарь с вышеуказанными параметрами.
    """
    if system() == "Linux":
        try:
            com_run = check_output('ip -h -br a | grep UP', shell=True).decode()
            default_interface = com_run.split()[0].strip()
            ipv4 = com_run.split()[2].strip().split("/")[0]
            ipv6 = com_run.split()[3].strip().split("/")[0]
        except Exception:
            com_run, default_interface, ipv4, ipv6 = None, None, None, None
        try:
            router_ip = str(check_output('route -n | grep UG', shell=True).decode().split()[1])
            try:
                IPv4Address(router_ip)
            except Exception:
                pass
            else:
                try:
                    ip = gethostbyname(router_ip)
                    router_ip = ip
                except Exception:
                    pass
        except Exception:
            router_ip = None
        try:
            mac_address = check_output(f'ifconfig {default_interface} | grep "ether"', shell=True).decode(). \
                split()[1]
        except Exception:
            mac_address = None

        return {"Default Interface": default_interface, "IPv4 address": ipv4, "IPv6 address": ipv6,
                "Router ip-address": router_ip, "MAC-address": mac_address}
    elif system() == "Windows":
        try:
            net_set = check_output(
                "wmic nicconfig get IPAddress, MACAddress, IPEnabled, SettingID, DefaultIPGateway /value"). \
                decode("cp866"). strip().split("\r\r\n")

            default_interface, ipv4, ipv6, router_ip, mac_address = None, None, None, None, None
            text = ""
            for net in net_set:
                if net.strip() == "":
                    text = f"{text}|"
                else:
                    text = f"{text}~{net.strip()}"
            text = text.strip().split("||")
            for tx in text:
                if tx.split("~")[-3].split("=")[1] != "TRUE":
                    continue
                for item in tx.split("~"):
                    if item.strip() == "":
                        continue
                    if item.strip().split("=")[0] == "IPEnabled":
                        continue
                    if item.strip().split("=")[1] != "":
                        if item.strip().split("=")[0] == "SettingID":
                            default_interface = item.strip().split("=")[1]
                        if item.strip().split("=")[0] == "DefaultIPGateway":
                            router_ip = item.strip().split("=")[1].replace("{", "").replace("}", "").replace('"', '')
                        if item.strip().split("=")[0] == "MACAddress":
                            mac_address = item.strip().split("=")[1]
                        if item.strip().split("=")[0] == "IPAddress":
                            ipv4 = item.strip().split("=")[1].split(",")[0].replace('"', '').replace("{", "")
                            ipv6 = item.strip().split("=")[1].split(",")[1].replace('"', '').replace("}", "")
        except Exception:
            default_interface, ipv4, ipv6, router_ip, mac_address = None, None, None, None, None
        return {"Default Interface": default_interface, "IPv4 address": ipv4, "IPv6 address": ipv6,
                "Router ip-address": router_ip, "MAC-address": mac_address}
