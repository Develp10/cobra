#!/usr/bin/python3
# -*- coding:utf-8 -*-
import ssl


class TLSClient:
	"""TLS клиент"""
	def __init__(self, hostname: str, port: int, client_key: str, client_cert: str, server_cert: str):
		"""Инициализация:

		 + hostname: str - имя хоста
		 + port: int - порт
		 + client_key: str - путь до файла с ключом клиента
		 + client_cert: str - путь до файла с сертификатом клиента
		 + server_cert: str - путь до файла с сертификатом сервера"""
		self.hostname = hostname
		self.port = port
		self.client_key = client_key
		self.client_cert = client_cert
		self.server_cert = server_cert

	def create_ssl_context(self):
		"""Создание SSL контекста"""
		context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=server_cert)
		context.load_cert_chain(certfile=client_cert, keyfile=client_key)
		context.load_verify_locations(cafile=server_cert)
		context.verify_mode = ssl.CERT_REQUIRED
		context.options |= ssl.OP_SINGLE_ECDH_USE
		context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

	def run(self):
		"""Запуск TLS клиента
		В данной функции реализовано простейшая функция отправки сообщения"""
		with socket.create_connection((hostname, port)) as sock:
			with context.wrap_socket(sock, server_side=False, server_hostname=hostname) as socks:
				print(socks.version())
				message = input("Введите ваше сообщение > ")
				socks.send(message.encode())
				receives = socks.recv(1024)
				print(receives)


class TLSServer:
	"""TLS сервер"""
	def __init__(self, hostname: str, port: int, server_key: str, client_cert: str, server_cert: str):
		"""Инициализация сервера

		 + hostname: str - имя хоста
		 + port: int - порт
		 + server_key: str - путь до файла с ключом сервера
		 + client_cert: str - путь до файла с сертификатом клиента
		 + server_cert: str - путь до файла с сертификатом сервера"""
		self.hostname = hostname
		self.server_cert = server_cert
		self.server_key = server_key
		self.client_cert = client_cert
		self.port = port

	def create_ssl_context(self):
		"""Создание SSL контекста"""
		context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
		context.verify_mode = ssl.CERT_REQUIRED
		context.verify_mode = ssl.CERT_REQUIRED
		context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
		context.options |= ssl.OP_SINGLE_ECDH_USE
		context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

	def run(self):
		"""Запуск TLS сервера
		В данной функции реализовано простейшая функция получения сообщения"""
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
			sock.bind(('', port))
			sock.listen(1)
			
			with context.wrap_socket(sock, server_side=True) as socks:
				conn, addr = socks.accept()
				print(f'[{addr}] Connected')
				message = conn.recv(1024).decode()
				capitalizedMessage = message.upper()
				conn.send(capitalizedMessage.encode())
