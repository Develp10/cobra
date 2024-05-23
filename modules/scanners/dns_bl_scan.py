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
import socket
import re
from ipaddress import ip_network, ip_address
from dns import resolver
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
	bad_dict = dict()
	result = str()
	req = get('https://raw.githubusercontent.com/evgenycc/DNSBL-list/main/DNSBL')
	read = req.text.splitlines()
	
	for serv in read:
		print(f'Checking... {serv}')
		req = f"{'.'.join(reversed(ip.split('.')))}.{serv.strip()}"
		try:
			resolv = resolver.Resolver()
			resolv.timeout = 5
			resolv.lifetime = 5
			resp = resolv.resolve(req, 'A')
			resp_txt = resolv.resolve(req, 'TXT')
			result += f'{serv.strip():30}: [BAD]\n'
			pattern = r'(?:https?:\/\/)?(?:[\w\.]+)\.(?:[a-z]{2,6}\.?)(?:\/[\w\.]*)*\/?'
			find = re.findall(pattern, str(resp_txt[0]))
			if len(find) == 0:
				find = ['No address']
			bad_dict.update({serv.strip(): f'{resp[0]} {find[0]}'})
		except resolver.NXDOMAIN:
			result += f'{serv.strip():30}: [OK]\n'
		except (resolver.LifetimeTimeout, resolver.NoAnswer):
			continue
		except Exception as ex:
			raise ex
			return ('error', ex)
	
	if len(bad_dict) > 0:
		result += f'{ip} is found in black list\n'
		
		for bad in bad_dict:
			result += f' - {bad:30} : {bad_dict[bad]}\n'
	else:
		result += 'IP is not found in black list\n'

	return (result, 0)


def check_ip_in_black_list(addr_input):
	result = ''
	result += f'Your public IP: {public_ip()}\n'

	if addr_input.lower() == "x":
		exit(0)

	ip = ''
	
	try:
		ip = socket.gethostbyname(addr_input)
	except socket.gaierror as ex:
		return ('error', ex)

	if cloudfare_detect(ip):
		result += f'Cloudfare detected: {ip}\n'
	else:
		result += 'Cloudfare not detected\n'
	
	dnsbl_list = dns_bl_check(ip)

	if dnsbl_list[0] is None or dnsbl_list[0] == 'error':
		return (result, 0)
	else:
		result += dnsbl_list[0]

	return (result, 0)
