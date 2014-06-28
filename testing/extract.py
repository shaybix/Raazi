import subprocess

file = ''


data = subprocess.Popen(["mdb-array", "sample.bok", "b767"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = data.communicate()
print type(out)
file = open('testing.txt', 'wb')

file.write(out)
file.close()

