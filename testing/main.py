#!/usr/bin/env python



"""

Extracting data from arabic .bok file and storing it in json format in preparation for elasticsearch's bulk indexing. 


Author: Aboo Shayba
Date: July 21, 2014


THE FOLLOWING STEPS NEED TO BE IMPLEMENTED!

1) unrar the file and rename the .bok file with the book ID as its name
2) Extract the names of the relevant tables and store in variables
3) Create a JSON Object with all the field names
4) Extract the various information from the tables, and store them in variables
5) Populate the json object with the variables.

"""

import sys, subprocess, os, re


##############################################
#                                            #
#        Initialising JSON fields            #
#                                            #
##############################################



author = None # done
authorInfo = None # done
bookTitle = None # done
bookId = None # done
bookVolumes = None # done
bookInfo = None # done
category = None # done
publisher = None # done
authorDateOfDeath = None # done
chapterTitle = None
chapterId = None
chapterLevel = None
page = None
pageId = None
volume = None
pageNumber = None
school = None

 
"""
Preparing the input arguments provided at the commandline. Expecting a .bok file.
"""
def extractBookId(data):
    data = data[0].splitlines()[-1]
    return data.split('\t')[-1]
    


DATABASE = "sample.bok" #sys.argv[1]
 
## Dump the schema for the DB
#schema = subprocess.check_output(["mdb-tables", DATABASE])
#
#tables = schema.split(' ')
#
#info = tables[4]
#
#pages = tables[2]
#
#
#print info
#print pages

#content = subprocess.Popen(["mdb-export", DATABASE, info], stdout=subprocess.PIPE).communicate()[0]
#
#print content
#                

"""
Extract all the table names and store the relevant table names in preparation for extracting data inside those tables.
"""

table_names = subprocess.Popen(["mdb-tables", "-1", DATABASE],stdout=subprocess.PIPE).communicate()[0]
table = table_names.splitlines()

mainTable = table[4]
pagesTable = table[2]
chaptersTable = table[-1]

#print chaptersTable

content = subprocess.Popen(["mdb-array", DATABASE, mainTable], stdout=subprocess.PIPE).communicate()[0]

content = content.split(',')

#print content[0].splitlines()[-1]


bookId = int(extractBookId(content))
category = content[16].split('\n')[-1].split('\t')[-1].replace('"', '')
bookLargeInfo = content[2]
bookTitle = bookLargeInfo.splitlines()[1].split(':')[-1]
#author = bookLargeInfo.splitlines()[2]
author = content[17].split('\n')[1].split('\t')[-1].replace('"', '')
publisher = bookLargeInfo.splitlines()[3]
bookVolumes = bookLargeInfo.splitlines()[5].split(':')[-1]
authorInfo = content[5]#.replace('\n', " ")
bookInfo = content[3]
authorDateOfDeath = content[-5:][1].splitlines()[-1].split('\t')[-1]
#print authorDateOfDeath
#
#
#print "BookID: " + bookId
#print "Title: " + bookTitle
#print "Category: " + category
#print "Book Info: " + bookInfo
#print "Volumes: " + bookVolumes
#print "Author: " + author
#print "Author Info: " + authorInfo
#print "D.O.D: " + authorDateOfDeath


content = subprocess.Popen(["mdb-array", DATABASE, pagesTable], stdout=subprocess.PIPE).communicate()[0]

content = content.split('},')

pages = []


for page in content:
    page = re.sub(r'{.+', '' ,page)
    page = page.split(',')
    pages.append(page)

#print content[4]
print pages[0]
#print content[]