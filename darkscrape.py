#!/usr/bin/env python3
from modules.file import file
from modules.url import url
import requests
import subprocess as subp

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white


version = '1.3'

def banner():
	banner = r'''
	______           _    _____                           
	|  _  \         | |  /  ___|                          
	| | | |__ _ _ __| | _\ `--.  ___ _ __ __ _ _ __   ___ 
	| | | / _` | '__| |/ /`--. \/ __| '__/ _` | '_ \ / _ \
	| |/ / (_| | |  |   </\__/ / (__| | | (_| | |_) |  __/
	|___/ \__,_|_|  |_|\_\____/ \___|_|  \__,_| .__/ \___|
	                                          | |         
	                                          |_|'''
	print(G + banner + W)
	print(R + "Created By :- " + G + "Hacker Destination" +W)
	print(R + "Version :- " + G + version + W + '\n')

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

def updater():
	print (G + '[+]' + R + ' Checking for updates...' + W + '\n')
	updated_version = requests.get('https://raw.githubusercontent.com/itsmehacker/DarkScrape/master/version.txt', timeout = 5)
	updated_version = updated_version.text.split(' ')[1]
	updated_version = updated_version.strip()
	if updated_version != version:
		print (G + '[!]' + R + ' A New Version is Available : ' + W + updated_version)
		ans = input(G + '[!]' + R + ' Update ? [y/n] : ' + W)
		if ans == 'y':
			print ('\n' + G + '[+]' + R + ' Updating...' + '\n' + W)
			subp.check_output(['git', 'reset', '--hard', 'origin/master'])
			subp.check_output(['git', 'pull'])
			print (G + '[+]' + R + ' Script Updated...Please Execute Again...' + W)
			exit()
	else:
		print (G + '[+]' + R + ' Script is up-to-date...' + '\n' + W)
	

def service():
	print('\n' + C + "[>] Checking for tor service..." + W + '\n')
	cmd = 'systemctl is-active tor.service'
	co = subp.Popen(cmd, shell=True,stdout=subp.PIPE).communicate()[0]
	if 'inactive' in str(co):
		print(R + '[!] Tor Service Not Running..' + W + '\n')
		print(R + '[>] Tor Service is Required for this Script...')
		exit()
	else:
		print(C + "[>] Tor Service is Running..."  + W + '\n')



def scrap():
	r= session.get("http://icanhazip.com").text
	print(R + '[+]' + G  + ' Connected to Tor...')
	print(R + '[+]' + G  + ' Your Tor IP -> {}'.format(r))

def main():
	choice ='0'
	while choice =='0':
		print(R + '[+] ' + G +  'Choose the File Format:-' + W)
		print(R + '[1] ' + G +  'Scrape From File'  + W)
		print(R + '[2] ' + G +  'Scrape From Single URL'  + W + '\n')
		choice = input (G + '[+]' + C + " Enter Option No. ->  " + W)

		if choice == "2":
			url()
		elif choice == "1":
			file()
		else:
			print('\n' + R + "[!] I don't understand your choice." + W + '\n')
			return main()	

try:
	banner()
	updater()
	service()
	scrap()
	main()
except KeyboardInterrupt:
	print ('\n' + R + '[!]' + R + ' Keyboard Interrupt.' + W)
	exit()
