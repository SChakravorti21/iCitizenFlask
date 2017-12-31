
#LIST OF SUBJECTS


'''Agriculture, Food
Animal Rights, Wildlife
Arts, Humanities
Budget, Spending, Taxes
Business, Consumers
Campaign Finance and Election Issues
Civil Liberties and Civil Rights
Commerce
Crime
Drugs
Education
Energy
Environmental
Executive Branch
Family and Children Issues
Federal, State, and Local Relations
Gambling and Gaming
Government Reform
Guns
Health
Housing and Property
Immigration
Indigenous Peoples
Insurance
Judiciary
Labor and Employment
Legal Issues
Legislative Affairs
Military
Municipal and County Issues
Nominations
Other
Public Services
Recreation
Reproductive Issues
Resolutions
Science and Medical Research
Senior Issues
Gender
Social Issues
State Agencies
Technology and Communication
Trade
Transportation
Welfare and Poverty'''


from textblob import Word
from textblob import TextBlob
from textblob.wordnet import Synset
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from scrapeEvents import scrape
import time


def get_sorted_events(state = 'ny', city = 'new york', pref_subjs = ['Education', 'Science'], num_pages = 3)
	start_time = time.time()


	'''plan:

	for each event in event_list
		for each noun in phrase:
			for each subj in pref_subjs:
				for each word in subj:

					find synsets of subj_word and each noun
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

	# i = 0
	# for e in event_list:
	# 	print(e.title, e.pts)

	# 	i += 1
	# 	if i > 10:
	# 		break




'''

t1 = 'tree'
t2 = 'plant'

ps = PorterStemmer()
# t1 = ps.stem(t1)
# t2 = ps.stem(t2)

print(t1, " ", t2)

w1 = Word(t1)
w2 = Word(t2)

print(w1.synsets)
print(w1.definitions)
print(w2.synsets)
print(w2.definitions)

print(w1.synsets[0].path_similarity(w2.synsets[1]))

quit()

word = Word('social')
print('test' ,word.synsets)
politics = word.synsets[0]


quit()



# print(politics.hypernyms())

# political = Word('political')
# print(political.synsets)



# n = politics.path_similarity(political)
# print(n)



# from textblob import Word
# word = Word('octopus')
# for x in range(2):
# 	print(word.synsets[x])
# 	print(word.definitions[x])
# 	print('')


# plant = word.synsets[1]
# # #lemma names are synonyms
# # print(plant.lemma_names())
# # print(plant.hypernyms())
# # print(plant.hyponyms()[:10])

# from textblob.wordnet import Synset
# octopus = Synset("octopus.n.01")
# fish = Synset('fish.n.01')

# word = Word('fish')
# print(word.synsets)
# print(word.definitions)


# from scrapeEvents import scrape

# eventslist = scrape(max_pg_num = 20)

# doc_complete = []


# for e in eventslist:
# 	doc_complete.append(e.title)
# # # compile documents
# # doc_complete = [doc1, doc2, doc3, doc4, doc5]




# from nltk.corpus import stopwords 
# from nltk.stem.wordnet import WordNetLemmatizer
# import string
# stop = set(stopwords.words('english'))
# exclude = set(string.punctuation) 
# lemma = WordNetLemmatizer()
# def clean(doc):
#     stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
#     punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
#     normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
#     return normalized

# doc_clean = [clean(doc).split() for doc in doc_complete] 

# # Importing Gensim
# import gensim
# from gensim import corpora

# # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
# dictionary = corpora.Dictionary(doc_clean)

# # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
# doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]


# # Creating the object for LDA model using gensim library
# Lda = gensim.models.ldamodel.LdaModel

# # Running and Trainign LDA model on the document term matrix.
# ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)

# # print(ldamodel.print_topics(num_topics=3, num_words=3))




# print(ldamodel.print_topics(num_topics = 10, num_words = 5))

'''