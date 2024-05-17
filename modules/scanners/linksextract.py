#!/usr/bin/python3
# -*- coding:utf-8 -*-
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
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

internal_urls = set()
external_urls = set()


def is_valid(url):
	"""Данная функция проверяет, валиден ли URL

	Аргументы:
		url - ссылка на страницу
	"""
	parsed = urlparse(url)
	
	return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
	urls = set()
	domain_name = urlparse(url).netloc
	soup = BeautifulSoup(requests.get(url).content, "html.parser")

	for a_tag in soup.findAll("a"):
		href = a_tag.attrs.get("href")
		
		if href == "" or href is None:
			continue
		
		href = urljoin(url, href)

		parsed_href = urlparse(href)
		href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

		if not is_valid(href):
			continue
		
		if href in internal_urls:
			continue
		
		if domain_name not in href:
			if href not in external_urls:
				print(f"[!] Внешняя ссылка: {href}")
				external_urls.add(href)
			continue
		
		print(f"[*] Внутренняя ссылка: {href}")
		urls.add(href)
		internal_urls.add(href)

	return urls


def crawl(url, max_urls=30):
	total_urls_visited = 0

	total_urls_visited += 1
	print(f"[*] Работа над {url}")
	links = get_all_website_links(url)

	for link in links:
		if total_urls_visited > max_urls:
			break
		crawl(link, max_urls=max_urls)


def get_links(url, max_urls=30):
	crawl(url, max_urls)
	print("[+] Всего внутренних ссылок:", len(internal_urls))
	print("[+] Всего внешних ссылок:", len(external_urls))
	print("[+] Всего ссылок", len(external_urls) + len(internal_urls))
	print("[+] Всего проверенных ссылок:", max_urls)
