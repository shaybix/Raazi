import urllib2
from bs4 import BeautifulSoup

categoryUrl = 'http://shamela.ws/index.php/category/'
bookUrl = 'http://shamela.ws/index.php/book/'


def main(category=127):
    try:
        f = open('url.txt', 'w')

        html = urllib2.urlopen(categoryUrl + str(category)).read()
        html = BeautifulSoup(html)
        html = html.table.select('td')
        count = 1
        for each in html:
            each = each.a

            each = "[" + str(count) + "] " + each.string + " | " + "http://shamela.ws" + each['href'] + "\n"
            print each
            f.write(each.encode('utf-8'))
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



main()