import requests
from bs4 import BeautifulSoup
import subprocess as subp
import os

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

def url():
	url_media = []
	try:
		try:
			torurl = input(C + '[+] '+ G + 'Please Enter URL -> ' +W)
			response = session.get('http://' +torurl).text
			soup = BeautifulSoup(response, 'lxml')
			tags = soup.find_all('img')
			for tag in tags:
				urls = tag.get('src')
				media = 'http://'+torurl+'/'+str(urls)				
				url_media.append(media)
				print(C + "[>] " + W + str(urls))
			down = input(C + '[+] '+ G + 'Download Media (y/n) -> ')
			torurl1 = torurl.replace('.','-')
			if down =='y':
				os.system('mkdir Media/{}'.format(torurl1))
				for item in url_media:
					m = item.split('/')[-1]
					if '.png' or '.jpg' or '.gif' in m:
						r =session.get(item)
						with open('Media/{}/{}'.format(torurl1,m), 'wb') as f:
							f.write(r.content)
				print('\n' + C + '[>] All Media Downloaded -> ' + G + 'Media/'+torurl1 + W)
			else:
				print('\n' + R + '[!] Exiting...')
				exit()
		except requests.exceptions.ConnectionError as e:
			print( '\n' + R +'[!] Connection Error in {}'.format(torurl) + W)
			pass
	except requests.exceptions.InvalidURL as e:
			print( '\n' + R +'[!] Invalid URL{}'.format(torurl) + W)
			pass

