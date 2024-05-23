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
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# Модули
from modules.tlsconnection import TLSClient, TLSServer
from modules.port_scanner import scan_ports
from modules.netlib import url_info
from modules.dns_bl_scan import *
from modules.whois_information import *
from modules.network_base.ping_address import ping_addr


def execute(cmd: str) -> str:
	"""Выполнение команды в терминале

	Параметры:
	 + cmd: str - команда

	Возвращает:
	 + str - строка с выводом команды
	"""
	cmd = cmd.strip()

	if not cmd:
		return 'None'

	output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)    # Чтение и возрват (1)
	
	return str(output.decode()).replace('\n', '')


class NetCobra:
	"""Класс NetCobra"""
	def __init__(self, args, buffer=None):
		"""Инициализация класса NetCobra

		 + args - аргументы
		 + buffer=None - буфер"""
		self.args = args 					# Наши будующие аргументы
		self.buffer = buffer    			# Буфер с данными
		
		# Подключение к серверу
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Обработка запроса и протоколов
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def run(self):
		"""Запуск NetCobra
		Если аргумент равен listen, то мы слушаем подключения
		Если же был передан любой другой, то мы запускаем функцию send"""
		if self.args.listen:
			print('[+] Слушаем...')
			self.listen()
		else:
			print('[+] Отправляем...')
			self.send()

	def send(self):
		"""Отправка данных
		Коннектимся к хосту, если буфер не пуст, то отправляем его. 
		Потом читаем данные, максимальный размер пакета - 4096 байтов"""
		self.socket.connect((self.args.target, self.args.port))			# Установка соединения с сервером
		
		print('[+] Отправляем данные...')

		if self.buffer:
			print('[/] Отправляем данные из буфера')
			self.socket.send(self.buffer)								# Проверка буфера на наличие данных

		try:
			while True:
				print('[+] Отправка данных на сервер')
				recv_len = 1								# Задаем длину запроса
				response = ''
				
				while recv_len:
					data = self.socket.recv(4096)			# Размер буфера в битах
					recv_len = len(data)					# Проверяем длину
					response += data.decode()				# Декодируем запрос
				
				# Если длина запроса больше 100
				if recv_len > 4096:							# Сверяем данные
					print("[/] Сообщение слишком длинное. Максимальное количество байтов в пакете - 4096")
					break
			
			if response:
				print('[/] Отправка данных и заполнение буфера')
				print(response)								# Выводим его на экран
				buffer = input('NetCobra > $ ')						# Задаем приглашение для ввода
				buffer += '\n'								# Добавляем перевод на новую строку
				self.socket.send(buffer.encode())			# Отправляем информацию с ее энкодированием
		except KeyboardInterrupt:
			# Нажат Ctrl+C, клавиатурное прерывание
			print('[Abort] Сервер прервал свою работу клавиатурным прерыванием')
			self.socket.close()
			sys.exit()

	def listen(self):
		"""Слушаем подключения"""
		try:
			self.socket.bind((self.args.target, self.args.port))
		except OSError as oserr:
			print(f'[!] Операция была прервана с ошибкой: {oserr}')
			self.socket.close()
			sys.exit()
		else:
			print(f'[/] Слушаем подключение к {self.args.target}:{self.args.port}')

		self.socket.listen(5)
		print('[+] Слушаем подключения...')

		try:
			while True:
				client_socket, addr = self.socket.accept()
				print(f'[{addr}] присоединился')
				client_thread = threading.Thread(target=self.handle, args=(client_socket,))
				client_thread.start()
		except KeyboardInterrupt:
			print('[Abort] Сервер прервал свою работу клавиатурным прерыванием')
			self.socket.close()
			sys.exit()


	def handle(self, client_socket):
		"""Обработчик"""
		data = client_socket.recv(4096).decode('utf-8')
		print(data)

		if self.args.execute:
			output = execute(self.args.execute)				# Обращаемся к командной строке
			client_socket.send(output.encode())
			print(f'[exec] {output}')
		elif self.args.upload:
			file_buffer = b''								# Задаем буфер обмена
			
			while True:
				data = client_socket.recv(4096)				# Размер буфера в битах
				if data:
					print(f'[Данные] {data}')
					file_buffer += f'{data}\n'				# Помещаем файл в наш запрос
				else:
					break
			
			with open(self.args.upload, 'wb') as f:
				print(f'[+] Записываем данные в файл {self.args.upload}')
				f.write(file_buffer)						# Открываем и читаем файл в бинарном виде
			
			message = f'Файл сохранен в {self.args.upload}'	# Выгружаем и отправляем на сервер
			client_socket.send(message.encode())
			self.socket.close()
			sys.exit()
		elif self.args.command:
			cmd_buffer = b''								# Снова задаем буфер
			while True:
				try:
					client_socket.send(b'Unknown: #> ')		# Приглашение для ввода команды
					
					while '\n' not in cmd_buffer.decode():
						cmd_buffer += client_socket.recv(64)
					
					response = execute(cmd_buffer.decode())	# Декодирование команды в читаемый для пк вид
					
					if response:
						client_socket.send(response.encode())	# Отправка ответа
					
					cmd_buffer = b''						# Очистка буфера
				except Exception as e:						# В случаи ошибки говорим что сервер умер от потери питания
					print(f'[!] Сервер был отключен: {e}')
					self.socket.close()
					sys.exit()
		else:
			while True:
				data = client_socket.recv(4096).decode('utf-8')
				if data:
					print(f'[Данные] {data}')
				else:
					break


def main():
	"""Главная функция. Запускается при прямом выполнении
	Здесь создаются переменные или константы, парсер аргументов и запускаются функции"""
	client_key = 'client.key'
	client_cert = 'client.crt'
	server_cert = 'server.crt'
	server_key = 'server.key'
	
	parser = argparse.ArgumentParser(description='NetCobra', formatter_class=argparse.RawDescriptionHelpFormatter, 
								epilog=textwrap.dedent('''
Примеры использования:

// Командная оболочка
netcobra -t 127.0.0.1 -p 4444 -l -c

// Загружаем в файл
netcobra -t 127.0.0.1 -p 4444 -l -u=mytest.txt

// Выполняем команду
netcobra -t 127.0.0.1 -p 4444 -l -e=\"cat /etc/passwd\"

// Шлем текст на порт сервера 1234
echo 'ABC' | ./netcobra -t 127.0.0.1 -p 1234

// Соединяемся с сервером
netcobra -t 127.0.0.1 -p 4444

// Узнаем информацию о домене по IP адресу
netcobra -t 127.0.0.1 -w

// Узнаем, есть ли IP в черных списках DNS
netcobra -t 127.0.0.1 -b

// Запуск TLS-соединения (сервер)
netcobra -t 127.0.0.1 -p 4444 -ts

// Запуск TLS-соединения (клиент)
netcobra -t 127.0.0.1 -p 4444 -tc

// Сканер портов
netcobra -s -t 127.0.0.1 -pc 65536

// Информация о сети
netcobra -ni

// Информация о домене
netcobra -ui -t ya.ru

Copyright Okulus Dev (C) 2023
	'''))

	parser.add_argument('-c', '--command', action='store_true',
						help='командная строка')
	parser.add_argument('-e', '--execute', help='выполнение специфичной команды')
	parser.add_argument('-l', '--listen', action='store_true', help='слушание подключений')
	parser.add_argument('-p', '--port', type=int, default=5555,
						help='специфичный порт')
	parser.add_argument('-t', '--target', default='192.168.1.203',
						help='специфичный IP адрес')
	parser.add_argument('-u', '--upload', help='загрузка файла')
	parser.add_argument('-w', '--whois', help='информация о домене по IP адресу', action='store_true')
	parser.add_argument('-b', '--blacklist', help='проверить IP в черных списках DNS', action='store_true')
	parser.add_argument('-ts', '--tls-server', help='запуск tls-сервера', action='store_true')
	parser.add_argument('-tc', '--tls-client', help='запуск tls-клиента', action='store_true')
	parser.add_argument('-s', '--scan-ports', help='сканирование портов', action='store_true')
	parser.add_argument('-pc', '--ports-count', help='количество портов для сканирования')
	parser.add_argument('-ni', '--network-info', help='информация о сети', action='store_true')
	parser.add_argument('-ui', '--url-info', help='информация об домене', action='store_true')
	parser.add_argument('--ping', help='ping IP адреса', action='store_true')
	args = parser.parse_args()

	if args:
		if args.whois:
			ipwhois_info(args.target)
			whois_info(args.target)
			print('\n')
			validate_request(args.target)
		elif args.ping:
			if ping_addr(args.target):
				print(f'[{args.target}] Доступен')
			else:
				print(f'[{args.target}] Недоступен')
		elif args.url_info:
			if args.target:
				url_info(args.target)
		elif args.network_info:	
			check_network()
		elif args.scan_ports:
			print(f'[+] Запуск сканер портов на {args.target}')

			if args.ports_count:
				if args.ports_count.isdigit():
					if int(args.ports_count) <= 2 ** 16:
						ports_count = int(args.ports_count)
					else:
						ports_count = 8000
				else:
					ports_count = 8000
			else:
				ports_count = 8000

			print(f'[/] Количество портов для сканирования: {ports_count}')

			try:
				scan_ports(args.target, port_count=ports_count)
			except Exception as e:
				print(f'[!] Произошла ошибка: {e}')
				sys.exit()
		elif args.blacklist:
			check_ip_in_black_list(args.target)
		elif args.tls_server:
			tls_serv = TLSServer(args.target, args.port, server_key, client_cert, server_cert)
			tls_serv.create_ssl_context()
			print(f'[{args.target}:{args.port}] Запуск TLS соединения (серверная часть)')
			tls.run()
		elif args.tls_client:
			tls_client = TLSClient(args.target, args.port, client_key, client_cert, server_cert)
			tls_client.create_ssl_context()
			print(f'[{args.target}:{args.port}] Подключение TLS соединения (клиентская часть)')
			tls_client.run()
		else:
			print('[/] Попытка соединения с сервером...')
			if args.listen:
				buffer = ''
			else:
				print('Введите сообщение для буфера:')
				buffer = sys.stdin.read()
			
			nc = NetCobra(args, buffer.encode())
			nc.run()


if __name__ == '__main__':
	main()
