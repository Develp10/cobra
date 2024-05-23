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
import os
from datetime import datetime
from core.logger import Logger
from core.style import FG, Style
from modules.anonymity.fakeuseragent import generate_useragent
from modules.osint.ip import get_info_about_ip
from modules.osint.netlib import ip_info
from modules.osint.phone import get_info_phonenumber
from modules.scanners.dns_bl_scan import check_ip_in_black_list
from dotenv import load_dotenv

logger = Logger('cobra.log', filename=__name__)
load_dotenv()
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_KEY")
signature_resources = ['res/signatures.txt', 'res/signatures2.txt',
						'res/signatures3.txt', 'res/signatures4.txt']

signature_resource_info = 'res/signatures_info.json'


class BaseModule:
	"""Base Module class"""
	def __init__(self, filename: str=None):
		"""Initialization module

		Arguments:
		---------
		 + filename: str=None - filename path for reports"""
		self.curr_date = datetime.now()

		if filename is None:
			self.filename = f'cobra_report_{self.curr_date}.txt'
		else:
			self.filename = filename

	def write(self, text: str) -> bool:
		"""Write information to log

		Arguments:
		---------
		 + text: str - text for log"""

		try:
			with open(self.filename, 'a') as log:
				log.write(f'{text}\n')
		except Exception as ex:
			logger.log(f'Error when save to log: {ex}', 'error')
			return False
		else:
			Style.write(f'{Style.italic}{FG.green}Report saved in {Style.italic}{self.filename}{Style.reset}')


class OSINTModule(BaseModule):
	"""OSINT Module"""
	@logger.debug_func
	def ip(self, ipaddr: str) -> tuple:
		"""Get information about IP address

		Arguments:
		---------
		 + ipaddr: str - IP v4 address"""
		result = ''
		whois = ''

		try:
			result, whois = get_info_about_ip(ipaddr, generate_useragent())
			result += ip_info(ipaddr)
		except Exception as ex:
			logger.log(f'Error when receiving information about the IP address: {ex}', 'error', caller_function='OSINTModule.ip')
			return None
		else:
			if result is None and whois is None:
				logger.log('Unknown error when receiving information about the IP address: summary info or whois is none', 'error', caller_function='OSINTModule.ip')
				return ('No info', 'No info')

		if result == 'error':
			logger.log(f'Error: {whois}', 'error', caller_function='OSINTModule.ip')
			return None

		logtext = f'Cobra OSS OSINT Tool report {self.curr_date} for IP {ipaddr}\n\nResult: {result}\nWhoIS Full Info: {whois}'
		self.write(logtext)
		print(result)

		return (result, whois)

	@logger.debug_func
	def phone(self, phonenumber: str):
		result, errcode = '', 0
		try:
			result, errcode = get_info_phonenumber(phonenumber, generate_useragent())
		except Exception as ex:
			logger.log(f'Error when receiving information about the phone number: {ex}', 'error', caller_function='OSINTModule.phone')
		else:
			if result is None:
				logger.log('Unknown error when receiving information about the phone number', 'error', caller_function='OSINTModule.phone')
				return None

		if errcode != 0 or result == 'error':
			logger.log(f'Error: {errcode}', 'error', caller_function='OSINTModule.phone')
			return None
		
		logtext = f'Cobra OSS OSINT Tool report {self.curr_date} for {phonenumber}\n\nResult: {result}\nError: {errcode}'
		self.write(logtext)
		print(result)

		return (result, errcode)



class ScannerModule(BaseModule):
	@logger.debug_func
	def dns_bl(self, ipaddr: str):
		"""Check IP Address in DNS Black List

		Arguments:
		---------
		 + ipaddr: str - IP address
		"""
		result, errcode = '', 0

		try:
			result, errcode = check_ip_in_black_list(ipaddr)
		except Exception as e:
			logger.log(f'Error when searching for IP in DNS blacklists: {e}', 'error', caller_function='ScannerModule.dns_bl')
		else:
			if result is None:
				logger.log('Unknown error when searching for IP in DNS blacklists', 'error', caller_function='OSINTModule.phone')
				return None

		if errcode != 0 or result == 'error':
			logger.log(f'Error: {errcode}', 'error', caller_function='ScannerModule.dns_bl')
			return None

		logtext = f'Cobra OSS OSINT Tool report {self.curr_date} for {ipaddr} (scan dns black lists)\n\nResult: {result}\nError: {errcode}'
		self.write(logtext)
		print(result)

		return (result, errcode)


@logger.debug_func
def main():
	logger.log('Sorry, this project in developement. See you later!', 'debug', True, caller_function='cobra.main')
	logger.log('[ru] Извините, но этот проект еще в разработке. Увидимся позже!', 'debug', True, caller_function='cobra.main')

	print(f'\n{Style.italic}{Fore.green}Please, star repo: https://github.com/AlexeevDeveloper/cobra{Style.reset}')


if __name__ == '__main__':
	main()
