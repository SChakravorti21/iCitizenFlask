import urllib.request as u
from bs4 import BeautifulSoup
from textblob import Word
from textblob import TextBlob
from textblob.wordnet import Synset
import time

class Event:

	def __init__(self, org_title, title, link, time, location, price, img_link, pts = 0, saved = False):
		self.org_title = org_title
		self.title = title
		self.link = link
		self.time = time
		self.location = location
		self.price = price
		self.img_link = img_link
		self.pts = pts
		self.saved = saved

	def json(self):
		return {
			"org_title": self.org_title,
			"title": self.title,
			"link": self.link,
			"time": self.time,
			"location": self.location,
			"price": self.price,
			"img_link": self.img_link,
			"pts": self.pts,
			"saved": self.saved
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

			event_titles = set([])

			for n in range(numEvents):


				e_to_add = cls(
					org_title = title_boxes[n].text.strip(),
					title = title_boxes[n].text.strip().lower(),
					link = link_boxes[n]['href'],
					time = time_boxes[n].text.strip(),
					location = loc_boxes[n].text.strip(),
					price = price_boxes[n].text,
					img_link = image_boxes[n].img['src']
				)

				if e_to_add.title not in event_titles:
					event_titles.add(e_to_add.title)
					event_list.append(e_to_add)

		return event_list


	#retusn sorted list of events
	@classmethod
	def get_sorted_events(cls, state, city, pref_subjs, num_pages):

		start_time = time.time()
		event_list = Event.scrape(state = state, city = city, max_pg_num = num_pages)

		print('took ', time.time() - start_time, 'secs to get ', num_pages, ' pages of events')

		# event_list = [cls(title = 'prohibition pub crawl', org_title = 'PROHIBITION PUB CRAWL', link = 1, time=1,location=1,price=1,img_link=1)]


		for p in pref_subjs:
			print(p)

		for i in range(len(pref_subjs)):
			pref_subjs[i] = pref_subjs[i].replace(',', '').lower()
		#goes through every combination of words in the event title and the pref subjects words
		#finds the list of synonyms for each combination
		#finds the max path similarity value in this list of synonyms
		#adds this max num to the pts field in events object
		#repeat for every combination of event and subject words
		#find the average of the pts in the object
		#repeat for each event
		#sort events by descending order according to pts

		chars_to_skip = {',', '\'', '"', ':', '-', '?', '!', '&', '+', '#', '@', '/',
						'\\', '(', ')', '{', '}', '%', '^', '*', '_'}
		stop_words = {'a','in', 's', 'do', 'that', 'between', 'most', 'who', 'their',
		'now', 'be', 'which', 'ourselves', 'my', 'some', 'of', 'the', 'to', 'hasn',
		'about', 'was', 'before', 'its', 'but', 'with', 'have', 'on', 'own', 'ma',
		'them', 'doesn', 'mustn', 'a', 'same', 'yourself', 'y', 'is', 'for', 'where',
		'aren', 'had', 'didn', 'o', 'this', 'himself', 'in', 'further', 'only', 'against',
		't', 'each', 'as', 'i', 'just', 'if', 'out', 'were', 'from', 'has', 'again',
		 'through', 'we', 'how', 'me', 'so', 'does', 'off', 'yourselves', 'you', 'below',
		  'wasn', 'been', 'because', 'any', 'am', 'will', 're', 'ain', 'during', 'or',
		   'than', 'your', 'when', 'these', 'wouldn', 'll', 'haven', 'itself', 'more',
		    'she', 'while', 'yours', 'by', 'both', 'couldn', 'his', 'at', 'down', 've',
			 'mightn', 'and', 'after', 'then', 'theirs', 'it', 'such', 'our', 'those',
			  'don', 'what', 'he', 'themselves', 'd', 'whom', 'him', 'above', 'ours',
			   'once', 'can', 'weren', 'under', 'not', 'there', 'here', 'shan', 'why',
			    'being', 'they', 'm', 'won', 'into', 'over', 'up', 'needn', 'few', 'isn',
				 'are', 'shouldn', 'too', 'hadn', 'myself', 'did', 'her', 'having', 'very',
				  'herself', 'doing', 'hers', 'should', 'no', 'all', 'nor', 'an', 'other',
				   'until'}


		for event in event_list:

			ctr = 0
			pts_to_assign = 0

			old_title = event.title
			event_words = []
			curr = ''

			# for c in old_title:
			# 	if c in chars_to_skip or c.isdigit():
			# 		continue
			# 	elif c.strip() == '' and curr.strip() != '':

			# 		if curr not in stop_words:
			# 			event_words.append(curr.strip())
			# 		curr = ''
			# 	else:
			# 		curr += c

			for c in old_title:
				if (c in chars_to_skip or c.isdigit() or c.strip() == '') and curr.strip() != '':
					if curr not in stop_words:
						event_words.append(curr.strip())
						curr = ''
					else:
						curr = ''
				else:
					curr += c

			#get the last word in phrase
			if curr not in stop_words:
				event_words.append(curr.strip())
				curr = ''


			for word in event_words:

				for subj in pref_subjs:

					#subj_words is each indiv subj phrase in pref subjs
					subj_words = subj.split(' ')
					# print(subj_words)

					for subj_word in subj_words:

						if subj_word in stop_words:
							continue

						currMax = 0
						word_syns = Word(word).synsets
						subj_syns = Word(subj_word).synsets

						if len(word_syns) == 0 or len(subj_syns) == 0:
							break;

						for i in range(len(word_syns)):
							for j in range(len(subj_syns)):

								pathsim = word_syns[i].path_similarity(subj_syns[j])
								if pathsim != None:
									if pathsim > currMax:
										currMax = pathsim

						# print(word, 'vs', subj_word, 'score =', currMax)

						if(currMax != 0):
							ctr += 1
							event.pts += currMax

			if(ctr != 0):
				event.pts /= ctr

		# import numpy as np
        #
		# event_pts=[]
		# for e in event_list:
		# 	event_pts.append(e.pts)
        #
		# #softmax
		# event_pts = np.exp(event_pts) / float(sum(np.exp(event_pts)))
        #
		# for p, e in zip(event_pts, event_list):
		# 	e.pts = p

		import operator
		#sort by descending
		event_list.sort(key = operator.attrgetter('pts'), reverse=True)


		print('time taken to sort by relevancy', time.time() - start_time)
		return event_list


	@staticmethod
	def get_top_n_events(state = 'ny', city = 'new york', pref_subjs = ['education, finance, economy, financial, scholarship, school'], num_pages = 5, num_events = 15):

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


# event_l = Event.get_top_n_events(num_events = 10)
# for e in event_l:
# 	print(e.title, '\n       ', e.pts)


'''
for each event in event_list
	for each word in title:
		for each subj in pref_subjs:
			for each word in subj:

				find synonymsets of subj_word and each noun
				find max of path similarity between subj and noun
				sum that to total points per event

	average the num points per event
'''
