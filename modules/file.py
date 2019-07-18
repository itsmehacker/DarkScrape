#!/usr/bin/env python3
import xlrd
import csv
import requests
from bs4 import BeautifulSoup
import os
import subprocess as subp
import face_recognition


R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

url_media = []
foln = []
results = []
record = []
fol = ''

def file():
	global file
	file = input(C + '[+] ' + G + 'Please Enter File Name or Location -> ')
	if '.txt' in str(file):
		Text()
	elif '.csv' in str(file):
		Csv()
	elif '.xlsx' in str(file):
		Excel()
	else:
		print(R +"[!] File Type Is Not Supported." + W )

def Text():
	with open(file, 'r') as torfile:
		torfile = torfile.readlines()
		url2 = [x.replace('\n', '') for x in torfile]
		try:
			try:
				for res in url2:
					print('\n' + C + '[>] ' + G + 'Scraping Url -> ' + R + '{}'.format(res) + W)
					if 'http://' in url2:
						response = session.get(res, HTTPAdapter(max_retries=5)).text
					else:
						response = session.get('http://'+res).text
					soup = BeautifulSoup(response, 'lxml')
					tags = soup.find_all('img')
					if len(tags) < 1:
						print(R + '[!] No Media Found...' +W)
						url2.remove(res)
						pass
					for tag in tags:
						urls = tag.get('src')
						media = 'http://'+str(res)+'/'+str(urls)
						if 'http://' and '//' in  media:
							media = media.replace('//','/')
							media = media.replace('https://', 'http://')
							print(C + "[>] " + W + str(urls))
						media = 'http://'+str(res)+'/'+str(urls)
						if 'http://' and '//' in  media:
							media = media.replace('//','/')
							media = media.replace('http:/', 'http://')
						url_media.append(media)
			except requests.exceptions.ConnectionError as e:
				print( '\n' + R +'[!] Connection Error in {}'.format(res) + W)
				pass
		except requests.exceptions.InvalidURL as e:
			print( '\n' + R +'[!] Invalid URL{}'.format(res) + W)
			pass		
	down = input(C + '[+] '+ G + 'Download Media (y/n) -> ')
	if down == 'y':
		Download()
	else:
		print(R  + '[!] Exiting...' + W)
		exit()	

def Csv():
	with open(file, newline='') as inputfile:
		for row in csv.reader(inputfile):
			results.append(row[0])
		for res in results:
			print('\n' + C + '[>] ' + G + 'Scraping Url -> ' + R + '{}'.format(res) + W)
			try:
				try:
					if 'http://' in res:
						response = session.get(res).text
					else:
						response = session.get('http://'+res).text
					soup = BeautifulSoup(response, 'lxml' )
					tags = soup.find_all('img')
					for tag in tags:
						url = tag.get('src')
						print(C + "[>] " + W + str(urls))
						media = 'http://'+str(res)+'/'+str(urls)
						if 'http://' and '//' in  media:
							media = media.replace('//','/')
							media = media.replace('http:/', 'http://')
						url_media.append(media)
				except requests.exceptions.ConnectionError as e:
					print( '\n' + R +'[!] Connection Error in {}'.format(res) + W)
					pass
			except requests.exceptions.InvalidURL as e:
				print( '\n' + R +'[!] Invalid URL{}'.format(res) + W)
				pass	
	total_img = print('\n' + R + '[>] ' + G + 'Total Images -> {}'.format(len(media)))	
	down = input(C + '[+] '+ G + 'Download Media (y/n) -> ')
	if down == 'y':
		Download()
	else:
		print(R  + '[!] Exiting...' + W)
		exit()

		
def Excel():
	workbook = xlrd.open_workbook('{}'.format(file))
	sh = workbook.sheet_names()
	print(G + '[>]' + C + ' Sheet Names -> {}'.format(sh) + W)
	shn = input(C + '[+] ' + G + 'Please Enter the Sheet Name For Urls -> ' +W)
	worksheet = workbook.sheet_by_name('{}'.format(shn))
	total_rows = worksheet.nrows
	total_cols = worksheet.ncols
	for x in range(total_rows):
		for y in range(total_cols):
			record.append(worksheet.cell(x,y).value)
	for res in record:
		if '.onion' in res:
			print('\n' + C + '[>] ' + G + 'Scraping Url -> ' + R + '{}'.format(res) + W)
			try:
				try:
					if 'http://' in res:
						response = session.get(res).text
					else:
						response = session.get('http://'+res).text
					soup = BeautifulSoup(response, 'lxml' )
					tags = soup.find_all('img')
					if len(tags) < 1:
							print(R + '[!] No Media Found...' +W)
							record.remove(res)
					for tag in tags:
						urls = tag.get('src')
						print(C + "[>] " + W + str(urls))
						media = 'http://'+str(res)+'/'+str(urls)
						if 'http://' and '//' in  media:
							media = media.replace('//','/')
							media = media.replace('http:/', 'http://')
						url_media.append(media)
				except requests.exceptions.ConnectionError as e:
					print( '\n' + R +'[!] Connection Error in {}'.format(res) + W)
					pass
			except requests.exceptions.InvalidURL as e:
				print( '\n' + R +'[!] Invalid URL{}'.format(res) + W)
				pass	
	total_img = print('\n' + R + '[>] ' + G + 'Total Images -> {}'.format(len(media)))	
	down = input(C + '[+] '+ G + 'Download Media (y/n) -> ')
	if down == 'y':
		Download()
	else:
		print(R  + '[!] Exiting...' + W)
		exit()



def Download():
	global fol
	fol = input('\n' + R + '[>] ' + G + 'Enter Folder Name -> ' +W)
	os.system('mkdir Media/{}'.format(fol))
	for item in url_media:
		m = item.split('/')[-1]
		if '.png' or '.jpg' or '.gif' in m:
			r =session.get(item)
			with open('Media/{}/{}'.format(fol,m), 'wb') as f:
				f.write(r.content)
	print('\n' + C + '[>] ' + R + 'All Files Downloaded in Media/{}'.format(fol) +W)
	face = input(C + '[+] '+ G + 'Do You What To Search Image (y/n) -> ')
	if face == 'y':
		face_re()
	else:
		print(R  + '[!] Exiting...' + W)
		exit()


def face_re():
	known_folder = input(C + '[+] '+ G + 'Enter the Known Images Folder Name or Location -> ')
	unknown_folder =input(C + '[+] '+ G + 'Enter the Check Images Folder Name or Location -> ')
	search = subp.Popen(['face_recognition', '{}'.format(known_folder), '{}'.format(unknown_folder)], stdout=subp.PIPE, stderr=subp.PIPE)
	output = search.communicate()[0].decode('utf-8')
	output = output.splitlines()
	for name in output:
		if 'person' in name:
			pass
		else:
			name = name.split(',')[1]
			print('\n' + C + '[>]' + G + 'Image Founded -> '+ R +'{}'.format(name)+W)