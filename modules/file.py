import xlrd
import csv
import requests
from bs4 import BeautifulSoup

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

def file():
	global file
	file = input(C + '[+] ' + G + 'Please Enter File Name or Location -> ')
	if 'txt' in str(file):
		Text()
	elif 'csv' in str(file):
		CSV()
	elif 'xlsx' in str(file):
		Excel()
	else:
		print(R +"[!] File Type Is Not Supported." + W )

def Text():
	with open(file, 'r') as torfile:
		torfile = torfile.readlines()
		for res in torfile:
			response = session.get(res).text
			soup = BeautifulSoup(response, 'lxml')
			tags = soup.find_all('img')
			for tag in tags:
				url = tag.get('src')
			print(C + "[>] " + W + url + '\n')

def Excel():
	workbook = xlrd.open_workbook('{}'.format(file))
	sh = workbook.sheet_names()
	print(G + '[>]' + C + ' Sheet Names -> {}'.format(sh))
	shn = input(C + '[+] ' + G + 'Please Enter the Sheet Name For Urls -> ')
	worksheet = workbook.sheet_by_name('{}'.format(shn))
	total_rows = worksheet.nrows
	total_cols = worksheet.ncols
	record = []
	for x in range(total_rows):
		for y in range(total_cols):
			record.append(worksheet.cell(x,y).value)
	for url in record:
		if '.onion' in url:
			print('\n' + C + '[>] ' + G + 'Scrapping Url -> ' + R + '{}'.format(url) + W)
			try:
				try:
					response = session.get('http://'+url).text
					soup = BeautifulSoup(response, 'lxml' )
					tags = soup.find_all('img')
					for tag in tags:
						url = tag.get('src')
						print(C + "[>] " + W + str(url))
				except requests.exceptions.ConnectionError as e:
					print( '\n' + R +'[!] Connection Error in {}'.format(url) + W)
					pass
			except requests.exceptions.InvalidURL as e:
				print( '\n' + R +'[!] Invalid URL{}'.format(torurl) + W)
				pass

	
