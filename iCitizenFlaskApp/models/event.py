class Event:

	def __init__(self, title, link, time, location, price):
		self.title = title
		self.link = link
		self.time = time
		self.location = location
		self.price = price

	def printInfo(self):
		print('title : ', self.title)
		print('link for more info : ', self.link)
		print('date of event : ', self.time)
		print('location of event: ', self.location)
		print('price : ', self.price)



import urllib.request as u
from bs4 import BeautifulSoup

from textblob import Word
from textblob import TextBlob
from textblob.wordnet import Synset
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from scrapeEvents import scrape
import time



@classmethod
#param = state, city, max page num, list of subject prefs
#returns list of all events
def scrape(cls, state = 'ny', city = 'new york', max_pg_num = 1):


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
				cls(
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


@classmethod
def get_sorted_events(cls, state = 'ny', city = 'new york', pref_subjs = ['Education', 'Science'], num_pages = 3)
	start_time = time.time()


	'''plan:

	for each event in event_list
		for each word in title:
			for each subj in pref_subjs:
				for each word in subj:

					find synonymsets of subj_word and each noun
					find max of path similarity between subj and noun
					sum that to total points per event
		
		average the num points per event
	'''
	event_list = scrape(state = state, city = city, max_pg_num = num_pages)
	print('took ', time.time() - start_time, 'secs to get ', n, ' pages of events')


	#goes through every combination of words in the event title and the pref subjects words
	#finds the list of synonyms for each combination
	#finds the max path similarity value in this list of synonyms
	#adds this max num to the pts field in events object
	#repeat for every combination of event and subject words
	#find the average of the pts in the object
	#repeat for each event
	#sort events by descending order according to pts
	for event in event_list:

		ctr = 0
		pts_to_assign = 0
		old_title = event.title
		nouns_phrases = []
		curr = ''

		for c in old_title:
			if c == (',' or '\'' or ':' or '-' or '?' or '!' or '&' or '+' or '#' or '@'):
				continue
			elif c == ' ' and curr != '':
				nouns_phrases.append(curr)
				curr = ''
			else:
				curr += c

		# nouns_phrases = TextBlob(old_title).noun_phrases
		# nouns_phrases = old_title.split(' ')
		for noun_phrase in nouns_phrases:
			nouns = noun_phrase.split(' ')
			#noun is each indiv noun in the title
			for noun in nouns:
				for subj in pref_subjs:
					#subj_word is each indiv subj word in pref subjs
					subj_words = subj.split(' ')
					for subj_word in subj_words:

						currMax = 0
						noun_syns = Word(noun).synsets
						subj_syns = Word(subj_word).synsets

						if len(noun_syns) == 0 or len(subj_syns) == 0:
							break;

						for i in range(len(noun_syns)):
							for j in range(len(subj_syns)):
								pathsim = noun_syns[i].path_similarity(subj_syns[j])
								if pathsim != None:
									if pathsim > currMax:
										currMax = pathsim

						if(currMax != 0):
							ctr += 1
							event.pts += currMax

		if(ctr != 0):			
			event.pts /= ctr


	import operator
	#sort by descending
	event_list.sort(key = operator.attrgetter('pts'), reverse=True)


	print('time taken to sort by relevancy', time.time() - start_time)
	return event_list

