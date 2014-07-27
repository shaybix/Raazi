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


def export(bok_file):
    """



    :type bok_file: str
    :param bok_file:
    :rtype : str
    """


    # TODO accept bok_file as param and begin and convert to sqlite3

    # # Dump the schema for the DB
    # subprocess.call(["mdb-schema", DATABASE, "mysql"])
    #
    # # Get the list of table names with "mdb-tables"
    # table_names = subprocess.Popen(["mdb-tables", "-1", DATABASE],
    #                                stdout=subprocess.PIPE).communicate()[0]
    # tables = table_names.splitlines()
    #
    # print "BEGIN;" # start a transaction, speeds things up when importing
    # sys.stdout.flush()
    #
    # # Dump each table as a CSV file using "mdb-export",
    # # converting " " in table names to "_" for the CSV filenames.
    # for table in tables:
    #     if table != '':
    #         subprocess.call(["mdb-export", "-I", "mysql", DATABASE, table])
    #
    # print "COMMIT;" # end the transaction
    # sys.stdout.flush()

    return 'sample.sqlite3'


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
    :rtype : object
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

    :rtype : str
    """

    usage = "usage: python %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", dest="input_file", help="give BOK file to read from")
    parser.add_option("-o", dest="output_file", help="the desired json output filename")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

    options, args = parser.parse_args()

    # TODO test the validation for options parsed

    print len(args)
    # if len(args) < 4:
    #     parser.error("incorrect number of arguments")

    # TODO validate the filetypes given for input and output before continuing

    bok_file = options.input_file
    bok_file_split = bok_file.split('.')
    json_file = options.output_file
    json_file_split = json_file.split('.')

    if not bok_file_split[-1] == "bok":
        pass
    elif not json_file_split[-1] == 'json':
        print "Must provide json filetype for output"
        return 0
    else:
        # TODO is there need to validate the .bok file itself?
        return bok_file


if __name__ == "__main__":

    sql_db = export(validator())

    json_data = fetch_main(sql_db)

    f = open('jsondata.json', 'w+')

    f.write(json_data)

    f.close()