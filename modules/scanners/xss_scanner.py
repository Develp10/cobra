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

