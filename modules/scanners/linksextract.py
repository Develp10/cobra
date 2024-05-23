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
