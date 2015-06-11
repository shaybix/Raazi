import urllib2
import urllib
from bs4 import BeautifulSoup
import subprocess
import os
import rarfile





names = open('urls.txt', 'r').read()
urls = open('urls.txt', 'r').read()
# f = open('downloads.txt', 'a+')

names = names.splitlines()
urls = urls.splitlines()
urls = urls[0:19]
count = 0
for url in urls:

    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    link = soup.find(id='content').contents[11].a.get('href')


    print link
    subprocess.call(['wget', '-r', '-nd', '-P', 'downloads', link])
    # if not os.path.isfile("downloads/" + name + ".rar"):



    count += 1


# TODO add functionality for unrar and rename bok file



directory = 'downloads/'
dest = 'bok/'
files = []


def unrar(file):
    rf = rarfile.RarFile(file)
    file = file.replace('rar', 'bok')
    file = file.replace(directory, dest)
    if not os.path.isfile(file):
        for names in rf.infolist():
            name = names.filename
        rf.extract(name)

        subprocess.call(['mv', name, file])


for (dirpath, dirnames, filenames) in os.walk(directory):
    files.extend(filenames)

    if os.path.isfile('downloads/.DS_Store'):
        files.remove('.DS_Store')
    count = 0

    while count < len(files):
        for file in files:
            unrar(directory + file)
            print 'Extracting file ' + file + '.............. - DONE!'
            count += 1

    pass

    # TODO exception handling and timing out of connection


    # TODO perhaps extract the script out with extract.py and refactor the code?
