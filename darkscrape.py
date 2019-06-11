import socks 
import socket
import requests
from bs4 import BeautifulSoup

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

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
	print(R + "Version :- " + G + "1.0" + W + '\n')

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'


def scrap():
	r= session.get("http://icanhazip.com").text
	print(R + '[+]' + G  + ' Connected to Tor...')
	print(R + '[+]' + G  + ' Your Tor IP -> {}'.format(r))
	print(R + '[+]' + G  + ' Starting the Website Scraping' + "\n")
	

	file = 'test.txt' #file name
	
	with open(file, 'r') as torfile:
		torfile = torfile.readlines()
		for res in torfile:
			response = session.get(res).text
			soup = BeautifulSoup(response, 'lxml')
			tags = soup.find_all('img')
			for tag in tags:
				print(C + "[>] " + W + tag.get('src'))

try:
	banner()
	scrap()
except KeyboardInterrupt:
	print ('\n' + R + '[!]' + R + ' Keyboard Interrupt.' + W)
	exit()