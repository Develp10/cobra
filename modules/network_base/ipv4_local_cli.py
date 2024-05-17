"""
Скрипт предназначен для получения локального ip-адреса с помощью стандартных средств
операционной системы, в зависимости от того, какая операционная система запущена
в данный момент. Работает на Linux и Windows. Выполняется парсинг вывода стандартных команд.
Данный код требует более детальной проверки на различных дистрибутивах ОС Linux, так как
вывод команды может немного отличатся. Проверен на: Kali, Ubuntu, Mint.
Для Windows, также требуется проверка на версиях ОС младше и старше 10 версии. В данный
момент протестирован на Windows 10 Pro.

Установки дополнительных библиотек для работы не требует.
"""
from platform import system
from subprocess import check_output


def local_ipv4() -> (str, None):
    """
    Выполняется определение ОС. В зависимости от этого выполняется
    команда с помощью subprocess.check_output для получения локального
    ip-адреса. Парситься и возвращается вывод команд. Если в процессе
    выполнения команды поднимается исключение, возвращается None.
    :return: строковый параметр - локальный ip-адрес или None.
    """
    if system() == "Linux":
        try:
            return check_output('ip -h -br a | grep UP', shell=True).decode().split()[2].split("/")[0]
        except Exception:
            return

    elif system() == "Windows":
        try:
            net_set = check_output("wmic nicconfig get IPAddress, IPEnabled /value"). decode("cp866").strip().\
                split("\r\r\n")

            text = ""
            for net in net_set:
                if net.strip() == "":
                    text = f"{text}|"
                else:
                    text = f"{text}~{net.strip()}"
            text = text.strip().split("||")
            for tx in text:
                if tx.split("~")[-1].split("=")[1] != "TRUE":
                    continue
                for item in tx.split("~"):
                    if item.strip() == "":
                        continue
                    if item.strip().split("=")[0] == "IPEnabled":
                        continue
                    if item.strip().split("=")[1] != "":
                        if item.strip().split("=")[0] == "IPAddress":
                            return item.strip().split("=")[1].split(",")[0].replace('"', '').replace("{", "")
        except Exception:
            return
