#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
import re, os

global data
global bookUrls
global total
global pageCount
global count
count = 14 
pageCount = 237
bookUrl = 'http://shamela.ws/index.php/book/'
bookBase = 'http://shamela.ws/browse.php/book-'

'''

This function is called by the getUrl() function and is passed a url for the book page
and this code gets that page, and looks for url for the online shamela reading app in order
to extract the json data from there.  Important!


'''

def getBook(bookUrls, count, pageCount, total):

    
    file = open('index5.txt', 'a+')
    
    while (count < total ):
        
        print "Currently getting Book: " + str(count) + "/" + str(total)
        url = bookUrls[count].split('/')
        bookId = url[-1].split('-')[-1]
        pageUrl = url[0] + '//' + url[2] + '/' + url[3] +  '/book/' + 'get_page/' + bookId + '/'

#        print pageUrl

        while urllib2.urlopen(pageUrl + str(pageCount)).getcode() == 200:
            
            page = urllib2.urlopen(pageUrl + str(pageCount)).read()
            index = '\n{ "index" : { "_index" : "books", "_type" : "tafsir", "_id" : "' + "b" + str(bookId) + "_p" + str(pageCount) + "_" + str(count) + '" } }\n' + str(page)
            file.write('\n{ "index" : { "_index" : "books", "_type" : "tafsir", "_id" : "' + "b" + str(bookId) + "_p" + str(pageCount) + "_" + str(count) + '" } }\n' + str(page))
            print index
            pageCount += 1
            
            try:
                
                urllib2.urlopen(pageUrl + str(pageCount)).getcode()
                
            except urllib2.URLError, e:

                if e.code == 500:
                    count += 1
                    pageCount = 1
                    file.close()
                    getBook(bookUrls, count, pageCount, total)

                else:
                    print "Something happened! Error code: ", e.reason
                    return False

#        print "Book Count = " + str(count) + " " + "Page Count = " + str(pageCount)
        else:
            print "This attempt number " + count


	

# This function is responsible for reading the urls that are stored in a text file.


def getUrl():

    bookUrls = []
  
    try:
#		Reading from file that contains urls for the books
        f = open('url.txt', 'r')

#		extract url and names for each book and put in list
        data = f.readlines()
        for line in data:
#			store regex pattern in page
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
#            url = urls[0]
#            authorPage = urllib2.urlopen(url).read()
#            links = re.findall('http://shamela.ws(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', authorPage)
#            bookUrl = links[2]
            url = urls[0].split('/')
            bookUrl = bookBase + url[-1]
            bookUrls.append(bookUrl)
        total = len(bookUrls)
        getBook(bookUrls, count, pageCount, total)
        
           
    except IOError:
        pass



getUrl()
