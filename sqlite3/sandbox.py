import subprocess
import sys
import sqlite3


def db(DATABASE):
    sql_db = DATABASE.split('.')[0]
    sql_db = sql_db + ".db"

    connection = sqlite3.connect(sql_db)

    return connection


def something():
    DATABASE = 'sample.bok'

    con = db(DATABASE)
    c = con.cursor()

    # Dump the schema for the DB
    reply = subprocess.Popen(["mdb-schema", DATABASE, "mysql"],
                             stdout=subprocess.PIPE).communicate()[0]
    c.executescript(reply)
    con.commit()

    table_names = subprocess.Popen(["mdb-tables", "-1", DATABASE],
                                   stdout=subprocess.PIPE).communicate()[0]
    tables = table_names.splitlines()

    c.execute("BEGIN;")
    sys.stdout.flush()

    for table in tables:
        if table != '':
            reply = subprocess.Popen(["mdb-export", "-I", "mysql", DATABASE, table],
                                     stdout=subprocess.PIPE).communicate()[0]
            c.executescript(reply)

    con.commit()
    sys.stdout.flush()


def main(something):
    f = open('sql.txt', 'w+')
    f.write(something)
    f.close()


something()