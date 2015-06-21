import subprocess
import os
from elasticsearch import Elasticsearch

client = Elasticsearch()




files = []

for (dirpath, dirnames, filenames) in os.walk('downloads'):
        files.extend(filenames)

        print len(files)
        exit()






# for file in files:
#     print file
#     subprocess.call(['curl', '-s', '-XPOST', addr + '/_bulk', '--data-binary', '@' + 'json/' + file + ';'])
