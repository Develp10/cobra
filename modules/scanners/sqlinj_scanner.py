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
	session = get_session(fua)
	scan_sql_injection(session, url)
