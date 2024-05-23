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
from sys import stdout, stdin
from time import sleep
from datetime import datetime
import os

logo = """
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⣴⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  ⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣶⣄⠈⠻⣿⣿⣿⣿⣿⣿⡀⢰⣦⣀⠀⠀⠀⠀⠀⠀
   ⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣷⣤⡀⠙⢿⣿⣿⣿⡇⠀⣿⣿⣷⡄⠀⠀⠀
  ⠀⠀⠀⡰⠿⠿⠿⠿⠛⠛⠛⠛⠋⠉⠉⠀⠀⠈⠻⣿⡇⠀⣿⣿⣿⣿⣆⠀⠀⠀    ____    ___   ____   _____     _
  ⠀⠀⣀⣤⣤⣤⣤⣴⣶⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⣿⣿⣿⣿⡿⠂⠀⠀   /       /   \\  |   \\  |   |    / \\  
  ⠀⢀⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⠋⢀⣴⡀⠀  |        |   |  |___/  |___/   /   \\  
  ⠀⢸⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠟⠁⣠⣾⣿⡇⠀  |        |   |  |   |  | \\    |-----|
  ⠀⢸⣿⣿⠋⢀⣴⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⡇    \\____   \\___/  |___|  |  \\_  /     \\ 
  ⠀⠈⠟⠁⣠⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⠁⠀
  ⠀⠀⠠⣾⣿⣿⣿⣿⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⠿⠿⠟⠛⠛⠛⠋⠀⠀               OSS OSINT TOOL 
  ⠀⠀⠀⠹⣿⣿⣿⣿⠀⢸⣿⣦⣄⠀⠀⣀⣀⣀⣤⣤⣤⣤⣤⣶⣶⣶⠆⠀⠀⠀        Alexeev Bronislav (C) 2024
  ⠀⠀⠀⠀⠘⢿⣿⣿⡄⠸⣿⣿⣿⣷⣄⡈⠙⢿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀
  ⠀⠀⠀⠀⠀⠀⠉⠻⠇⠀⣿⣿⣿⣿⣿⣿⣦⡀⠉⠻⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀
           ⠙⠛⠻⠿⠿⠿⠿⠟⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


def cls():
	# Очистка терминала
	os.system('clear')


class FG:
	"""Цвет текста
	Данный класс содержит константы ansi-кодов разных цветов для текста"""
	black = "\u001b[30m"
	red = "\u001b[31m"
	green = "\u001b[32m"
	yellow = "\u001b[33m"
	blue = "\u001b[34m"
	magenta = "\u001b[35m"
	cyan = "\u001b[36m"
	white = "\u001b[37m"
  
	def rgb(r: int, g: int, b: int) -> str:
		"""Функция для преобразования RGB-цвета в ansi-код
		
		Аргументы:
		 r: int - красный цвет (0-255)
		 g: int - зеленый цвет (0-255)
		 b: int - синий цвет (0-255)

		Возвращает:
		 + str - ansi код цвета"""
		return f"\u001b[38;2;{r};{g};{b}m"

class BG:
	"""Цвет фона
	Данный класс содержит константы ansi-кодов разных цветов для фона"""
	black = "\u001b[40m"
	red = "\u001b[41m"
	green = "\u001b[42m"
	yellow = "\u001b[43m"
	blue = "\u001b[44m"
	magenta = "\u001b[45m"
	cyan = "\u001b[46m"
	white = "\u001b[47m"
	
	def rgb(r: int, g: int, b: int) -> str:
		"""Функция для преобразования RGB-цвета в ansi-код
		
		Аргументы:
		 r: int - красный цвет (0-255)
		 g: int - зеленый цвет (0-255)
		 b: int - синий цвет (0-255)

		Возвращает:
		 + str - ansi код цвета"""
		return f"\u001b[48;2;{r};{g};{b}m"


class Style:
	reset = "\u001b[0m"
	bold = "\u001b[1m"
	underline = "\u001b[4m"
	reverse = "\u001b[7m"
	clear = "\u001b[2J"
	italic = '\u001b[3m'
	clearline = "\u001b[2K"
	up = "\u001b[1A"
	down = "\u001b[1B"
	right = "\u001b[1C"
	left = "\u001b[1D"
	nextline = "\u001b[1E"
	prevline = "\u001b[1F"
	top = "\u001b[0;0H"
	
	def to(x, y):
		return f"\u001b[{y};{x}H"
	
	def write(text="\n"):
		stdout.write(f'{text}\n')
		stdout.flush()
	
	def writew(text="\n", wait=0.01):
		for char in text:
			stdout.write(char)
			stdout.flush()
			sleep(wait)
  
	def read(begin=""):
		text = ""
		stdout.write(begin)
		stdout.flush()
		while True:
			char = ord(stdin.read(1))
      
		if char == 3: return
		elif char in (10, 13): return text
		else: text += chr(char)
	
	def readw(begin="", wait=0.5):
		text = ""

		for char in begin:
			stdout.write(char)
			stdout.flush()
			sleep(wait)
		
		while True:
			char = ord(stdin.read(1))
      
			if char == 3: return
			elif char in (10, 13): return text
			else: text += chr(char)


def info_message(text: str, highlight: bool=False) -> str:
	"""Print info message.

	Arguments:
	---------
	 + text: str - text of message
	+ highlight: bool=False - need to highlight background

	"""
	prefix = f'{BG.green}{FG.black}' if highlight else f'{FG.green}'
	print(f'{prefix}[INFO {datetime.now()}]{Style.reset} {text}{Style.reset}')


def warn_message(text: str, highlight: bool=False) -> str:
	"""Print warn message.

	Arguments:
	---------
	 + text: str - text of message
	+ highlight: bool=False - need to highlight background

	"""
	prefix = f'{BG.yellow}{FG.black}' if highlight else f'{FG.yellow}'
	print(f'{prefix}[WARN {datetime.now()}]{Style.reset} {text}{Style.reset}')


def error_message(text: str, highlight: bool=False) -> str:
	"""Print error message.

	Arguments:
	---------
	 + text: str - text of message
	+ highlight: bool=False - need to highlight background

	"""
	prefix = f'{BG.red}{FG.black}' if highlight else f'{FG.red}'
	print(f'{prefix}[ERROR {datetime.now()}]{Style.reset} {text}{Style.reset}')


def debug_message(text: str, highlight: bool=False) -> str:
	"""Print debug message.

	Arguments:
	---------
	 + text: str - text of message
	+ highlight: bool=False - need to highlight background

	"""
	prefix = f'{BG.magenta}{FG.black}' if highlight else f'{FG.magenta}'
	print(f'{prefix}[DEBUG {datetime.now()}]{Style.reset} {text}{Style.reset}')


def other_message(text: str, msg_type: str, highlight: bool=False) -> str:
	"""Print messages.

	Arguments:
	---------
	 + text: str - text of message
	 + msg_type: str - type of message (ex. other)
	+ highlight: bool=False - need to highlight background

	"""
	prefix = f'{BG.cyan}{FG.black}' if highlight else f'{FG.cyan}'
	print(f'{prefix}[{msg_type.upper()} {datetime.now()}]{Style.reset} {text}{Style.reset}')


def run_exception(text: str, highlight: bool=False):
	"""Run exception message.

	Arguments:
	---------
	 + text: str - text of message
	+ highlight: bool=False - need to highlight background

	"""
	prefix = f'{BG.red}{FG.black}' if highlight else f'{FG.red}'
	print(f'{Style.bold}{prefix}[EXCEPTION {datetime.now()}]{Style.reset} {text}{Style.reset}')
	raise Exception(text)


menu = f"""
{FG.rgb(64, 224, 208)}
	╔═════════════════════════════════@hex_warehouse═╗   
	║                     Other                      ║
	║ 0 - Exit                                       ║
	║                    Anonymity                   ║
	║ 1 - Generate fake user agent                   ║
	║ 2 - Change MAC Address                         ║
	║                    Scanners                    ║
	║ 3 - DNS Black List scanner                     ║
	║ 4 - Links extractor                            ║
	║ 5 - Port Scanner v1                            ║
	║ 6 - Port SYN Scanner                           ║
	║ 7 - SQL Injection
	╚════════════════════════════════════════════════╝
"""
