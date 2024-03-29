import urllib.request as u
from bs4 import BeautifulSoup
from textblob import Word
from textblob import TextBlob
from textblob.wordnet import Synset
import time
import math




class Event:


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
			   'until', 'also'}


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


		'''
		The part below uses the first 10 chars of the title to calculate a hashcode
		which acts as a unique ID for the event. This is used later on when determining which
		event has been favorited
		'''
		h = 0
		for c in self.title[:10]:
			h = (31 * h + ord(c)) & 0xFFFFFFFF
		hc = ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

		self.event_id = hc
		print('event_id = ', self.event_id)



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
			"saved": self.saved,
			"event_id": self.event_id
		}

	#param = state, city, max page num, list of subject prefs
	#returns list of all events
	@classmethod
	def scrape(cls, state = 'ny', city = 'new york', max_pg_num = 1):
		'''
		Scrapes events from eventbrite with the given location parameters

		@param state : state of user, used to Scrape
		@param city : city of user, used to Scrape
		@param max_pg_num : basically, number of pages to scrape from
		@return list of Event objects
		'''

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


	'''
	1. goes through every combination of words in the event title and the pref subjects words
	2. finds the list of synonyms for each combination
	3. finds the max path similarity value in this list of synonyms
	4. adds this max num to the pts field in events object
	5. repeat for every combination of event and subject words
	6. find the average of the pts in the object
	7. repeat for each event
	8. sort events by descending order according to pts
	'''
	@classmethod
	def get_sorted_events(cls, state, city, pref_subjs, num_pages):

		'''
		Calls the scrape method defined above to get all the events from a certain number
		of pages. Then it finds the max path similarity between every combination of words in
		every title and in the pref_subjs. It averages all the path similarities for an event
		and assigns that value to the 'pts' field. At the end, the list is sorted by the 'pts'
		attribute, and list is returned.

		@param state : state of user, used to scrape Events
		@param city : city of user, used to scrape Events
		@param pref_subjs : list of preferred used subjects, used to sort by relevancy
		@param num_pages : number of pages to scrape from
		@return list of sorted events
		'''

		start_time = time.time()
		event_list = Event.scrape(state = state, city = city, max_pg_num = num_pages)

		print('took ', time.time() - start_time, 'secs to get ', num_pages, ' pages of events')

		# event_list = [cls(title = 'prohibition pub crawl', org_title = 'PROHIBITION PUB CRAWL', link = 1, time=1,location=1,price=1,img_link=1)]


		pref_subjs = [s.replace(',', '') for s in pref_subjs]

		for event in event_list:

			ctr = 0


			event_words = []
			curr = ''

			for c in event.title:

				if (c in Event.chars_to_skip or c.isdigit() or c.strip() == ''):
					if curr.strip() not in Event.stop_words and len(curr.strip()) > 1:
						event_words.append(curr.strip())
					curr = ''
				else:
					curr += c

			#get the last word in phrase
			if curr.strip() not in Event.stop_words and len(curr.strip()) > 1:
				event_words.append(curr.strip())
				curr = ''


			for word in event_words:

				for subj in pref_subjs:

					#subj is each indiv subj phrase in pref subjs
					subj_words = subj.split(' ')
					subj_words = [w for w in subj_words if w not in Event.stop_words]


					for subj_word in subj_words:

						currMax = 0
						word_syns = Word(word).synsets
						subj_syns = Word(subj_word).synsets

						if len(word_syns) == 0 or len(subj_syns) == 0:
							break;

						for word_syn in word_syns:
							for subj_syn in subj_syns:

								pathsim = word_syn.path_similarity(subj_syn)
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



	@staticmethod
	def get_top_n_events(state = 'ny', city = 'new york', pref_subjs = ['education, finance, economy, financial, scholarship, school'], num_pages = 5, num_events = 15):

		'''
		This method is called from user_data.py by a celery worker once the user
		has reached the dashboard. Once the loading is finished, the user can visit the
		events page and see his relevant events. This also puts the 'pts' field
		or relevancy score through the sigmoid function, to map the small relevancy value
		to a percent.

		@param state : state of user
		@param city : city of user
		@param pref_subj : list of preferred subjects, used to find most relevant events
		@param num_pages : how many pages to scrape events from Eventbrite from
		@param num_events : how many of the top events do you want?
		@return list of top n events that are sorted by relevancy
		'''

		sorted_events = Event.get_sorted_events(state = state, city = city, pref_subjs = pref_subjs, num_pages = num_pages)

		top_n = []

		if num_events <= len(sorted_events):
			for i in range(num_events):
				top_n.append(sorted_events[i])

		else:
			top_n = sorted_events

			for i in range(0, len(sorted_events) - num_events):
				top_n.pop(-1)


		e = 2.718281828459

		for event in top_n:
			score = 1/(1 + (e ** (-10 * event.pts))) * 100
			stepper = pow(10.0, 2)
			event.pts = math.trunc(stepper * score) / stepper

		return top_n


# events = Event.get_top_n_events()
# for e in events:
# 	print(e.json()['event_id'])

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
