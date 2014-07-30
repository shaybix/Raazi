import sqlite3
import json
import sys
import subprocess

from optparse import OptionParser
# import elasticsearch


def fetch_main(sql_db):
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

    conn = sqlite3.connect(sql_db)
    c = conn.cursor()

    c.execute('SELECT BkId, Bk, Betaka, Inf, Auth, AuthInf, cat, AD FROM main')

    result = c.fetchall()[0]

    book_id = str(result[0])

    content = dict(book_id=str(result[0]), book_title=result[1], info=result[2], book_info=result[3], author=result[4],
                   author_bio=result[5], category=result[6], died=str(result[7]),
                   body=fetch_body(book_id, c), chapters=fetch_chapters(book_id, c))

    return json.dumps(content)


def fetch_body(book_id, c):
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

    c.execute('SELECT id, nass, part, page FROM b' + str(book_id) + '')
    result = c.fetchall()
    body = []

    for row in result:
        page = dict(page_id=str(row[0]), page_body=row[1], volume=row[2], page_number=str(row[3]))

        body.append(page)
    return body


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
        chapter = dict(heading=row[0], heading_level=str(row[1]), sub_level=str(row[2]), page_id=str(row[3]))

        chapters.append(chapter)

    return chapters


def validator():
    """
    validate the arguments giving through the commandline

    :rtype : list
    """

    usage = "usage: python %prog -i <input file> -o <output file>"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", dest="input_file", help="give BOK file to read from")
    parser.add_option("-o", dest="output_file", help="the desired json output filename")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

    options, args = parser.parse_args()

    # TODO test the validation for options parsed

    # if len(args) < 4:
    #     parser.error("incorrect number of arguments")


    bok_file = options.input_file
    bok_file_split = bok_file.split('.')
    json_file = options.output_file
    json_file_split = json_file.split('.')

    if not bok_file_split[-1] == "bok":
        pass
    elif not json_file_split[-1] == 'json':
        print "Must provide json filetype for output"
        pass
    else:
        return [bok_file, json_file]


def db(bok_file):
    """


    :rtype : object
    :param bok_file:
    :return:
    """
    sql_db = bok_file.split('.')[0]
    sql_db += ".db"

    connection = sqlite3.connect(sql_db)

    return [connection, sql_db]


def export(bok_file):
    """

    :param bok_file:
    """
    database = bok_file[0]
    DB = db(database)
    con = DB[0]
    sql_file = DB[1]
    c = con.cursor()

    # print 'setting charset....'
    # subprocess.Popen(['MDB_JET3_CHARSET="cp1256"'])

    # Dump the schema for the DB
    print 'dumping msql schema....'
    reply = subprocess.Popen(["mdb-schema", database, "mysql"],
                             stdout=subprocess.PIPE).communicate()[0]
    c.executescript(reply)
    con.commit()

    print 'dumping tables....'
    table_names = subprocess.Popen(["mdb-tables", "-1", database],
                                   stdout=subprocess.PIPE).communicate()[0]
    tables = table_names.splitlines()

    print 'begin executing mysql....'
    c.execute("BEGIN;")
    sys.stdout.flush()

    for table in tables:
        if table != '':
            print 'dumping ' + table + '....'
            reply = subprocess.Popen(["mdb-export", "-I", "mysql", database, table],
                                     stdout=subprocess.PIPE).communicate()[0]
            c.executescript(reply)

    print 'committing it all to the database....'
    con.commit()
    sys.stdout.flush()
    con.close()
    return sql_file


def index():
    """
    :rtype : object
    """

    # TODO automate process for indexing the document into Elasticsearch
    pass


if __name__ == "__main__":
    if validator():
        sql_db = export(validator())
        files = validator()
        json_data = fetch_main(sql_db)
        f = open(files[1], 'w+')
        f.write(json_data)
        f.close()

