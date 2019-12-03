import subprocess as subp
import os
import requests
from bs4 import BeautifulSoup

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m' # white

def parse_url():
    """
    Scrapes website url defined by user
    """
    url_media = []
    try:
        try:
            torurl = input(C + '[+] '+ G + 'Please Enter URL -> ' +W)
            if 'http://' in torurl:
                response = session.get(torurl).text
            else:
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
            if down == 'y':
                os.system('mkdir Media/{}'.format(torurl1))
                for item in url_media:
                    m = item.split('/')[-1]
                    if '.png' or '.jpg' or '.gif' in m:
                        r = session.get(item)
                        with open('Media/{}/{}'.format(torurl1,m), 'wb') as f:
                            f.write(r.content)
                print('\n' + C + '[>] All Media Downloaded -> ' + G + 'Media/'+torurl1 + W)
            else:
                print('\n' + R + '[!] Exiting...')
                exit()
        except requests.exceptions.ConnectionError as e:
            print('\n' + R +'[!] Connection Error in {}'.format(torurl) + W)
            pass
    except requests.exceptions.InvalidURL as e:
        print('\n' + R +'[!] Invalid URL{}'.format(torurl) + W)
        pass

def face_re():
    known_folder = input(C + '[+] '+ G + 'Enter the Known Images Folder Name or Location -> ')
    unknown_folder = input(C + '[+] '+ G + 'Enter the Check Images Folder Name or Location -> ')
    search = subp.Popen(['face_recognition', '{}'.format(known_folder), '{}'.format(unknown_folder)], stdout=subp.PIPE, stderr=subp.PIPE)
    output = search.communicate()[0].decode('utf-8')
    output = output.splitlines()
    for name in output:
        if 'person' in name:
            pass
        else:
            name = name.split(',')[1]
            print('\n' + C + '[>]' + G + 'Image Founded -> '+ R +'{}'.format(name)+W)
