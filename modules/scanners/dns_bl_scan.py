#!/usr/bin/python3
# -*- coding:utf-8 -*-
import socket
from ipaddress import ip_network, ip_address
import dns
from requests import get, exceptions


def ip_in_range(ip, addr):
	"""Сканирование IP"""
	if ip_address(ip) in ip_network(addr):
		return True
	return False


def cloudfare_detect(ip):
	"""Сканирование в Cloudfare"""
	list_addr = ["104.16.0.0/12"]

	url = 'https://www.cloudflare.com/ips-v4'
	req = get(url=url)

	for adr in req.text.split("\n"):
		list_addr.append(adr)

	for addr in list_addr:
		detect = ip_in_range(ip, addr)
		if detect:
			return True
	return False


def public_ip():
	"""Получить публичный IP"""
	try:
		return get('https://api.ipify.org/').text
	except exceptions.ConnectionError:
		return '127.0.0.1'


def dns_bl_check(ip):
	"""Сканирование IP в черных листах DNS"""
	print('\n- Проверка черных списков\n')
	bad_dict = dict()
	req = get('https://raw.githubusercontent.com/evgenycc/DNSBL-list/main/DNSBL')
	read = req.text.splitlines()
	
	for serv in read:
		req = f"{'.'.join(reversed(ip.split('.')))}.{serv.strip()}"
		try:
			resolv = dns.resolver.Resolver()
			resolv.timeout = 5
			resolv.lifetime = 5
			resp = resolv.resolve(req, 'A')
			resp_txt = resolv.resolve(req, 'TXT')
			print(f'{serv.strip():30}: [BAD]')
			pattern = r'(?:https?:\/\/)?(?:[\w\.]+)\.(?:[a-z]{2,6}\.?)(?:\/[\w\.]*)*\/?'
			find = re.findall(pattern, str(resp_txt[0]))
			if len(find) == 0:
				find = ['No address']
			bad_dict.update({serv.strip(): f'{resp[0]} {find[0]}'})
		except dns.resolver.NXDOMAIN:
			print(f'{serv.strip():30}: [OK]')
		except (dns.resolver.LifetimeTimeout, dns.resolver.NoAnswer):
			continue
	
	if len(bad_dict) > 0:
		len_str = len(f'IP-АДРЕС: "{ip.upper()}" ОБНАРУЖЕН В ЧЕРНЫХ СПИСКАХ')
		print(f'\nIP-АДРЕС: {ip.upper()} ОБНАРУЖЕН В ЧЕРНЫХ СПИСКАХ\n{"*"*len_str}')
		
		for bad in bad_dict:
			print(f' - {bad:30} : {bad_dict[bad]}')
	else:
		print('\n[+] IP-адрес в черных списках не обнаружен')


def check_ip_in_black_list(addr_input):
	"""Есть ли IP в черных листах"""
	print(f'\n- Ваш внешний IP-адрес: {public_ip()}')
	#addr_input = input('- Введите IP-адрес или домен для проверки\n  Для выхода введите "x"\n  >>> ')
	if addr_input.lower() == "x":
		exit(0)
	ip = ''
	try:
		ip = socket.gethostbyname(addr_input)
	except socket.gaierror:
		print('\n - Не удалось получить IP-адрес')
		exit(0)

	if cloudfare_detect(ip):
		print(f'\n[!] ВНИМАНИЕ! Обнаружен адрес Cloudflare: {ip}')
	
	dns_bl_check(ip)
