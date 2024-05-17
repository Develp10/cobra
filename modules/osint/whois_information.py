#!/usr/bin/python3
# -*- coding:utf-8 -*-
import socket
import time
from ipaddress import IPv4Address, AddressValueError
from datetime import datetime
import ipwhois
import whois


def ipwhois_info(ip: str):
	"""Информация о IP по IPWhois

	 + ip: str - IP адрес"""
	results = ipwhois.IPWhois(ip).lookup_whois()
	print(results)
	print("\n")


def whois_info(ip):
	"""Информация о IP по WhoIs

	 + ip: str - IP адрес"""
	results = whois.whois(ip)
	print(results)


def ianna(ip):
	"""Информация о IP через whois.iana.org

	 + ip: str - IP адрес"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("whois.iana.org", 43))
	s.send((ip + "\r\n").encode())
	response = b""
	
	while True:
		data = s.recv(4096)
		response += data
		if not data:
			break
	
	s.close()
	whois = ''
	
	for resp in response.decode().splitlines():
		if resp.startswith('%') or not resp.strip():
			continue
		elif resp.startswith('whois'):
			whois = resp.split(":")[1].strip()
			break
	
	return whois if whois else False


def get_whois(ip, whois):
	"""Получения информации о IP"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((whois, 43))
	s.send((ip + "\r\n").encode())
	response = b""
	
	while True:
		data = s.recv(4096)
		response += data
		if not data:
			break
	
	s.close()
	whois_ip = dict()
	num = 0
	
	for ln in response.decode().splitlines():
		if ln.strip().startswith("%") or not ln.strip():
			continue
		else:
			if ln.strip().split(": ")[0].strip() in ['created', 'last-modified']:
				dt = datetime.fromisoformat(ln.strip().split(": ")[1].strip()).strftime("%Y-%m-%d %H:%M:%S")
				whois_ip.update({f'{ln.strip().split(": ")[0].strip()}_{num}': dt})
				num += 1
			else:
				whois_ip.update({ln.strip().split(": ")[0].strip(): ln.strip().split(": ")[1].strip()})
	
	return whois_ip if whois_ip else False


def validate_request(ip):
	"""Проверка IP

	 + ip - IP адрес"""
	try:
		IPv4Address(ip)
		if whois := ianna(ip):
			time.sleep(1)
			if info := get_whois(ip, whois):
				print(info)
			else:
				print("Не была получена информация")
		else:
			if info := get_whois(ip, 'whois.ripe.net'):
				print(info)
			else:
				print("Не была получена информация")
	except AddressValueError:
		print("IP адрес не валидный")
	except ConnectionResetError as ex:
		print(ex)
