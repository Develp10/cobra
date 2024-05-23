#!venv/bin/python3
"""Cobra OSS OSINT Tool

BSD 3-Clause License

Copyright (c) 2024, Alexeev Bronislav

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
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
