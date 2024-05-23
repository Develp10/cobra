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
