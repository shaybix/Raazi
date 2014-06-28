from bs4 import BeautifulSoup
import urllib2
import time

path = "http://shamela.ws/index.php/author/"
website = "http://shamela.ws"



def getAuthor():
	author_id = 1
	count = 1
	max = 20
	
	file = open('authors.txt', 'wb')
	
	while (count <= max):
		
		url = urllib2.urlopen(path + str(author_id))
		html = BeautifulSoup(url)
		title_tag = html.h3
		author_id = author_id + 1
		print title_tag.text + "  " + "[" + str(count) + "]"
		author_name =  title_tag.text + "  " + "[" + str(count) + "]"
		encoded = author_name.encode('utf-16')
		file.write(encoded)
		link_tag = html.table.find_all('li')
		
		for i in link_tag:
			print i.text +  " - " + website + i.a['href']
			data =  i.text +  " - " + website + i.a['href']§§§
			data = data.encode('utf-16')
			file.write(data)
			
		count = count + 1
		
		print "\n\n"
		
		time.sleep(2)
	file.close()
		
		
getAuthor()