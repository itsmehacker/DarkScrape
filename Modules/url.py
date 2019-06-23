import requests
from bs4 import BeautifulSoup
import subprocess as subp

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

def url():
	try:
		try:
			torurl = input(C + '[+] '+ G + 'Please Enter URL -> ')
			response = session.get('http://' +torurl).text
			soup = BeautifulSoup(response, 'lxml')
			tags = soup.find_all('img')
			for tag in tags:
				urls = tag.get('src')
				me = urls.split('/')
				print(C + "[>] " + W + str(urls))
		except requests.exceptions.ConnectionError as e:
			print( '\n' + R +'[!] Connection Error in {}'.format(torurl) + W)
			pass
	except requests.exceptions.InvalidURL as e:
			print( '\n' + R +'[!] Invalid URL{}'.format(torurl) + W)
			pass

