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
import os
import requests


def get_info_about_ip(ipaddr, fua) -> tuple:
	result = ''

	try:
		headers = {
			'User-Agent': fua
		}
		info_data = requests.get(f'https://ipinfo.io/{ipaddr}/json', headers=headers).json()
	except Exception as ex:
		return (f'Error: {ex}', f'Error: {ex}')

	whois_info = os.popen(f'whois {ipaddr}').read().strip()

	result += f'IP: {info_data.get("ip")}\n'
	result += f'Город: {info_data.get("city")}\n'
	result += f'Регион: {info_data.get("region")}\n'
	result += f'Страна: {info_data.get("country")}\n'
	result += f'Имя хоста: {info_data.get("hostname")}\n'
	result += f'JSON данные: {info_data}\n'

	return (result, whois)
