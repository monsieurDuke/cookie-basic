import re
#pnjacid.10-08-2020.shodan.log			
target = 'pnj.ac.id'
str_target = ""
arr_target = re.split('; |, |\.', target)
for i in arr_target:
	str_target += i
print (str_target)
#logs = open(str(os.getcwd())+'/log/shodan/'+fldate+'.shodan.log', "w+")			
