#!venv/bin/python3
"""Paintlog Example File.

Copyright Alexeev Bronislav (C) 2024
BSD 3 Clause License
"""
from core.logger import pydbg_obj, Logger
from core.paint import info_message, warn_message, error_message, other_message, FG, Style, debug_message, run_exception

logger = Logger('main.log', filename=__name__)


@logger.benchmark
@logger.debug_func
def debug_print() -> list:
	num = 12
	float_int = 12.12
	string = 'Hello'
	boolean = True
	list_array = [1, 2, 3, 'Hi', True, 12.2]
	dictionary = {1: "HELLO", 2: "WORLD"}

	pydbg_obj(num, float_int, string, boolean, list_array, dictionary)


debug_print()

# Simple messages
info_message('INFORMATION')
warn_message('WARNING')
error_message('EXCEPTION')
debug_message('DEBUG')
other_message('SOME TEXT', 'OTHER')
# Highlight bg
info_message('Highlight INFORMATION', True)
warn_message('Highlight WARNING', True)
error_message('Highlight EXCEPTION', True)
debug_message('Highlight DEBUG', True)
other_message('Highlight SOME TEXT', 'OTHER', True)

# Message with logger
logger.log('INFORMATION logger', 'info')
logger.log('WARNING logger', 'warn')
logger.log('EXCEPTION logger', 'error')
logger.log('DEBUG logger', 'debug')
logger.log('SOME TEXT logger', 'other')
# Message with logger and highlight bg
logger.log('INFORMATION logger', 'info', True)
logger.log('WARNING logger', 'warn', True)
logger.log('EXCEPTION logger', 'error', True)
logger.log('DEBUG logger', 'debug', True)
logger.log('SOME TEXT logger', 'other', True)

print(f'{FG.red}{Style.bold}BOLD RED{Style.reset}{Style.dim} example{Style.reset}')

run_exception('EXCEPTION')
