from pymongo import MongoClient
from os import environ

client = MongoClient(environ['ICITIZEN_MONGODB_URI'])
db = client['icitizen']


class QueryKeys:
	NAME = 'name'
	EMAIL = 'email'
	USERNAME = 'username'
	PASSWORD = 'password'
	INPUTTED_PREFERENCES = 'inputted_prefs'

	#stores arrayist of saved event titles
	SAVED_EVENTS = 'saved_events'

	PREFERENCES = 'preferences'
	LOCATION = 'location'

	ADDRESS = 'address'
	CITY = 'city'
	STATE = 'state'
	COUNTRY = 'country'
	ZIPCODE = 'zipcode'
	PARTY = 'party'
	TOPICS = 'subjects'
	LATLONG = 'latitude_longitude'
	LATITUDE = 'latitude'
	LONGITUDE = 'longitude'

	UPDATE_DB = 'update_db'

	UPDATE_EVENTS = 'update_events'
	UPDATE_BILLS = 'update_bills'
	UPDATE_POLLS = 'update_polls'
