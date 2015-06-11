import os
import sys
import sqlite3
from pymongo import MongoClient




client = MongoClient('localhost', 32768)

db = client['test_database']
collection = db['authors']



files = []

for (dirpath, dirnames, filenames) in os.walk('db'):
        files.extend(filenames)

        for file in files:

            file = 'db/' + file

            conn = sqlite3.connect(file)
            c = conn.cursor()

            # print file
            c.execute('SELECT BkId, Bk, Betaka, Inf, Auth, AuthInf, cat, AD FROM main')

            result = c.fetchall()[0]

            book_id = str(result[0])

            content = {
                        '_id': result[0],
                        'book_title': result[1],
                        'info': result[2],
                        'book_info': result[3],
                        'author': result[4],
                        'author_bio': result[5],
                        'category': result[6],
                        'died': result[7]
                        }


            post_id = db.posts.insert_one(content).inserted_id
            print post_id

            conn.close()






# posts = collection.find()
# for post in db.posts.find():
#     # print dir(post)
#     print post.get('book_title')
#     print post.get('author')
#     print post.get('died')
#
# print db.posts.retrieved
# print db.posts.count
