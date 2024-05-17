#!/usr/bin/python3
"""Hunter - is a pack of programs for interacting with the Internet, for conducting penetration testing, working with Linux and OSINT
Copyright (C) 2022, 2023 Okulus Dev (Alexeev Bronislav)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
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
