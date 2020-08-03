from termcolor import colored

a = colored('Hello World', 'grey', attrs=['bold'])
print(a)
print(colored('World Hello', 'magenta', attrs=['bold']))
a = input(colored('>> ', 'red', attrs=['bold']))

def clr(letter):
	letter = colored(letter, 'green', attrs=['bold'])
	return letter

print(clr(a)+"awawa")
