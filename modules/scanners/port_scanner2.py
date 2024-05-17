#!/usr/bin/python3
# -*- coding:utf-8 -*-
import socket
from threading import Thread

opened_ports = []


def scan_port(target_hostname: str, port: int):
	global opened_ports

	ports = {
		20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
		25: "SMTP", 43: "WHOIS", 53: "DNS", 80: "http",
		115: "SFTP", 123: "NTP", 143: "IMAP", 161: "SNMP",
		179: "BGP", 443: "HTTPS", 445: "MICROSOFT-DS",
		514: "SYSLOG", 515: "PRINTER", 993: "IMAPS",
		995: "POP3S", 1080: "SOCKS", 1194: "OpenVPN",
		1433: "SQL Server", 1723: "PPTP", 3128: "HTTP",
		3268: "LDAP", 3306: "MySQL", 3389: "RDP",
		5432: "PostgreSQL", 5900: "VNC", 8080: "Tomcat", 10000: "Webmin"}

	try:
		sock = socket.socket()
		sock.settimeout(1)
		sock.connect((target_hostname, port))
	except:
		print(f'[{target_hostname}] {port} закрыт')
	else:
		print(f'[{target_hostname}] {port} открыт')
		try:
			opened_ports.append(f'{port}/{ports[port]}')
		except:
			opened_ports.append(port)


def scan_ports(target_hostname: str, port_count: int=2 ** 16) -> dict:
	ip_addr = socket.gethostbyname(target_hostname)

	threads: list[Thread] = []

	count = 0
	for port in range(1, port_count):
		count += 1
		threads.insert(0, Thread(target=scan_port, args=(ip_addr, port,)))
		threads[0].start()

	for thread in threads:
		thread.join()

	print('\nОткрытые порты:')

	for opened_port in opened_ports:
		print(f'[/] Открыт {opened_port}')

	return
