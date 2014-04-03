import urllib2
from bs4 import BeautifulSoup
#import simplejson
import threading

global count
global page
global book
# maximum page == 5355
book = 
count = 5355
page = 1001

def fetch(page):
	
	
	file = open('pages.txt', 'a+')
	
	url = 'http://shamela.ws/browse.php/book/get_page/' + str(book) + '/' + str(page)
	webpage = urllib2.urlopen(url).read()

	file.write('\n{ "index" : { "_index" : "books", "_type" : "book_one", "_id" : "' + str(page) + '" } }\n' + str(webpage))

	
	
	
while count >= page:
	aThread = threading.Thread(target=fetch(page))
	aThread.start()

	page += 1


#file.close()
print threading.active_count()
