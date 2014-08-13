import subprocess
import os

addr = 'http://elastic.dev:9200'

files = []

for (dirpath, dirnames, filenames) in os.walk('json'):
        files.extend(filenames)

for file in files:
    print file
    subprocess.call(['curl', '-s', '-XPOST', addr + '/_bulk', '--data-binary', '@' + 'json/' + file + ';'])


