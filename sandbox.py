from faker import Faker

fake_gen = Faker()

#product_detail = '{:<13}'.format((str(
for i in range(10):
	name_gen = '{:<21}'.format(fake_gen.name())
	print('|- %s' % (name_gen), end =' ')
	for i in range(1):
		name_gen = '{:<21}'.format(fake_gen.name())
		print('|- %s' % (name_gen), end =' ')
		for i in range(1):
			name_gen = '{:<23}'.format(fake_gen.name())
			print('|- %s' % (name_gen))
print()

for i in range(10):
	email_gen = '{:<34}'.format(fake_gen.email())
	print('|- %s' % (email_gen), end =' ')
	for i in range(1):
		email_gen = '{:<26}'.format(fake_gen.email())
		print('|- %s' % (email_gen))
print()

for i in range(10):
	domain_gen = '{:<21}'.format(fake_gen.domain_name())
	print('|- %s' % (domain_gen), end =' ')
	for i in range(1):
		domain_gen = '{:<21}'.format(fake_gen.domain_name())
		print('|- %s' % (domain_gen), end =' ')
		for i in range(1):
			domain_gen = '{:<21}'.format(fake_gen.domain_name())
			print('|- %s' % (domain_gen))
print(fake_gen.job())


