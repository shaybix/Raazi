import os
import sys
import sqlite3
from pymongo import MongoClient




client = MongoClient('localhost', 32768)

db = client['books']
collection = db['books']



files = []

for (dirpath, dirnames, filenames) in os.walk('db'):
        files.extend(filenames)

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
                page = dict(page_id=row[0], page_body=row[1], volume=row[2], page_number=row[3])

                pages.append(page)


            content = {
                        '_id': author_result[0],
                        'book_title': author_result[1],
                        'info': author_result[2],
                        'book_info': author_result[3],
                        'author': author_result[4],
                        'author_bio': author_result[5],
                        'category': author_result[6],
                        'died': author_result[7],
                        'content': pages
                        }


            post_id = db.posts.insert_one(content).inserted_id
            print post_id

            conn.close()







# f = open('test.txt', 'a+')


# post = db.posts.find_one({'_id': str(132)})
#
# posts = db.posts.find({"_id": 61})
#
#
# for post in posts:
#     print post['_id']
