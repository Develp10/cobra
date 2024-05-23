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
import os
from time import perf_counter
from hashlib import sha256, sha1, md5
import vt
import json


def add_signatures(new_signatures: dict) -> None:
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
	try:
		with open(signature_resource_info, 'w') as file:
			json.dump(signatures, file, indent=4)
	except Exception:
		return False
	else:
		return True


def get_info_signature(signature: str) -> str:
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
	result = f'Сканируем {filename} на наличие угроз...\n'

	try:
		print('Load singatures...')
		start = perf_counter()
		shahash = sha256()
		sha1hash = sha1()
		md5hash = md5()

		with open(filename, 'rb') as file:
			while True:
				data = file.read()
				if not data:
					break
				shahash.update(data)
				sha1hash.update(data)
				md5hash.update(data)

			result1 = shahash.hexdigest()
			result2 = sha1hash.hexdigest()
			result3 = md5hash.hexdigest()
			result += f'Проверяем наличие хешей "{result1}", "{result2}", "{result3}" (sha256, sha1, md5) в сигнатурах...\n'

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

		with open(filename, "rb") as f:
			client.scan_file(f, wait_for_completion=True)
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

			if result in signatures:
				info = get_info_signature(result)
				result += f'Информация: {info}\n'
			elif result2 in signatures:
				info = get_info_signature(result2)
				result += f'Информация: {info}\n'
			elif result3 in signatures:
				info = get_info_signature(result3)
				result += f'Информация: {info}\n'

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
		result += '[!] Файл не найден\n'
	except PermissionError:
		result += '[!] Ошибка прав доступа к файлу\n'

	print('End')

	return result
