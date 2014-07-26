import sqlite3
import json
import sys
import subprocess
from optparse import OptionParser

# import elasticsearch


def index():
    """
    :rtype : object
    """

    # TODO automate process for indexing the document into Elasticsearch

    pass


def export(DATABASE, filename):
    """
    :type filename: str
    :type DATABASE: str
    :param filename:
    :param DATABASE:
    :rtype : object
    """


    # TODO accept bok file as param and begin and convert to sqlite3

    pass


def fetch_main():
    """
    THE FUNCTION IS RESPONSIBLE FOR RETRIEVING THE FOLLOWING FIELDS:

    [BkId]			Long Integer,
    [Bk]			Memo/Hyperlink (255),
    [Betaka]			Memo/Hyperlink (255),
    [Inf]			Memo/Hyperlink (255),
    [Auth]			Memo/Hyperlink (255),
    [AuthInf]			Memo/Hyperlink (255),
    [cat]			Memo/Hyperlink (255),
    [AD]			Long Integer,

    :rtype : object
    """


    c.execute('SELECT BkId, Bk, Betaka, Inf, Auth, AuthInf, cat, AD FROM main')

    result = c.fetchall()[0]

    book_id = str(result[0])

    content = dict(book_id=str(result[0]), book_title=result[1], info=result[2], book_info=result[3], author=result[4],
                   author_bio=result[5], category=result[6], died=str(result[7]),
                   body=fetch_body(book_id), chapters=fetch_chapters(book_id))

    return json.dumps(content)


def fetch_body(book_id):
    """

    THE FUNCTION IS RESPONSIBLE FOR RETRIEVING USING THE ID OF A BOOK - THE FOLLOWING FIELDS:

    [nass]			Memo/Hyperlink (255),
    [id]			Integer,
    [part]			Byte,
    [page]			Integer

    :rtype : list
    :type book_id: int
    :param book_id:
    """

    c.execute('SELECT id, nass, part, page FROM b' + str(book_id) + '')
    result = c.fetchall()
    body = []

    for row in result:
        page = dict(page_id=str(row[0]), page_body=row[1], volume=row[2], page_number=str(row[3]))

        body.append(page)
    return body


def fetch_chapters(book_id):
    """
    FUNCTIONALITY FOR RETRIEVING THE CHAPTERS AND HEADINGS AND THEIR DATA FROM THEIR TABLE IN THE DB.

    [tit]			Memo/Hyperlink (255),
    [lvl]			Byte,
    [sub]			Byte,
    [id]			Integer <- page_id

    :type book_id: int
    :rtype : object
    :param book_id:
    """

    c.execute('SELECT tit, lvl, sub, id FROM t' + str(book_id) + '')

    result = c.fetchall()
    chapters = []

    for row in result:
        chapter = dict(heading=row[0], heading_level=str(row[1]), sub_level=str(row[2]), page_id=str(row[3]))

        chapters.append(chapter)

    return chapters


def validator(arguments):
    """

    Get the arguments passed through the commandline, and validate.

    :type arguments: list
    :param arguments:
    :rtype : object
    """

    # TODO validate the arguments passed through and return
    parser = OptionParser()

    pass


conn = sqlite3.connect('sample.sqlite3')
c = conn.cursor()

if __name__ == "__main__":

    # TODO create an arguments validator
    pass