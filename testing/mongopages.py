import os
import sys
import sqlite3
from pymongo import MongoClient





client = MongoClient('localhost', 27017)

db = client['books1']
# db.drop_database
# exit()
collection = db['books1']




files = []

for (dirpath, dirnames, filenames) in os.walk('db'):
        files.extend(filenames)
        files = files[0:5]

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
                # page = dict(page_id=row[0], page_body=row[1], volume=row[2], page_number=row[3])
                #
                # pages.append(page)
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
                posted_page_id = db.posts.insert_one(content_page).inserted_id
                print posted_page_id



            conn.close()







# f = open('test.txt', 'a+')


# post = db.posts.find_one({'_id': str(132)})
#
# posts = db.posts.find({"_id": 61})
#
#
# for post in posts:
#     print post['_id']
