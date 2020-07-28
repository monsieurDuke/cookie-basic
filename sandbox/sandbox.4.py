from zipfile import ZipFile
import os
import re

file = ['00-icat','01-chad','02-awdawd','03-awdawd']
for i in range(len(file)):
	path = str(os.getcwd()) + '/wordlist-master/' + file[i]
	print(path)

range = 0
for file in os.listdir("/home/cookie/Sandbox/Cookie-Basic/wordlist-master"):
	if file.endswith(".lst"):
		range += 1

get_list = [None]*range
inc = 0
for file in os.listdir("/home/cookie/Sandbox/Cookie-Basic/wordlist-master"):
	if file.endswith(".lst"):
		get_list[inc] = file
		inc += 1

print(get_list)
