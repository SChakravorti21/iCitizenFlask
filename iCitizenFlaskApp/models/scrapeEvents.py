

class Event:

	def __init__(self, title, link, time, location, price, img_link, pts = 0):
		self.title = title
		self.link = link
		self.time = time
		self.location = location
		self.price = price
		self.img_link = img_link
		self.pts = pts

	def printInfo(self):
		print('NUM POINTS = ', self.pts)
		print('title : ', self.title)
		print('link for more info : ', self.link)
		print('date of event : ', self.time)
		print('location of event: ', self.location)
		print('price : ', self.price)
		print('img link : ', self.img_link)


import urllib.request as u
from bs4 import BeautifulSoup

#param = state, city, max page num, list of subject prefs
#returns list of all events
def scrape(state = 'ny', city = 'new york', max_pg_num = 1):


	city = city.replace(' ', '-')

	event_list = []

	for n in range(1, max_pg_num + 1):

		page_url = 'https://www.eventbrite.com/d/' + state.lower() + '--' + city.lower() + '/political-events/?crt=regular&sort=best'
		
		if n > 1:
			page_url += ('&page=' + str(n))

		page = u.urlopen(page_url)

		soup = BeautifulSoup(page, 'html.parser')


		#if page goes out of bounds, break

		out_of_bounds_box = soup.find('div', attrs = {'class': 'js-search-error-container'})
		if(out_of_bounds_box != None):
			break;

		title_boxes = soup.findAll('div', attrs = {'class': 'list-card__title'})
		loc_boxes = soup.findAll('div', attrs = {'class': 'list-card__venue'})
		link_boxes = soup.findAll('a', attrs = {'class': 'list-card__main'}, href = True)
		time_boxes = soup.findAll('time', attrs = {'class': 'list-card__date'})
		price_boxes = soup.findAll('span', attrs = {'class':'list-card__label'})
		image_boxes = soup.findAll('div', attrs = {'class': 'list-card__image'})


		numEvents = len(title_boxes)

		for n in range(numEvents):
			event_list.append(
				Event(
					title_boxes[n].text.strip(), 
					link_boxes[n]['href'], 
					time_boxes[n].text.strip(), 
					loc_boxes[n].text.strip(),
					price_boxes[n].text,
					image_boxes[n].img['src']
				)
			)

	print('got events')
	return event_list

