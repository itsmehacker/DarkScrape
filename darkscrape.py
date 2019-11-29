#!/usr/bin/env python3
import subprocess as subp
import requests
from modules.file import choose_file
from modules.url import parse_url

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white


VERSION = '1.6'

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
    print(R + "Version :- " + G + VERSION + W + '\n')

SESSION = requests.session()
SESSION.proxies = {}
SESSION.proxies['http'] = 'socks5h://localhost:9050'
SESSION.proxies['https'] = 'socks5h://localhost:9050'



def service():
    """
    Ensures Tor service is running before proceeding
    """
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
    r = SESSION.get("http://icanhazip.com").text
    print(R + '[+]' + G  + ' Connected to Tor...')
    print(R + '[+]' + G  + ' Your Tor IP -> {}'.format(r))

def main():
    """
    Presents options for scraping from single URL or file type
    """
    choice = '0'
    while choice == '0':
        print(R + '[+] ' + G +  'Choose the File Format:-' + W)
        print(R + '[1] ' + G +  'Scrape From File'  + W)
        print(R + '[2] ' + G +  'Scrape From Single URL'  + W + '\n')
        choice = input(G + '[+]' + C + " Enter Option No. ->  " + W)

        if choice == "1":
            choose_file()
        elif choice == "2":
            parse_url()
        else:
            print('\n' + R + "[!] I don't understand your choice." + W + '\n')
            return main()

try:
    banner()
    service()
    scrap()
    main()
except KeyboardInterrupt:
    print('\n' + R + '[!]' + R + ' Keyboard Interrupt.' + W)
    exit()
