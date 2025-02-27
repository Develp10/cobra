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
import modules.network_base.ipv4_local_cli as ipv4_cli
import modules.network_base.ipv4_local_getmac as ipv4_gm
import modules.network_base.ipv4_local_sock as ipv4_sock

import modules.network_base.router_ip as getaway

import modules.network_base.network_params as net_param

import modules.network_base.ip_from_domain as ip_domain
import modules.network_base.domain_from_ip as domain_ip
import modules.network_base.service_on_port as serv_port

import modules.network_base.my_public_ip as public_ip
import modules.network_base.ping_address as ping_addr
import modules.network_base.geolocation_ip as geo_ip
import modules.network_base.addr_from_geo as addr_geo


def url_info(url):
	print(f'Пинг домена или адреса: {ping_addr.ping_addr(ip_domain.ip_from_domain(f"{url}"))}')
	print(f"Координаты по IP-адресу: {geo_ip.geo_ip(domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}')))}")
	print(f"Физический адрес по координатам: "
		f"{addr_geo.get_addr(geo_ip.geo_ip(domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}'))))}")
	print(f"IP-адрес домена {url}: {ip_domain.ip_from_domain(f'{url}')}")
	print(f"Доменное имя {url} по полученному IP: {domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}'))}")


def ip_info(ip: str) -> str:
	result = ''
	result += f'Ping domain or address: {ping_addr.ping_addr(ip)}\n'
	result += f"Coords by IP: {geo_ip.geo_ip(ip)}\n"
	result += f"Geo Addr Coords by IP: {addr_geo.get_addr(geo_ip.geo_ip(domain_ip.domain_ip(ip)))}\n"
	result += f"Domain name: {domain_ip.domain_ip(ip)}\n"

	return result


def check_network():
	print(f'Локальный IP: {ipv4_cli.local_ipv4()}')
	print(f'Локальный IP: {ipv4_gm.local_ipv4()}')
	print(f'Локальный IP: {ipv4_sock.local_ipv4()}')

	print(f'IP шлюза по-умолчанию: {getaway.router_ip()}')

	print(f'Параметры сетевого интерфейса по-умолчанию:\n{net_param.network_param()}')

	print(f'Имя службы работающей на порту 80: {serv_port.type_port(80)}')

	print(f'Ваш публичный IP: {public_ip.public_ip()}')

