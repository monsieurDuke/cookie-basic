from bs4 import BeautifulSoup
import requests

with open('simple.html') as scrap_html:
	soup = BeautifulSoup(scrap_html, 'lxml')

title  = soup.title.text
footer = soup.find('div', class_='footer').prettify()

print(soup.prettify())
print(title)
print(footer)
