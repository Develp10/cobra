# Кобра: создаем OSINT инструмент на Python, часть 1
Итак, каждый программист желает все автоматизировать - и не только программист. В этой статье мы рассмотрим создание OSINT-инструмента на Python.

Я хочу предупредить, что все показано в целях ознакомления, данные человека не подлежат хранению или распространению без соответствующего разрешения.

В этой статье мы создадим инструмент для:

 + Получения информации об IP адресе
 + Получения информации об номере телефона
 + Получение информации, есть ли IP в черных листах DNS
 + Парсер всех ссылок с сайта
 + Сканер портов
 + SYN-сканер портов
 + Сканер SQL инъекций
 + Сканер XSS уязвимостей
 + Генератор фейкового User-Agent
 + Скрипт для изменения mac-адреса

Эта статья - **первая часть**, здесь мы рассмотрим минимум, а в следующей части доделаем код, улучшим его и сделаем полноценный CLI-инструмент.

Данная статья ориентирована на продвинутых разработчиков, которые уже умеют писать и читать python-код.

Для всего этого нам нужен будет Python >3.9, Linux и пакетный менеджер pip.

Весь исходный код доступен по [ссылке](https://github.com/AlexeevDeveloper/cobra). Репозиторий локализирован на английский язык, в директории `/docs/ru` есть markdown-версия статьи.

# Создаем рабочее окружение
Никогда вам не советую устанавливать пакеты в саму систему. Для того чтобы работать над каждым проектом отдельно (дабы не возникало ошибок с пакетами и библиотеками) надо создавать _виртуальные окружения_.

Для того, чтобы создать виртуальное окружение, нам потребуется всего лишь одна команда:

```bash
python3 -m venv <название виртуального окружения>
# Например, создание виртуального окружения venv
python3 -m venv venv
```

После ввода данной команды у вас в текущем проекте будет создана новая директория - это и будет виртуальное окружение.

Но это еще не все - нам предстоит активировать его командой:

```bash
source venv/bin/activate
# Или, если у вас fish:
source venv/bin/activate.fish
```

И вот теперь мы можем спокойно работать с проектом и устанавливать пакеты. Для деактивации и выхода из окружения можно использовать команду `deactivate`.

# Установка зависимостей
Для начала, давайте установим пакет `whois`. Он потребуется для того, чтобы мы могли узнать информацию об IP адресах.

```bash
sudo pacman -S whois  			# Arch
sudo apt install whois 			# Debian/Ubuntu
sudo dnf install whois 			# Fedora
sudo epm install whois 			# Alt
```

После активации нашего окружения, можно установить python-пакеты. Список нужных нам можно получить по [ссылке](https://github.com/AlexeevDeveloper/cobra) в файле requirements.txt. Просто скачиваете его в проект и выполняете следующию команду:

```bash
pip3 install -r requirements.txt
```

Этим мы установили нужные нам зависимости. Теперь можно начать разработку!

# Архитектура проекта
Давайте создадим архитектуру нашего инструмента:

 + Директория `core` - базовый функционал для самого инструмента
 + Директория `modules` - главная папка всего проекта, здесь мы будем хранить модули для работы.
  + `anonymity` - модуль анонимности, безопасности. Небольшой, чаще всего вспомогательный. Есть пока два компонента - генерация фейкового юзер-агента (`fakeuseragent.py`) и изменение MAC-адреса устройства (`machanger.py`)
  + `network_base` - вспомогательно-информационный модуль. Содержит информацию о сети, IP и портах. Один из самых больших модулей. Содержит следующие файлы: адрес из гео-координат, домен из IP, IP из домена, небольшие программы для работы с IPv4, ваш публичный IP, параметры сети, скрипт для пинга адреса, какой сервис на порту и т.д.
  + `osint` - модуль, как не странно, для OSINT и поиска информации. Здесь уже содержится прокси-файл для взаимодействия с модулем network_base, а также скрипты для получения информации об ip и номере телефона.
  + `scanners` - модуль для сканеров, как понятно из названия. Здесь есть сканер IP на наличие в черных списках DNS, парсер ссылок с сайта, сканер портов, поиск SQL-Injection и XSS уяизвимостей.
 + Файл `main.py` - главный файл кода в корневом каталоге проекта.

Итак, в репозитории директория core является хранилищем трех файлов - это

 + `highlight_schemes.py` - цветовые схемы Pygments.
 + `logger.py` - файл с классом логгера, дебаггера объектов.
 + `style.py` - файл с цветами, для того чтобы делать вывод красивее.

К сожалению, эти файлы мы не будем затрагивать - это совершенно другая тема. Если вы хотите, следующая статья будет об создании продвинутых CLI-программ на Python. А пока продолжим.

В репозитории modules есть огромное количество файлов и каталогов, я разберу здесь большую часть.

# Создание модулей
Займемся созданием модулей. Начнем с модуля анонимности

# Генерация фейкового User-Agent
Для этого мы будем использовать библиотеку `fake-useragent`.

```python
from fake_useragent import UserAgent


def generate_useragent() -> str:
    fua = UserAgent()

    return str(fua.random)

```

Здесь всего лишь одна функция - генерации случайного юзер-агента.

# Изменение MAC-адреса
Для этого нам не нужны будут дополнительные библиотеки. Но вам возможно нужно будет установить набор инструментов `net-tools`. Этот набор содержит в себе утилиту ifconfig, аналог ipconfig в Windows, который нам нужен будет для управления сетями.

```python
import re
import subprocess
from random import choice


def ifconfig():
    """Возвращаем вывод команды ifconfig"""
    output = subprocess.check_output(["sudo", 'ifconfig'])

    return str(str(output.decode('utf-8')).replace(r'\n', '\n'))


def change_mac(interface: str, new_mac_address: str) -> None:
    """Функция для изменения MAC-адреса при помощи утилиты ifconfig

    Аргументы:
     + interface: str - название интерфейса (ex. wlan0, wlp1s0, wlp3s0, eth)
     + new_mac_address - значение нового mac-адреса"""
    print(f'[+] Выключение {interface}')
    subprocess.call(["doas", "ifconfig", interface, "down"])
    print(f'[+] Замена MAC-адреса {interface} на {new_mac_address}')
    subprocess.call(["doas", 'ifconfig', interface, 'hw', 'ether', new_mac_address])
    print(f'[+] Включение {interface}')
    subprocess.call(["doas", "ifconfig", interface, "up"])


def get_random_mac_address() -> str:
    """Функция генерации и получения случайного mac-адреса.
    У нас есть словарь с числами от 0 до 9, и латинских букв от a до f, а также начало
    нового mac-адреса (00). После мы проходимся в итерационном цикле и добавляем 5 раз еще 
    по паре символов, а после возвращаем

    Возвращает:
     + str - новый mac-адрес"""
    characters = list("1234567890abcdef")
    random_mac_address = "00"

    for i in range(5):
        random_mac_address += ':' + choice(characters) + choice(characters)

    return random_mac_address


def get_current_mac(interface: str):
    """Получаем текущий MAC-адрес при помощи утилиты ifconfig"""
    output = subprocess.check_output(["doas", "ifconfig", interface])

    return re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(output)).group(0)


def main(interface: str):
    new_mac_address = get_random_mac_address()

    try:
        current_mac = get_current_mac(interface)
    except subprocess.CalledProcessError as ex:
        print(f'[!] Произошла ошибка. Скорее всего {interface} не существует')
        print(f' !-> {ex}')
        return

    print(f'[+] Текущий MAC-адрес: {current_mac}')
    print(f'[+] Замена MAC-адреса на {new_mac_address}')
    change_mac(interface, new_mac_address)

```

# Модуль `network_base`
Этот модуль, как я уже говорил, нужен для работы с сетью. Но весь код занимает слишком много места, поэтому посмотреть вы его можете по [ссылке](https://github.com/AlexeevDeveloper/cobra/tree/main/modules/network_base).

Обязательно советую использовать этот код, ибо он требуется для получения информации об IP. Можете просто скопировать код и изучить его, он обильно документирован.

Там вы увидите множество файлов - все они пригодятся.

# Модуль OSINT
Теперь займемся самим поиском информации по открытым источникам. Займемся файлом `ip.py` - он поведует нам некоторую информацию об IP адресе.

```python
import os
import requests


def get_info_about_ip(ipaddr: str, fua: str) -> tuple:
    """Получаем информацию об IP адресе

    Аргументы:
     + ipaddr: str - IP адрес
     + fua: str - фейковый юзер-агент"""
    result = str()

    try:
        # Отправляем запрос
        headers = {
            'User-Agent': fua
        }
        info_data = requests.get(f'https://ipinfo.io/{ipaddr}/json', headers=headers).json()
    except Exception as ex:
        # При ошибке возвращаем саму ошибку.
        return ex

    # Получаем информацию об IP
    whois_info = os.popen(f'whois {ipaddr}').read().strip()

    result += f'IP: {info_data.get("ip")}\n'
    result += f'City: {info_data.get("city")}\n'
    result += f'Region: {info_data.get("region")}\n'
    result += f'Country: {info_data.get("country")}\n'
    result += f'Hostname: {info_data.get("hostname")}\n'
    result += f'JSON data: {info_data}\n'
    result += f'WhoIS: {whois_info}\n'

    # возвращаем результат
    return result
```

Следующий шаг - компонент `netlib.py`. Он как раз и будет неким посредником между модулем OSINT и модулем network_base.

```python
import modules.network_base.ipv4_local_cli as ipv4_cli
import modules.network_base.ipv4_local_getmac as ipv4_gm
import modules.network_base.ipv4_local_sock as ipv4_sock

import modules.network_base.router_ip as getaway

import modules.network_base.network_params as net_param

import modules.network_base.ip_from_domain as ip_domain
import modules.network_base.domain_from_ip as domain_ip
import modules.network_base.service_on_port as serv_port

import modules.network_base.my_public_ip as public_ip
import modules.network_base.ping_address as ping_addr
import modules.network_base.geolocation_ip as geo_ip
import modules.network_base.addr_from_geo as addr_geo


def url_info(url):
    """Информация об URL.

    URL автоматически ретранслируется в IP"""

    # Пинг адреса
    print(f'Ping domain of address: {ping_addr.ping_addr(ip_domain.ip_from_domain(f"{url}"))}')
    # Координаты
    print(f"Coords by IP address: {geo_ip.geo_ip(domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}')))}")
    # Физический адрес по координатам
    print(f"Physical address by coords: "
        f"{addr_geo.get_addr(geo_ip.geo_ip(domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}'))))}")
    # IP из домена
    print(f"IP-address of domain {url}: {ip_domain.ip_from_domain(f'{url}')}")
    # Домен из IP
    print(f"Domain name {url} by IP: {domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}'))}")


def ip_info(ip: str) -> str:
    """Информация об IP"""
    print(f'Ping domain or address: {ping_addr.ping_addr(ip)}')
    print(f"Coords by IP: {geo_ip.geo_ip(ip)}")
    print(f"Geo Addr Coords by IP: {addr_geo.get_addr(geo_ip.geo_ip(domain_ip.domain_ip(ip)))}")
    print(f"Domain name: {domain_ip.domain_ip(ip)}")


def check_network():
    """Проверяем сетевые параметры"""

    # Локальный IP
    print(f'Local IP (cli): {ipv4_cli.local_ipv4()}')
    print(f'Local IP (gm): {ipv4_gm.local_ipv4()}')
    print(f'Local IP (sock): {ipv4_sock.local_ipv4()}')

    # IP шлюза
    print(f'IP router: {getaway.router_ip()}')

    # Параметры сети
    print(f'Network interface parameters:\n{net_param.network_param()}')

    # Название сервиса работающего на 80 порту
    print(f'Name of service work on port 80: {serv_port.type_port(80)}')

    # Публичный IP
    print(f'Public IP: {public_ip.public_ip()}')
```

Следующий компонент - `phone.py`, который отвечает за небольшой поиск информации об номере телефона.

```python
import requests


def get_info_phonenumber(phonenumber, fua):
    """Получение информации о номере телефона

    Аргументы:
     + phonenumber - номер телефона
     + fua - фейковый юзер-агент"""
    result = ''
    try:
        # Делаем запрос к API
        url = f"https://htmlweb.ru/geo/api.php?json&telcod={phonenumber}"
        headers = {
            'User-Agent': fua
        }
        info_data = requests.get(url, headers=headers).json()
    except Exception as ex:
        return ex

    result += f'Country: {info_data["country"]["name"]}\n'
    result += f'Region: {info_data["region"]["name"]}\n'
    result += f'Subregion: {info_data["region"]["okrug"]}\n'
    result += f'Operator: {info_data["0"]["oper"]}\n'
    result += f'Location: {info_data["country"]["location"]}\n'

    return result
```

После этого можно заняться следующим компонентом - `whois_information.py`:

```python
#!venv/bin/python3
import socket
import time
from ipaddress import IPv4Address, AddressValueError
from datetime import datetime
import ipwhois
import whois


def ipwhois_info(ip: str):
    """Информация о IP по IPWhois

     + ip: str - IP адрес"""
    results = ipwhois.IPWhois(ip).lookup_whois()
    print(results)
    print("\n")


def whois_info(ip):
    """Информация о IP по WhoIs

     + ip: str - IP адрес"""
    results = whois.whois(ip)
    print(results)


def ianna(ip):
    """Информация о IP через whois.iana.org

     + ip: str - IP адрес"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("whois.iana.org", 43))
    s.send((ip + "\r\n").encode())
    response = b""
    
    while True:
        data = s.recv(4096)
        response += data
        if not data:
            break
    
    s.close()
    whois = ''
    
    for resp in response.decode().splitlines():
        if resp.startswith('%') or not resp.strip():
            continue
        elif resp.startswith('whois'):
            whois = resp.split(":")[1].strip()
            break
    
    return whois if whois else False


def get_whois(ip, whois):
    """Получения информации о IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((whois, 43))
    s.send((ip + "\r\n").encode())
    response = b""
    
    while True:
        data = s.recv(4096)
        response += data
        if not data:
            break
    
    s.close()
    whois_ip = dict()
    num = 0
    
    for ln in response.decode().splitlines():
        if ln.strip().startswith("%") or not ln.strip():
            continue
        else:
            if ln.strip().split(": ")[0].strip() in ['created', 'last-modified']:
                dt = datetime.fromisoformat(ln.strip().split(": ")[1].strip()).strftime("%Y-%m-%d %H:%M:%S")
                whois_ip.update({f'{ln.strip().split(": ")[0].strip()}_{num}': dt})
                num += 1
            else:
                whois_ip.update({ln.strip().split(": ")[0].strip(): ln.strip().split(": ")[1].strip()})
    
    return whois_ip if whois_ip else False


def validate_request(ip):
    """Проверка IP

     + ip - IP адрес"""
    try:
        IPv4Address(ip)
        if whois := ianna(ip):
            time.sleep(1)
            if info := get_whois(ip, whois):
                print(info)
            else:
                print("Не была получена информация")
        else:
            if info := get_whois(ip, 'whois.ripe.net'):
                print(info)
            else:
                print("Не была получена информация")
    except AddressValueError:
        print("IP адрес не валидный")
    except ConnectionResetError as ex:
        print(ex)
```

После этого давайте займемся предпоследним компонентом модуля OSINT - `virus_total.py` для анализа бинарников на вирусы, трояны и другие малвари.

Для начала вам потребуется авторизоваться на [сайте Virus Total](https://www.virustotal.com/gui/). После активации аккаунта, откройте меню пользователя и перейдите в секцию API Key. Ниже вы увидете сам API ключ:

![](https://habrastorage.org/webt/dv/96/ap/dv96ap-voywnjsvk1no8hscekic.png)

Не забудьте про ограничения бесплатного API-ключа:

 + Частота запросов - 4 поиска / минута
 + Дневная квота - 500 поисков / день
 + Месячная квота - 15.5 K поисков / месяц

После просто скопируйте и вставьте в код. Есть разные практики хранить важные ключи в коде. Давайте рассмотрим три способа:

1. Первый и простой способ. Просто вставить ключ прямо в коде

```python
APIKEY='123456abcdef'

# Здесь ваш код
# ...
```

Но я категорически не советую так делать. Если вы забудете удалить ваш ключ, то он может оказаться в руках других людей. Они смогут получить доступ к вашему проекту, боту, аккаунта и т.д., в зависимости от возможностей API. Поэтому так делайте только в локальных проектах (да и даже так лучше не делать по стилю кода).

2. Создать файл настроек/конфигов, например `settings.py` и в нем хранить все важные ключи, а после импортировать в проект. Намного лучше чем 1 способ, но проблемы с безопасностью также остаются.

3. Переменные окружения. Безопасный способ, мы храним API не в коде, а в переменных окружения. Этот способ мы и будем использовать.

Вам будет надо установить пакет `python-dotenv`:

```bash
pip install python-dotenv
```

И после создайте в корневом каталоге файл `.env`, и в него вставьте следующий код:

```bash
VIRUS_TOTAL_KEY = "ваш ключ"
```

После этого давайте немного изменим концепцию, и создадим микро-антивирус. Он будет сперва проверять хеш файла в базе сигнатурах. Да, просто сопоставлять, и это не будет стоять рядом даже с самыми плохими антивирусами - ведь стоит добавить в бинарник малваря хотя-бы один байт, даже если это будет 0, то уже наш антивирус ничего не заподозрит. Но если малварь и пройдет сигнатурный анализ, то дальше его ждет Virus Total!

И еще, мы не будем сами посылать запросы, и парсить результат, мы будем использовать библиотеку [vt-py](https://virustotal.github.io/vt-py/index.html).

А также для локальной проверки файлов нам нужны будут сигнатуры. Собрал я их в каталоге res, доступный по [ссылке](https://github.com/AlexeevDeveloper/cobra/tree/main/res).


```python
import os
import json
import requests
from dotenv import load_dotenv
import os
from time import perf_counter
from hashlib import sha256, sha1, md5
from colorama import Fore, Style
import vt
import json

# загружаем переменные окружения
load_dotenv()

# получаем API-ключ
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_KEY")

# Сигнатуры
signature_resources = ['res/signatures.txt', 'res/signatures2.txt',
                        'res/signatures3.txt', 'res/signatures4.txt']

# для своих требований, туда можно поместить хэши зловредов, которых нету в обычных списках сигнатур. А также описание и название.
signature_resource_info = 'res/signatures_info.json'


def add_signature(new_signature: dict) -> None:
    """Добавление сигнатуры в базу"""
    with open(signature_resource_info, 'r') as file:
        signatures_info = json.load(file)

    for signature in new_signatures:
        signatures_info['name'] = new_signatures['name']
        signatures_info['desc'] = new_signatures['desc']
        signatures_info['date'] = new_signatures['date']

    with open(signature_resource_info, 'a') as file:
        json.dump(signatures_info, file, indent=4)

    return None


def rewrite_signatures(signatures: dict) -> bool:
    """Перезапись БД сигнатур"""
    try:
        with open(signature_resource_info, 'w') as file:
            json.dump(signatures, file, indent=4)
    except Exception as e:
        return False
    else:
        return True


def get_info_signature(signature: str) -> str:
    """Получение информации об сигнатуре из БД"""
    with open(signature_resource_info, 'r') as file:
        signatures_info = json.load(file)

    try:
        signature_info = f'''Сигнатура: {signature}
Название угрозы: {signatures_info[signature]["name"]}
Описание угрозы: {signatures_info[signature]["desc"]}
Дата обнаружения угроза: {signatures_info[signature]["date"]}'''
    except IndexError:
        signature_info = f'По сигнатуре {signature} еще нету информации в наших базах данных'
    finally:
        return signature_info


def scan_file(filename: str, delete_file: bool, signature_resources: list, VT_API_KEY: str) -> None:
    """Сканируем файл

     + filename: str - путь до файла
     + delete_file: bool - удалять ли файл
     + signature_resources: list - список ресурсов сигнатур
     + VT_API_KEY: str - API ключ Virus Total"""
    result = f'Сканируем {filename} на наличие угроз...\n'

    try:
        print('Load singatures...')
        start = perf_counter()
        shahash = sha256()
        sha1hash = sha1()
        md5hash = md5()

        # Получаем хэши
        with open(filename, 'rb') as file:
            while True:
                data = file.read()
                if not data:
                    break
                shahash.update(data) # sha256
                sha1hash.update(data) # sha1
                md5hash.update(data) #md5

            result1 = shahash.hexdigest()
            result2 = sha1hash.hexdigest()
            result3 = md5hash.hexdigest()
            result += f'Проверяем наличие хешей "{result1}", "{result2}", "{result3}" (sha256, sha1, md5) в сигнатурах...\n'

        # Читаем сигнатуры
        with open(signature_resources[0], 'r') as r:
            signatures = list(r.read().split('\n'))

        with open(signature_resources[1], 'r') as r:
            for sign_hash2 in list(r.read().replace(';', '').split('\n')):
                signatures.append(sign_hash2)

        with open(signature_resources[2], 'r') as r:
            for sign_hash3 in list(r.read().replace(';', '').split('\n')):
                signatures.append(sign_hash3)

        with open(signature_resources[3], 'r') as r:
            for sign_hash4 in list(r.read().replace(';', '').split('\n')):
                signatures.append(sign_hash4)

        result += f'''Сканирование {filename} на Virus Total...\n'''

        print('Loading Virus Total...')
        client = vt.Client(VT_API_KEY)

        # анализ файла
        with open(filename, "rb") as f:
            analysis = client.scan_file(f, wait_for_completion=True)
            file = client.get_object(f"/files/{result1}")
            stats = file.last_analysis_stats
        
            result += f'VirusTotal: {filename}\t size: {file.size} bytes\n'
            result += f'Безвредный: {stats["harmless"]}\n'
            result += f'Неподдерживаемый тип: {stats["type-unsupported"]}\n'
            result += f'Подозрительный: {stats["suspicious"]}\n'
            result += f'Отказ: {stats["failure"]}\n'
            result += f'Злонамеренный: {stats["malicious"]}\n'
            result += f'Безопасный: {stats["undetected"]}\n'

        print('Get final info...')

        if result1 in signatures or result2 in signatures or result3 in signatures:
            end = perf_counter()
            total = end - start
            result += f'Найдена угроза в файле {filename} (поиск по сигнатурам)\n'

            # получаем информацию о файле, если он есть в сигнатурах
            if result in signatures:
                info = get_info_signature(result)
                result += f'Информация: {info}\n'
            elif result2 in signatures:
                info = get_info_signature(result2)
                result += f'Информация: {info}\n'
            elif result3 in signatures:
                info = get_info_signature(result3)
                result += f'Информация: {info}\n'

            # удаление файла
            if delete_file:
                os.remove(filename)
                result += f'[!] Файл {filename} удален!\n'

            result += f'Время работы: {(total):.07f}s\n'
        else:
            end = perf_counter()
            total = end - start
            result += 'Угроз не найдено\n'
            result += f'Время работы: {(total):.07f}s\n'
    except FileNotFoundError:
        result += f'[!] Файл не найден\n'
    except PermissionError:
        result += f'[!] Ошибка прав доступа к файлу\n'

    print('End')

    return result


res = scan_file('<любой файл>', False, signature_resources, VIRUS_TOTAL_API_KEY)
print(res)
```

Вот и все - при запуске этого скрипта мы можем спокойно анализировать файлы на Virus Total.

# Модуль `scanners`
Модуль всеразличных сканеров и парсеров. ПОка есть 6 - поиск IP в черных списках DNS, парсер ссылок, сканер портов, сканер на SQL-Injection и XSS уязвимости. А также есть еще детектор ARP-спуфинга и сканер сессий meterpreter для Windows.

Займемся детектором ARP спуфинга. ARP-spoofing — разновидность сетевой атаки типа MITM, применяемая в сетях с использованием протокола ARP. В основном применяется в сетях Ethernet. Атака основана на недостатках протокола ARP.

Нам нужен будет модуль [scapy](https://scapy.readthedocs.io/).

```python
from scapy.all import sniff


class ARPSpoofingDetector:
    def __init__(self):
        self.IP_MAC_Map = {}

    def process_packet(self):
        src_IP = packet['ARP'].psrc
        src_MAC = packet['Ether'].src

        if src_MAC in self.IP_MAC_Map.keys():
            if self.IP_MAC_Map[src_MAC] != src_IP :
                try:
                    old_IP = self.IP_MAC_Map[src_MAC]
                except:
                    old_IP = "Неизвестный"

                message = f'''ARP атака замечена
Это возможно со стороны машины с IP адресом {old_IP} для {src_IP}'''

                return message
            else:
                self.IP_MAC_Map[src_MAC] = src_IP

    def sniffing(self):
        # "Нюхаем" пакеты
        sniff(count=0, filter="arp", store=0, prn=self.process_packet)


arpspoof_detector = ARPSpoofingDetector()
arpspoof_detector.sniffing()
```

Следующий шаг - сканер meterpreter сессий для Windows 7 и 10.

```python
import re
import subprocess
from typing import List, Dict

WIN_7_SIGNATURE = ["WINBRAND.dll", "WINHTTP.dll", "webio.dll", "SspiCli.dll", "cscapi.dll"]
WIN_10_SIGNATURE = ["rsaenh.dll", "netapi32.dll", "wkscli.dll", "psapi.dll", "cscapi.dll"]

REG_FOR_WINDOWS_VERSION = r'(?:Windows\s+)(\d+|XP|\d+\.\d+)'
REG_FOR_EXE_PROCESSES = r'(?<=\\r\\n)[A-Za-z]+\.exe\s+\d+'
REG_FOR_LOCAL_SOCKET = r'(?:TCP\s+)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})'
REG_FOR_REMOTE_SOCKET = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})\s+[A-Z]+\s+(\d+)'

CMD_NETSTAT_COMMAND = 'netstat -aon |find /i "established"'
CMD_TASKLIST_COMMAND = "tasklist /M"


class MeterpreterScanner:
    def __init__(self):
        self._signatures: List[str] = []
        self._processes_with_signatures: List[str] = []
        self._processes_with_dynamic_port: List[str] = []
        self._suspicious_processes: Dict[str:List[str]] = {}

    def _check_windows_version(self) -> None:
        """Проверка версии windows - 7 или 10"""
        info = subprocess.check_output("systeminfo", shell=True)
        win = re.findall(REG_FOR_WINDOWS_VERSION, str(info))

        if win[0] == '10':
            self._signatures = WIN_10_SIGNATURE
        elif win[0] == '7':
            self._signatures = WIN_7_SIGNATURE
        else:
            print("[X] Только Windows 7 или Windows 10")

    def _search_process_with_dll(self, dll: str) -> None:
        """Поиск процессов с DLL библиотеками"""
        output_tasklist = subprocess.check_output(f"{CMD_TASKLIST_COMMAND} {dll}", shell=True)
        process_list = re.findall(REG_FOR_EXE_PROCESSES, str(output_tasklist))

        for process_info in process_list:
            process, process_PID = re.split(r'\s+', process_info)
            if process in self._suspicious_processes:
                self._suspicious_processes[f'{process}_{process_PID}'].append(dll)
            else:
                self._suspicious_processes[f'{process}_{process_PID}'] = [dll]

    def _check_suspicious_process(self) -> None:
        """Сканируем подозрительные процессы"""
        self._check_windows_version()

        for dll in self._signatures:
            self._search_process_with_dll(dll)
        for proc_info in self._suspicious_processes.items():
            proc_name, proc_dlls = proc_info
            if len(proc_dlls) == 5:
                print(f"[-] Найден подозрительный процесс : {proc_name}")
                self._processes_with_signatures.append(proc_name)
        if not self._processes_with_signatures:
            print("[+] Meterpreter сигнатура не найдена в памяти")

    def _scan_suspicious_ports(self) -> None:
        """Сканируем подозрительные порты"""
        scan_output = subprocess.check_output(CMD_NETSTAT_COMMAND, shell=True)
        local_sockets = re.findall(REG_FOR_LOCAL_SOCKET, str(scan_output))
        for l_socket in local_sockets:
            l_ip, l_port = l_socket.split(':')
            if int(l_port) >= 49152:
                if l_ip != "127.0.0.1":
                    victim_socket = f"{l_ip}:{l_port}"
                    data_with_suspicious_socket = scan_output.decode().split(victim_socket)
                    suspicious_info = re.findall(REG_FOR_REMOTE_SOCKET, data_with_suspicious_socket[1])[0]
                    suspicious_socket, suspicious_PID = suspicious_info
                    # порт 4444 используется по умолчанию в MSF и meterpreter
                    if int(suspicious_socket.split(':')[-1]) == 4444:
                        print(f"[!] Найдено MSF подключение: {suspicious_socket}")
                    print(f"[-] Подключение {victim_socket} к {suspicious_socket} "
                          f"использование динамический PID - {suspicious_PID}")
                    self._processes_with_dynamic_port.append(suspicious_PID)

    def finding_meterpreter_sessions(self):
        """Находим сессии meterpreter"""
        found = False
        self._check_suspicious_process()
        self._scan_suspicious_ports()

        # ищем процесс
        for proc in self._processes_with_signatures:
            proc_name, proc_PID = proc.split('_')
            if proc_PID in self._processes_with_dynamic_port:
                print(f'[!] Найдено совпадение в {proc_name} с PID {proc_PID}')
                found = True

        if not found:
            print(f"[+] Совпадений не найдено")


MeterpreterScanner().finding_meterpreter_sessions()
```

Теперь займемся сканером черных листов DNS, а точнее будем искать целевой IP в этих списках.

```python
import socket
import re
from ipaddress import ip_network, ip_address
from dns import resolver
from requests import get, exceptions


def ip_in_range(ip, addr):
    """Сканирование IP"""
    if ip_address(ip) in ip_network(addr):
        return True
    return False


def cloudfare_detect(ip):
    """Сканирование в Cloudfare"""
    list_addr = ["104.16.0.0/12"]

    url = 'https://www.cloudflare.com/ips-v4'
    req = get(url=url)

    for adr in req.text.split("\n"):
        list_addr.append(adr)

    for addr in list_addr:
        detect = ip_in_range(ip, addr)
        if detect:
            return True
    return False


def public_ip():
    """Получить публичный IP"""
    try:
        return get('https://api.ipify.org/').text
    except exceptions.ConnectionError:
        return '127.0.0.1'


def dns_bl_check(ip):
    bad_dict = dict()
    result = str()
    req = get('https://raw.githubusercontent.com/evgenycc/DNSBL-list/main/DNSBL')
    read = req.text.splitlines()
    
    for serv in read:
        print(f'Checking... {serv}')
        req = f"{'.'.join(reversed(ip.split('.')))}.{serv.strip()}"
        try:
            resolv = resolver.Resolver()
            resolv.timeout = 5
            resolv.lifetime = 5
            resp = resolv.resolve(req, 'A')
            resp_txt = resolv.resolve(req, 'TXT')
            result += f'{serv.strip():30}: [BAD]\n'
            pattern = r'(?:https?:\/\/)?(?:[\w\.]+)\.(?:[a-z]{2,6}\.?)(?:\/[\w\.]*)*\/?'
            find = re.findall(pattern, str(resp_txt[0]))
            if len(find) == 0:
                find = ['No address']
            bad_dict.update({serv.strip(): f'{resp[0]} {find[0]}'})
        except resolver.NXDOMAIN:
            result += f'{serv.strip():30}: [OK]\n'
        except (resolver.LifetimeTimeout, resolver.NoAnswer):
            continue
        except Exception as ex:
            raise ex
            return ('error', ex)
    
    if len(bad_dict) > 0:
        result += f'{ip} is found in black list\n'
        
        for bad in bad_dict:
            result += f' - {bad:30} : {bad_dict[bad]}\n'
    else:
        result += 'IP is not found in black list\n'

    return (result, 0)


def check_ip_in_black_list(addr_input):
    result = ''
    result += f'Your public IP: {public_ip()}\n'

    if addr_input.lower() == "x":
        exit(0)

    ip = ''
    
    try:
        ip = socket.gethostbyname(addr_input)
    except socket.gaierror as ex:
        return ex

    if cloudfare_detect(ip):
        result += f'Cloudfare detected: {ip}\n'
    else:
        result += 'Cloudfare not detected\n'
    
    dnsbl_list = dns_bl_check(ip)

    if dnsbl_list[0] is None or dnsbl_list[0] == 'error':
        return result
    else:
        result += dnsbl_list[0]

    return result


check_ip_in_black_list('<IP адрес>')
```


Теперь парсер ссылок:

```python
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

internal_urls = set()
external_urls = set()


def is_valid(url):
    """Данная функция проверяет, валиден ли URL

    Аргументы:
        url - ссылка на страницу
    """
    parsed = urlparse(url)
    
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """Получаем все ссылки с сайта"""
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        
        if href == "" or href is None:
            continue
        
        href = urljoin(url, href)

        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            continue
        
        if href in internal_urls:
            continue
        
        if domain_name not in href:
            if href not in external_urls:
                print(f"[!] Внешняя ссылка: {href}")
                external_urls.add(href)
            continue
        
        print(f"[*] Внутренняя ссылка: {href}")
        urls.add(href)
        internal_urls.add(href)

    return urls


def crawl(url, max_urls=30):
    """Парсинг"""
    total_urls_visited = 0

    total_urls_visited += 1
    print(f"[*] Работа над {url}")
    links = get_all_website_links(url)

    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


def get_links(url, max_urls=30):
    """Получаем ссылки"""
    crawl(url, max_urls)
    print("[+] Всего внутренних ссылок:", len(internal_urls))
    print("[+] Всего внешних ссылок:", len(external_urls))
    print("[+] Всего ссылок", len(external_urls) + len(internal_urls))
    print("[+] Всего проверенных ссылок:", max_urls)
```

Как видите, ничего сложного.

А мы едем дальше - следующий шаг это сканер портов:

```python
import socket
from datetime import datetime


def scan_ports(hostname):
    start = datetime.now()

    ports = {
        20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
        25: "SMTP", 43: "WHOIS", 53: "DNS", 80: "http",
        115: "SFTP", 123: "NTP", 143: "IMAP", 161: "SNMP",
        179: "BGP", 443: "HTTPS", 445: "MICROSOFT-DS",
        514: "SYSLOG", 515: "PRINTER", 993: "IMAPS",
        995: "POP3S", 1080: "SOCKS", 1194: "OpenVPN",
        1433: "SQL Server", 1723: "PPTP", 3128: "HTTP",
        3268: "LDAP", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 5900: "VNC", 8080: "Tomcat", 10000: "Webmin"
    }

    open_ports = []
    closed_ports = []
    [i for i in range(1, 65355)]

    ip = socket.gethostbyname(hostname)

    for port in range(65535):
        cont = socket.socket()
        cont.settimeout(1)

        # попытаемся подключиться
        try:
            cont.connect((ip, port))
        except socket.error:
            print(f'[!] Порт {port} закрыт')
            closed_ports.append([port])
        else:
            # выводим тип порта
            try:
                print(f"[{socket.gethostbyname(ip)}:{str(port)}] открыт/{ports[port]}")
                open_ports.append({port, ports[port]})
            except KeyError:
                print(f"[{socket.gethostbyname(ip)}:{str(port)}] открыт/неизвестный тип")
                open_ports.append({port, 'неизвестный тип'})
            finally:
                cont.close()

    ends = datetime.now()
    print("<Время работы:{}>".format(ends - start))

    print('[+] Закрытые порты: ')
    for closed_port in closed_ports:
        print(closed_port, end=', ')

    print()

    print('[+] Открытые порты: ')
    for open_port in open_ports:
        print(open_port)


scan_ports('<IP адрес>')
```

Следующий шаг - поиск SQL-Injection уязвимостей. Внедрение SQL-кода — один из распространённых способов взлома сайтов и программ, работающих с базами данных, основанный на внедрении в запрос произвольного SQL-кода.

```python
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint


def get_session(user_agent):
    session = requests.Session()
    session.headers["User-Agent"] = user_agent

    return session


def get_all_forms(session, url):
    """Дается `url`, и это возвращаем весь html-контент с формами"""
    soup = bs(session.get(url).content, "html.parser")
    
    return soup.find_all("form")

def get_form_details(form):
    """
    Эта функция получает всю доступную информацию о форме
    """
    details = {}
    
    # получаем действие формы (url цели)
    try:
        action = form.attrsession.get("action").lower()
    except:
        action = None
    
    # получаем метод формы (POST, GET, etc.)
    method = form.attrsession.get("method", "get").lower()
    
    # получаем все детали ввода
    inputs = []
    
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrsession.get("type", "text")
        input_name = input_tag.attrsession.get("name")
        input_value = input_tag.attrsession.get("value", "")
        inputsession.append({"type": input_type, "name": input_name, "value": input_value})
    
    # добавляем информацию в словарь деталей
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details


def is_vulnerable(response):
    """Простая логическая функция, определяющая, является ли страница
    уязвима ли SQL-инъекция из-за ее «ответа»"""

    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }

    for error in errors:
        # Если мы находим ошибку, то возвращаем True
        if error in response.content.decode().lower():
            return True

    # Нету ошибок
    return False


def scan_sql_injection(session, url):
    """Сканирование URL на нахождение уяизвимостей для SQL-инъекции"""

    for c in "\"'":
        # Добавляем кавычку к URL
        new_url = f"{url}{c}"
        print("[!] Попытка нахождения уязвимости SQL-инъекции на", new_url)
        # Создаем HTTP-запрос
        res = session.get(new_url)
        if is_vulnerable(res):
            # SQL-инъекция обнаружена на самом URL-адресе, 
            # нет необходимости предварительно извлекать формы и отправлять их
            print("[+] SQL инъекция найдена, ссылка:", new_url)
            return

    # Анализ форм
    forms = get_all_forms(session, url)
    print(f"[+] Найдено {len(forms)} форм на {url}.")

    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            # данные тела для отправки
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    # любая форма ввода, которая скрыта или имеет некоторое значение,
                    # просто используем его в теле формы
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    # все остальные, кроме отправки, используют некоторые ненужные данные со специальным символом
                    data[input_tag["name"]] = f"test{c}"
            
            # добавляем к URL ссылку с действием из формы
            url = urljoin(url, form_details["action"])
            
            if form_details["method"] == "post":
                res = session.post(url, data=data)
            elif form_details["method"] == "get":
                res = session.get(url, params=data)
            
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:")
                pprint(form_details)
                break


def scanning(fua, url):
    """fua - юзер агент, url - ссылка на сайт"""
    session = get_session(fua)
    scan_sql_injection(session, url)
```

Займемся поиском XSS-уязвимостей (межсайтовый скриптинг). XSS — тип атаки на веб-системы, заключающийся во внедрении в выдаваемую веб-системой страницу вредоносного кода и взаимодействии этого кода с веб-сервером злоумышленника. Является разновидностью атаки «Внедрение кода». Википедия

```python
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def get_all_forms(url, fua):
    """Вводится `url`, это возвращает все формы из HTML-контента
    fua - фейковый юзер агент"""
    headers = {
        'User-Agent': fua
    }

    soup = bs(requests.get(url, headers=headers).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """Данная функция получает все возможные данные из HTML-формы"""
    details = {}
    # Получаем действие формы
    action = form.attrs.get("action", "").lower()
    
    # Получаем все методы формы (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    
    # Получаем все инпуты
    inputs = []
    
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    
    # Добавляем в детали
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details


def submit_form(form_details, url, value):
    """
    Отправляем данные формы
    Возвращает HTTP ответ
    """
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    
    for input in inputs:
        # заменить весь текст и значения поиска на `value`
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
    
        input_name = input.get("name")
        input_value = input.get("value")
    
        if input_name and input_value:
            data[input_name] = input_value

    print(f"[+] Отправка вредоносной полезной нагрузки на {target_url}")
    print(f"[+] Данные: {data}")
    
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # GET request
        return requests.get(target_url, params=data)


def scan_xss(url, fua):
    """
    Получив `url`, он выводит все формы, уязвимые для XSS, и
    возвращает True, если кто-то из них уязвим, False в противном случае
    """
    forms = get_all_forms(url, fua)
    
    print(f"[+] Найдено {len(forms)} форм на {url}.")
    
    js_script = "<Script>alert('Detected')</script>"
    is_vulnerable = False

    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS найдена на {url}")
            print("[*] Детали формы:")
            pprint(form_details)
            is_vulnerable = True
    
    return is_vulnerable


if __name__ == "__main__":
    url = "https://xss-game.appspot.com/level1/frame"
    print(scan_xss(url, '<юзер агент>'))
```

Вот и все. Осталось это скомбинировать в одну программу на Python, считайте что это ваше домашнее задание. Попробуйте улучшить код, улучшить вывод сообщений и многое другое. А как насчет асинхронности? Обо всем этом мы будем говорить во второй части статьи - там мы будем красоту наводить, и пытаться оптимизировать.

# Заключение
Итак, в этой статье мы смогли написать набор OSINT (да и не только OSINT) инструментов. Оставляйте ваши комментарии, критику. Я понимаю, что всем не угодить, и вы можете высказаться в комментариях.

Я хочу предупредить, что весь мой код был скоплен за несколько месяцев кодинга. Если вы обнаружили код, который был уже в другой статье, прошу оставить комментарий, я внесу источник в статью. Благодарю за понимание!

Надеюсь вам понравилась статья!

## Ссылки
 + [GitHub-репозиторий](https://github.com/AlexeevDeveloper/cobra). Внимание, он в разработке, поэтому многое там не работает.
