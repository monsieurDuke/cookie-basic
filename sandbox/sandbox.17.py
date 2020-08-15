import re

text = "alo ini irsyad ini aku yeeeeeeeeet\neh kamu mau kemana\now ok m8"
arr  = re.split('; |, |\\n', text)

print (text)
for i in arr:
	print (i)
