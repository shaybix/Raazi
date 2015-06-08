import os
import rarfile
import subprocess

directory = 'downloads/'
dest = 'bok/'
files = []


def unrar(file):
    rf = rarfile.RarFile(file)
    file = file.replace('rar', 'bok')
    file = file.replace(directory, dest)
    if not os.path.isfile(file):
        for names in rf.infolist():
            name = names.filename
        rf.extract(name)

        subprocess.call(['mv', name, file])


for (dirpath, dirnames, filenames) in os.walk(directory):
    files.extend(filenames)
    files.remove('.DS_Store')
    count = 0

    while count < 15:
        for file in files:
            unrar(directory + file)
            print 'Completed ' + file
            count += 1

    pass
