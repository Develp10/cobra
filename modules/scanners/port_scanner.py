#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Copyright (c) 2023, Okulus Dev
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
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
import socket
from datetime import datetime


def scan_ports(hostname):
	start = datetime.now()

	ports = {
		20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
		25: "SMTP", 43: "WHOIS", 53: "DNS", 80: "http",
		115: "SFTP", 123: "NTP", 143: "IMAP", 161: "SNMP",
		179: "BGP", 443: "HTTPS", 445: "MICROSOFT-DS",
		514: "SYSLOG", 515: "PRINTER", 993: "IMAPS",
		995: "POP3S", 1080: "SOCKS", 1194: "OpenVPN",
		1433: "SQL Server", 1723: "PPTP", 3128: "HTTP",
		3268: "LDAP", 3306: "MySQL", 3389: "RDP",
		5432: "PostgreSQL", 5900: "VNC", 8080: "Tomcat", 10000: "Webmin"
	}

	open_ports = []
	closed_ports = []
	[i for i in range(1, 65355)]

	ip = socket.gethostbyname(hostname)

	for port in range(65535):
		cont = socket.socket()
		cont.settimeout(1)

		try:
			cont.connect((ip, port))
		except socket.error:
			print(f'[!] Порт {port} закрыт')
			closed_ports.append([port])
		else:
			try:
				print(f"[{socket.gethostbyname(ip)}:{str(port)}] открыт/{ports[port]}")
				open_ports.append({port, ports[port]})
			except KeyError:
				print(f"[{socket.gethostbyname(ip)}:{str(port)}] открыт/неизвестный тип")
				open_ports.append({port, 'неизвестный тип'})
			finally:
				cont.close()

	ends = datetime.now()
	print("<Время работы:{}>".format(ends - start))

	print('[+] Закрытые порты: ')
	for closed_port in closed_ports:
		print(closed_port, end=', ')

	print()

	print('[+] Открытые порты: ')
	for open_port in open_ports:
		print(open_port)
