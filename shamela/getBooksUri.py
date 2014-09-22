#!/usr/bin/env python


import urllib2
from bs4 import BeautifulSoup
import os


baseUrl = 'http://shamela.ws/index.php/book/'




def fetch():


    urls = []
    count = 164242 


    while (count < 1000000 ):
        file = open('urls.txt', 'a+')
        try:
            uri = baseUrl + str(count)
            url = urllib2.urlopen(uri)
            print uri
            file.write(uri + '\n')
            
            
        except urllib2.URLError, e:

                if e.code == 404:
                    print str(count) +" Page not found!"

                elif e.code == 403:
                    print "Access Denied!"

                else:
                    print "Something happened! Error code: ", e.reason
                    return False
        file.close()

        count = count + 1
    
fetch()


