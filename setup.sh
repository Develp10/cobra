#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
END='\033[0m'
BOLD='\033[1m'
GRAY='\033[2m'
ITALIC='\033[3m'

printf "${BLUE}${BOLD}    ______      __               ${END}\n"
printf "${BLUE}${BOLD}   / ____/___  / /_  ___________ ${END}\n"
printf "${BLUE}${BOLD}  / /   / __ \/ __ \/ ___/ __ '/ ${END}\n"
printf "${BLUE}${BOLD} / /___/ /_/ / /_/ / /  / /_/ /  ${END}\n"
printf "${BLUE}${BOLD} \____/\____/_.___/_/   \__,_/   ${END}\n"

printf "${CYAN}${ITALIC}  >  OSS OSINT Tool${END}\n"
printf "Made with ${RED}love${END} by ${PURPLE}Alexeev Bronislav${END}\n\n"

printf "${ITALIC}${CYAN}Setup...${END}\n"

if [ ! -d venv ]; then
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
fi

printf "${GREEN}${BOLD}Setup completed${END}\n"

printf "${BOLD}Please, star repository: https://github.com/AlexeevDeveloper/cobra\n${END}"
