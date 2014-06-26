from bs4 import BeautifulSoup
import urllib2

website = "http://shamela.ws"
path = "http://shamela.ws/index.php/author/"
author_id = 20


url = urllib2.urlopen(path + str(author_id))
html = BeautifulSoup(url)
link_tag = html.table.find_all('li')




for i in link_tag:
	print i.text +  " - " + website + i.a['href']