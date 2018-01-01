
import urllib.request as u
from bs4 import BeautifulSoup

from textblob import Word
from textblob import TextBlob
from textblob.wordnet import Synset
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import time

class Event:

	def __init__(self, org_title, title, link, time, location, price, img_link, pts = 0, _id=None):
		self.org_title = org_title
		self.title = title
		self.link = link
		self.time = time
		self.location = location
		self.price = price
		self.img_link = img_link
		self.pts = pts

	def json(self):
		return {
			"org_title": self.org_title,
			"title": self.title,
			"link": self.link,
			"time": self.time,
			"location": self.location,
			"price": self.price,
			"img_link": self.img_link,
			"pts": self.pts
		}

	#param = state, city, max page num, list of subject prefs
	#returns list of all events
	@classmethod
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
						title_boxes[n].text.strip().lower(),
						link_boxes[n]['href'],
						time_boxes[n].text.strip(),
						loc_boxes[n].text.strip(),
						price_boxes[n].text,
						image_boxes[n].img['src']
					)
				)

		print('got events')
		return event_list


	#retusn sorted list of events
	@classmethod
	def get_sorted_events(cls, state = 'ny', city='new york', pref_subjs = ['politics'], num_pages = 5):


		start_time = time.time()

		event_list = Event.scrape(state = state, city = city, max_pg_num = num_pages)
		print('took ', time.time() - start_time, 'secs to get ', num_pages, ' pages of events')


		for i in range(len(pref_subjs)):
			pref_subjs[i] = pref_subjs[i].lower()
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

					if noun == 'and':
						continue

					for subj in pref_subjs:
						#subj_word is each indiv subj word in pref subjs
						subj_words = []

						nouns_phrases = []
						curr_sub = ''

						for c in subj:
							if c == (',' or '\'' or ':' or '-' or '?' or '!' or '&' or '+' or '#' or '@'):
								continue
							elif c == ' ' and curr_sub != '':
								subj_words.append(curr_sub)
								curr_sub = ''
							else:
								curr_sub += c

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

		import numpy as np

		event_pts=[]
		for e in event_list:
			event_pts.append(e.pts)

		#softmax
		event_pts = np.exp(event_pts) / float(sum(np.exp(event_pts)))

		for p, e in zip(event_pts, event_list):
			e.pts = p

		import operator
		#sort by descending
		event_list.sort(key = operator.attrgetter('pts'), reverse=True)


		print('time taken to sort by relevancy', time.time() - start_time)
		return event_list


	@staticmethod
	def get_top_n_events(state, city, pref_subjs, num_pages, num_events):

		sorted_events = Event.get_sorted_events(state = state, city = city, pref_subjs = pref_subjs, num_pages = num_pages)

		top_n = []

		if num_events <= len(sorted_events):
			for i in range(num_events):
				top_n.append(sorted_events[i])

		else:
			top_n = sorted_events

			for i in range(0, len(sorted_events) - num_events):
				top_n.pop(-1)

		return top_n



# pref_subjs = ['college', 'education', 'art']
# event_l = Event.get_top_n_events(state = 'ny', city = 'new york', pref_subjs = pref_subjs, num_pages = 1, num_events = 10)
# for e in event_l:
# 	print(e.title)
# 	print('						', e.pts)


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
