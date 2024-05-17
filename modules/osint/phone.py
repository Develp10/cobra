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


def get_info_phonenumber(phonenumber, fua):
	url = f"https://htmlweb.ru/geo/api.php?json&telcod={phonenumber}"

	headers = {
		'User-Agent': fua
	}

	info_data = requests.get(url, headers=headers).json()

	print("Номер телефона --->", phonenumber)
	print("Страна ---> ", info_data["country"]["name"])
	print("Регион ---> ", info_data["region"]["name"])
	print("Округ ---> ", info_data["region"]["okrug"] )
	print("Оператор ---> ", info_data["0"]["oper"] )
	print("Часть света ---> ", info_data["country"]["location"] )
