import urllib2
import urllib
from bs4 import BeautifulSoup
import subprocess
import os

urls = open('downloads.txt', 'r').read()
names = open('urls.txt', 'r').read()
# f = open('downloads.txt', 'a+')

names = names.splitlines()
urls = urls.splitlines()
count = 0
for url in urls:

    # html = urllib2.urlopen(url).read()
    # soup = BeautifulSoup(html)
    # link = soup.find(id='content').contents[11].a.get('href')

    name = names[count].split('/')[-1]

    # f.write(link + '\n')
    # print link
    # subprocess.call(['wget', '-r', '-nd', '-P', 'downloads', link])
    if not os.path.isfile("downloads/" + name + ".rar"):
        download = urllib.URLopener()
        download.retrieve(url, 'downloads/' + name + ".rar")
        print name + ".rar"


    count += 1


    # TODO add functionality for unrar and rename bok file
    # TODO exception handling and timing out of connection
    # TODO perhaps extract the script out with extract.py and refactor the code?