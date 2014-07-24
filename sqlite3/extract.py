import sqlite3

author = None  # done
authorInfo = None  # done
bookTitle = None  # done
bookId = None  # done
bookVolumes = None  # done
bookInfo = None  # done
category = None  # done
publisher = None  # done
authorDateOfDeath = None  # done
chapterTitle = None
chapterId = None
chapterLevel = None
page = None
pageId = None
volume = None
pageNumber = None
school = None


#This is an outline of the table 'main' inside the sqlite3 database
#
#0 - [BkId]			Long Integer,
#1 - [Bk]			Memo/Hyperlink (255),
#2 - [Betaka]			Memo/Hyperlink (255),
#3 - [Inf]			Memo/Hyperlink (255),
#4 - [Auth]			Memo/Hyperlink (255),
#5 - [AuthInf]			Memo/Hyperlink (255),
#6 - [TafseerNam]			Memo/Hyperlink (255),
#7 - [IslamShort]			Byte,
#8 - [oNum]			Long Integer,
#9 - [oVer]			Long Integer,
#10 - [seal]			Memo/Hyperlink (255),
#11 - [oAuth]			Long Integer,
#12 - [bVer]			Long Integer,
#13 - [Pdf]			Byte,
#14 - [oAuthVer]			Long Integer,
#15 - [verName]			Memo/Hyperlink (255),
#16 - [cat]			Memo/Hyperlink (255),
#17 - [Lng]			Memo/Hyperlink (255),
#18 - [HigriD]			Memo/Hyperlink (255),
#19 - [AD]			Long Integer,
#20 - [aSeal]			Memo/Hyperlink (255),
#21 - [bLnk]			Memo/Hyperlink (255),
#22 - [PdfCs]			Byte

def fetch_main():
    """
    THE FUNCTION IS RESPONSIBLE FOR RETRIEVING THE FOLLOWING FIELDS:
    #0 - [BkId]			Long Integer,
    #1 - [Bk]			Memo/Hyperlink (255),
    #2 - [Betaka]			Memo/Hyperlink (255),
    #3 - [Inf]			Memo/Hyperlink (255),
    #4 - [Auth]			Memo/Hyperlink (255),
    #5 - [AuthInf]			Memo/Hyperlink (255),
    #16 - [cat]			Memo/Hyperlink (255),
    #19 - [AD]			Long Integer,
    FROM THE 'MAIN' TABLE.
    """
    c.execute('SELECT BkId, Bk, Betaka, Inf, Auth, AuthInf, cat FROM main')

    result = c.fetchall()[0]

    book_id = result[0]
    book_title = result[1]
    info = result[2]
    book_info = result[3]
    author = result[4]
    author_bio = result[5]
    category = result[6]

    print "\nBook ID: " + str(book_id)
    print "\nTitle: " + book_title
    print "\nBook Info: " + book_info
    print "\nAuthor: " + author
    print "\nCategory: " + category
    print "\nAuthor Bio: " + author_bio


def fetch_body():

    pass


def fetch_
conn = sqlite3.connect('sample.sqlite3')

c = conn.cursor()

if __name__ == "__main__":
    fetch_main()

