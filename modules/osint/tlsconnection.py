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
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
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
