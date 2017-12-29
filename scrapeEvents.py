class Event:

	def __init__(self, title, link, time, price):
		self.title = title
		self.link = link
		self.time = time
		self.price = price

	def printInfo(self):
		print('title : ', self.title)
		print('link for more info : ', self.link)
		print('date of event : ', self.time)
		print('price : ', self.price)


import urllib.request as u
from bs4 import BeautifulSoup


state = input('Enter state code\n')
city = input('Enter city name\n')
city = city.replace(' ', '-')



page_url = 'https://www.eventbrite.com/d/' + state.lower() + '--' + city.lower() + '/political-events/?crt=regular&sort=best'
page = u.urlopen(page_url)

soup = BeautifulSoup(page, 'html.parser')

title_boxes = soup.findAll('div', attrs = {'class': 'list-card__title'})
link_boxes = soup.findAll('a', attrs = {'class': 'list-card__main'}, href = True)
time_boxes = soup.findAll('time', attrs = {'class': 'list-card__date'})
price_boxes = soup.findAll('span', attrs = {'class':'list-card__label'})

numEvents = len(title_boxes)
event_list = []

for n in range(numEvents):
	event_list.append(
		Event(
			title_boxes[n].text.strip(), 
			link_boxes[n]['href'], 
			time_boxes[n].text.strip(), 
			price_boxes[n].text)
		)


for e in event_list:
	e.printInfo()
	print('')