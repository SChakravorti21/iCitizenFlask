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

	EVENT_LIST = 'user_events'
	UPDATE_POLLS = 'update_polls'

	USER_POLLS = 'user_polls'
	SAVED_POLLS = 'saved_polls'
	POLL_ID = 'poll_id'

	NATIONAL_BILLS = 'national_bills'
	SAVED_NATIONAL_BILLS = 'saved_national_bills'

	STATE_BILLS = 'state_bills'
	SAVED_STATE_BILLS = 'saved_state_bills'
