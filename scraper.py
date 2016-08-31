#!/usr/bin/python3

import requests
import argparse
import re
import os

parser = argparse.ArgumentParser(description='Download comics from 8muses.com')
parser.add_argument("-u", help="Url")
args = parser.parse_args()
home = os.getenv("HOME")
download_dir = '{0}/Pictures/porncomics'.format(home)
comic_dir = args.u.split('/')[5]


useragent = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)'}

url = args.u
# Here we grab the page the user passed with -u
page = requests.get(url, headers = useragent).text
# print(page)


if url[-1:] == '/':
    url = url[:-1]
else:
    pass

url_split = url.split('/')[5]

comic_pages_list = re.findall('/picture/\d+/[a-zA-Z0-9_-]*/[a-zA-Z0-9_-]*/\d+', page)
# print(comic_pages_list)
x = 1
for i in comic_pages_list:
    print("grabbing {0}".format('http://8muses.com' + i))
    comic_page = requests.get('http://8muses.com' + i).text
    pictures = re.findall('[a-zA-Z0-9\-_+]*\.(?:jpg|gif|png)', comic_page)
    for u in pictures:
        if len(u) == 73 or len(u) > 73:
            comic_url = "https://www.8muses.com/data/fu/small/" + u
            print(comic_url)
            comic_page_number = "{0}-{1}".format(x, u)
            file_path = "{0}/{1}".format(download_dir, url_split)
            file_download_path = "{0}/{1}/{2}".format(download_dir, url_split, comic_page_number)
            if os.path.isdir(download_dir) == False:
                file_path = url_split
                file_download_path = "{0}/{1}".format(url_split, comic_page_number)
            if os.path.isdir(file_path):
                pass
            else:
                os.mkdir(file_path)
            r = requests.get(comic_url, stream=True)
            with open(file_download_path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            x = x + 1
