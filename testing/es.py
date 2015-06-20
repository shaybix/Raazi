import os
import sys
import sqlite3
from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search, Q

client = Elasticsearch()


files = []
count = 1

for (dirpath, dirnames, filenames) in os.walk('db'):
        files.extend(filenames)
        # files = files[0:5]

        for file in files:

            file = 'db/' + file

            conn = sqlite3.connect(file)
            author_cursor = conn.cursor()
            body_cursor = conn.cursor()

            # print file
            author_cursor.execute('SELECT BkId, Bk, Betaka, Inf, Auth, AuthInf, cat, AD FROM main')

            author_result = author_cursor.fetchall()[0]

            book_id = str(author_result[0])

            body_cursor.execute('SELECT id, nass, part, page FROM b' + str(book_id) + '')

            body_result = body_cursor.fetchall()

            pages = []


            for row in body_result:
                row = list(row)
                # page = dict(page_id=row[0], page_body=row[1], volume=row[2], page_number=row[3])
                #
                # pages.append(page)

                if not isinstance(row[2], (int)):
                    row[2] = [None]

                content = {
                            '_id': author_result[0],
                            'book_title': author_result[1],
                            'info': author_result[2],
                            'book_info': author_result[3],
                            'author': author_result[4],
                            'author_bio': author_result[5],
                            'category': author_result[6],
                            'died': author_result[7],
                            }

                content_page = {
                                '_id': str(author_result[0]) + '-' + str(row[0]),
                                'book_id': author_result[0],
                                'page_body': row[1],
                                'volume': row[2],
                                'page_number': row[3],
                                'book': content
                                }

                response = client.create(
                                index='shamela',
                                id=str(author_result[0]) + '-' + str(row[0]),
                                body=content_page,
                                doc_type='pages'
                                )

                # print response

            print "[" + str(count) + "] completed inserting '" + author_result[1] + "' into index"
            count = count + 1

            conn.close()
