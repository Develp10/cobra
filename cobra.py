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
from datetime import datetime
from core.logger import Logger
from core.style import cls, FG, BG, Style, logo

from modules.anonymity.fakeuseragent import generate_useragent
from modules.osint.ip import get_info_about_ip

logger = Logger('cobra.log', filename=__name__)


def intro():
	Style.write(BG.rgb(22, 22, 22) + FG.rgb(240, 240, 240))
	Style.write(Style.clear)
	Style.write(Style.top)

	for line in logo.split('\n'):
		# Выводим лого
		Style.writew(f"{line}\n", 0.0015)


def clear_bg():
	cls()
	Style.write(BG.rgb(22, 22, 22) + FG.rgb(240, 240, 240))


class OSINTModule:
	def __init__(self, filename: str=None):
		curr_date = datetime.now()
		if filename is None:
			self.filename = f'cobra_osint_report_{curr_date}.txt'
		else:
			self.filename = filename

	def write(self, text: str):
		with open(self.filename, 'a') as log:
			log.write(f'{text}\n')

	@logger.benchmark
	@logger.debug_func
	def ip(self, ipaddr: str) -> str:
		result, whois = get_info_about_ip(ipaddr, generate_useragent())

		print(result)

		logtext = f'Cobra OSS OSINT Tool report {curr_date}\n\nResult: {result}\nWhoIS Full Info:{whois}'
		self.write(logtext)

		Style.write(f'{FG.green}Report saved in {Style.italic}{self.filename}{Style.reset}')

		return result


if __name__ == '__main__':
	intro()
	clear_bg()
	