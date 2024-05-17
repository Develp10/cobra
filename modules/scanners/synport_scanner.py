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
from scapy.layers.inet import ICMP, IP, TCP, sr1
import socket
from datetime import datetime


def icmp_probe(ip: str):
	"""Функция для проверки, в сети ли сервер.
	Аргументы:
	 ip: str - IP-адрес сервера"""
	icmp_packet = IP(dst=ip) / ICMP()
	resp_packet = sr1(icmp_packet, timeout=10)
	
	return resp_packet is not None


def syn_scan(ip, ports):
	"""Функция для syn скана портов"""
	for port in ports:
		syn_packet = IP(dst=ip) / TCP(dport=port, flags="S")
		
		resp_packet = sr1(syn_packet, timeout=3)
		
		if resp_packet is not None:
			if resp_packet.getlayer('TCP').flags & 0x12 != 0:
				print(f"{ip}:{port} открыт/{resp_packet.sprintf('%TCP.sport%')}")


def start_scan(hostname):
	ip = socket.gethostbyname(hostname)
	ports = [20, 21, 22, 23, 25, 43, 53, 80,
			 115, 123, 143, 161, 179, 443, 445,
			 514, 515, 993, 995, 1080, 1194,
			 1433, 1723, 3128, 3268, 3306, 3389,
			 5432, 5060, 5900, 8080, 10000]

	try:
		if icmp_probe(ip):
			start = datetime.now()
			syn_ack_packet = syn_scan(ip, ports)
			syn_ack_packet.show()
			datetime.now()
		else:
			print("[!] Не удалось отправить ICMP пакет")
	except AttributeError:
		print("[+] Сканирование завершено")
		print("<Время работы:{}>".format(ends - start))
	except PermissionError:
		print('[!] Недостаточно прав')
		print('[!] Для работы запустите команду "make rootinstall", а после "make rootrun"')
