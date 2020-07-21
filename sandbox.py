from faker import Faker
from faker.providers import phone_number

fake_gen = Faker()
fake_gen.add_provider(phone_number)

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
print()

for i in range(10):
	date_gen = '{:<13}'.format(fake_gen.date(pattern='%Y-%m-%d', end_datetime=None))
	print('|- %s' % (date_gen), end =' ')
	for i in range(1):
		date_gen = '{:<13}'.format(fake_gen.date(pattern='%Y-%m-%d', end_datetime=None))
		print('|- %s' % (date_gen), end =' ')
		for i in range(1):
			date_gen = '{:<14}'.format(fake_gen.date(pattern='%Y-%m-%d', end_datetime=None))
			print('|- %s' % (date_gen))
print()

for i in range(10):
	phone_gen = '{:<25}'.format(fake_gen.phone_number())[:14]
	print('|- %s' % (phone_gen), end =' ')
	for i in range(1):
		phone_gen = '{:<25}'.format(fake_gen.phone_number())[:14]
		print('|- %s' % (phone_gen), end =' ')
		for i in range(1):
			phone_gen = '{:<13}'.format(fake_gen.phone_number())[:14]
			print('|- %s' % (phone_gen))
print()

for i in range(5):
	add_gen = '{:<20}'.format(fake_gen.address())
	if i > 0:
		print()
	print('Address:\n'+add_gen)
print()

for i in range(10):
	job_gen = '{:<30}'.format(fake_gen.job())
	print('|- %s' % (job_gen))
print()

#print(fake_gen.job())
#print(fake_gen.address())

