import urllib2
from bs4 import BeautifulSoup
import re, os

bookUrl = 'http://shamela.ws/index.php/book/'

# This function is called by the getUrl() function and is passed a url for the book page
# and this code gets that page, and looks for url for the online shamela reading app in order
# to extract the json data from there.


def getBook(bookUrls):
    
    while (count <= max ):
        url = bookUrls[count].split('/')
        bookId = url[-1].split('-')[-1]
        print bookId
        pageUrl = url[0] + '//' + url[2] + '/' + url[3] +  '/book/' + 'get_page/' + bookId + '/'
        print pageUrl
    #    while(urllib2.urlopen(pageUrl + str(count)).getcode() == 200):
    #        page = urllib2.urlopen(pageUrl + str(count)).read()
    #        print page
    #        count += 1
        count = count + 1
	

# This function is responsible for reading the urls that are stored in a text file.


def getUrl():
    global data
    global count
    global bookUrls
    global max
    bookUrls = []
    count = 0
    try:
#		Reading from file that contains urls for the books
        f = open('url.txt', 'r')

#		extract url and names for each book and put in list
        data = f.readlines()
        for line in data:
#			store regex pattern in page
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            url = urls[0]
            authorPage = urllib2.urlopen(url).read()
            links = re.findall('http://shamela.ws(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', authorPage)
            bookUrl = links[2]
            bookUrls.append(bookUrl)
        max = len(bookUrls)
        print max            
        getBook(bookUrls)
        
           
    except IOError:
        pass



getUrl()