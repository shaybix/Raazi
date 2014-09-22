import sqlite3
import json
import sys
import subprocess
import os
import codecs
from elasticsearch import Elasticsearch

from optparse import OptionParser

# TODO create way to index BOOK, AUTHOR, PAGES, CHAPTERS into their very own types
# TODO refactor the code to allow bulk indexing for every 1000-5000 pages

def fetch_main(c):
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


    :type sql_db: str
    :param sql_db:
    :rtype : str
    """



    c.execute('SELECT BkId, Bk, Betaka, Inf, Auth, AuthInf, cat, AD FROM main')

    result = c.fetchall()[0]

    book_id = result[0]
    book_title = result[1]
    info = result[2]
    book_info = result[3]
    author = result[4]

    author_bio = result[5]
    category = result[6]
    died = result[7]

    content = dict(book_id=book_id, book_title=result[1], info=result[2], book_info=result[3], author=result[4],
                   author_bio=result[5], category=result[6], died=result[7])
    # content = '{"book_id":' + book_id + ', "book_title":' + book_title + ', "info":' + info + ', "book_info":' + book_info + ',"author":' + author + ', "author_bio":' + author_bio + ', "category":' + category + ', "died":' + died + ', "body":'

    # print json.dumps(content)

    return content


def fetch_body(sql_db, book_id):
    """
    THE FUNCTION IS RESPONSIBLE FOR RETRIEVING USING THE ID OF A BOOK - THE FOLLOWING FIELDS:

    [nass]			Memo/Hyperlink (255),
    [id]			Integer,
    [part]			Byte,
    [page]			Integer

    :type book_id: int
    :param book_id:
    :type c: object
    :param c:
    :rtype : list
    """
    conn = sqlite3.connect(sql_db)
    c = conn.cursor()

    c.execute('SELECT id, nass, part, page FROM b' + str(book_id) + '')
    result = c.fetchall()
    body = []
    es = Elasticsearch()
    for row in result:

        try:
            page_id = row[0]
            page_body = row[1]
            volume =row[2]
            page_number = row[3]

            # page = dict(page_id=page_id, page_body=page_body, volume=volume, page_number=page_number,
            #             chapters=fetch_chapters(book_id, c), body=fetch_main(c))

            page = dict(page_id=page_id, page_body=page_body, volume=volume, page_number=page_number)

            es = Elasticsearch()

            es.index(index='maktabah', doc_type='books', id=str(book_id) + 'p' + str(page_id), body=page)

            print "Uploaded: " + str(book_id) + "p" + str(page_id)

        #     f.write(json.dumps(dict(index=dict(_index='maktabah', _type='books', _id=str(book_id) + 'p' + page_id))))
        #     f.write('\n')
        #     f.write(json.dumps(page))
        #     f.write('\n')
        except Exception, e:
            print e
            pass




def fetch_chapters(book_id, c):
    """
    FUNCTIONALITY FOR RETRIEVING THE CHAPTERS AND HEADINGS AND THEIR DATA FROM THEIR TABLE IN THE DB.

    [tit]			Memo/Hyperlink (255),
    [lvl]			Byte,
    [sub]			Byte,
    [id]			Integer <- page_id

    :type c: object
    :param c:
    :type book_id: int
    :param book_id:
    :rtype : list
    """

    c.execute('SELECT tit, lvl, sub, id FROM t' + str(book_id) + '')

    result = c.fetchall()
    chapters = []

    for row in result:
        heading = (row[0]) if (row[0]) else ''
        heading_level = row[1]
        sub_level = row[2]
        page_id = row[3]

        chapter = dict(heading=heading, heading_level=heading_level, sub_level=sub_level, page_id=page_id)

        chapters.append(chapter)

    return chapters


def db_init(bok_file):
    """
    initialise the db connection with sqlite3 and pass through connection object and filename

    :rtype : list
    :param bok_file:
    :return:
    """

    db_file = bok_file.split('.')[0]
    db_file = db_file.replace('bok', 'sql')
    db_file += ".db"
    print db_file
    connection = sqlite3.connect(db_file)
    return [connection, db_file]


def export(file):
    """
    takes a list as a parameter at the moment, and takes the bok filename and passes on to export
    as mysql creating an sqlite3 database with the same filename.


    :type files: list
    :rtype : str
    :param files:
    """


    # TODO needs refactoring as it accepts a list though not necessary!
    database = file
    DB = db_init(database)
    con = DB[0]
    sql_file = DB[1]
    c = con.cursor()

    os.environ['MDB_JET3_CHARSET'] = "cp1256"

    # Dump the schema for the DB
    print database
    print 'dumping msql schema....'

    reply = subprocess.Popen(["mdb-schema", database, "mysql"],
                             stdout=subprocess.PIPE).communicate()[0]

    c.executescript(reply)
    con.commit()

    table_names = subprocess.Popen(["mdb-tables", "-1", database],
                                   stdout=subprocess.PIPE).communicate()[0]

    tables = table_names.splitlines()

    print 'begin executing mysql....'

    c.execute("BEGIN;")

    sys.stdout.flush()

    for table in tables:
        if table != '':
            print 'dumping table -' + table + '....'

            reply = subprocess.Popen(["mdb-export", "-I", "mysql", database, table],
                                     stdout=subprocess.PIPE).communicate()[0]
            c.executescript(reply)

    print 'committing it all to the database....'

    con.commit()
    sys.stdout.flush()
    con.close()

    return sql_file


def extract_from_dir(directory):
    bok_files = []

    for (dirpath, dirnames, filenames) in os.walk(directory):
        bok_files.extend(filenames)

    return bok_files


DIR = 'bok/'

if __name__ == "__main__":

    files = extract_from_dir('bok')
    count = 0
    databases = extract_from_dir('sql')
    # print len(databases)
    # exit()
    if databases:
        try:
            last_index = files.index(databases[-1].split('.')[0] + ".bok")
            del files[0:last_index + 1]
        except Exception, e:
            print e

    for file in files:
        print "\n--------------- EXPORTING " + file + " -----------------\n"
        print DIR + file
        sql_file = export(DIR + file)
        id = file.split('.')[0]
        fetch_body(sql_file, id)


        # json_file = 'json/' + file.split('/')[0].split('.')[0] + '.txt'
        # f = codecs.open(json_file, 'w+')
        #
        # json_data = fetch_body(sql_file, id, f)
        # f.close()
        # json_file = '@' + json_file
        # output = subprocess.Popen(
        #     ['curl', '-s', '-XPOST', 'localhost:9200/_bulk', '--data-binary', json_file],
        #     stdout=subprocess.PIPE).communicate()[0]
        # print output



        #     files = export(validator())
        #     files = validator()
        #     json_data = fetch_main(sql_db)
        #     f = open(files[1], 'w+')
        #     f.write(json_data)
        #     f.close()
        # else:
        #     pass

