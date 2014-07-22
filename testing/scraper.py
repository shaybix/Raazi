import urllib2
from bs4 import BeautifulSoup
import re, os

categoryUrl = 'http://shamela.ws/index.php/category/'
bookUrl = 'http://shamela.ws/index.php/book/'



# This function is responsible for loading an entire category page and scrape
# the entire listing for the title of the book and url and store them in a txt file.


def getCategory(category=127):
    try:
        f = open('url.txt', 'w')

        html = urllib2.urlopen(categoryUrl + str(category)).read()
        html = BeautifulSoup(html)
        html = html.table.select('td')
        count = 1
        for each in html:
            each = each.a
            
            print each.string

#            each = "[" + str(count) + "] " + each.string + " | " + "http://shamela.ws" + each['href'] + "\n"
#            print each
#            f.write(each.encode('utf-8'))
            count += 1
        f.close()
    except urllib2.URLError, e:

        if e.code == 404:
            print "Page not found!"

        elif e.code == 403:
            print "Access Denied!"

        else:
            print "Something happened! Error code: ", e.reason
            return False


# This function is called by the getUrl() function and is passed a url for the book page
# and this code gets that page, and looks for url for the online shamela reading app in order
# to extract the json data from there.


def getBook(bookUrl):
    count = 1
    url = bookUrl.split('/')
    pageUrl = url[0] + '//' + url[2] + '/' + url[3] +  '/book/' + 'get_page/' + url[-1].split('-')[-1] + '/'
    print pageUrl
    while(urllib2.urlopen(pageUrl + str(count)).getcode() == 200):
        page = urllib2.urlopen(pageUrl + str(count)).read()
        print page
        count += 1



# This function is responsible for reading the urls that are stored in a text file.


def getUrl():
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

            getBook(bookUrl)

            return 0
    except IOError:
        pass



# Still work in progress, but function receives data and stores each book in its own .txt file
# ready for ElasticSearch Bulk indexing.

def storeData(data):

    directory = '/data'

    if not os.path.exists(directory):
        print 'data exists!'
        file = open(bookId + '.txt', 'w')


    else:
        print "data doesn't exist"






getCategory()
#getUrl()

#storeData('hello world')