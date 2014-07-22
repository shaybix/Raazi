import sqlite3


connection = sqlite3.connect('sample.sqlite3')


cursor = connection.cursor()

output = cursor.execute('Select * from main')

f = open('sample2.txt', 'w')

fetch = cursor.fetchone()

#lines = []
#
#for line in f:
#    lines.append(line)
#
#
#print lines[]

#print fetch[0]
#print "----------------"
#print fetch[1]
#print "----------------"
#info = fetch[2]
#
#encoded = info.encode('utf-8')
#
#f.write(encoded)

#print "----------------"
#encoded = fetch[3].encode('utf-8')
#encoded = encoded.splitlines()[5].split(':')[-1].split('.')[0]
info = fetch[-5:]
#
print info[1]
#encoded = info.encode('utf-8')
#print encoded
#f.write(encoded)
#print "----------------"
#print fetch[4]


f.close()