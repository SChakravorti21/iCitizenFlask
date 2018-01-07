from pymongo import MongoClient
from os import environ

client = MongoClient("mongodb://127.0.0.1:27017")
db = client['icitizen']


class QueryKeys:
	NAME = 'name'
	EMAIL = 'email'
	USERNAME = 'username'
	PASSWORD = 'password'
	INPUTTED_PREFERENCES = 'inputted_prefs'


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
	IS_UPDATING = 'is_updating'

	UPDATE_EVENTS = 'update_events'
	UPDATE_BILLS = 'update_bills'

	USER_EVENTS = 'user_events'
	SAVED_EVENTS = 'saved_events'

	UPDATE_POLLS = 'update_polls'

	USER_POLLS = 'user_polls'
	SAVED_POLLS = 'saved_polls'
	EVENT_ID = 'event_id'
	POLL_ID = 'poll_id'

	NATIONAL_LEGISLATORS = 'national_legislators'
	STATE_LEGISLATORS = 'state_legislators'
	SAVED_LEGISLATORS = 'saved_legislators'

	NATIONAL_BILLS = 'national_bills'
	SAVED_NATIONAL_BILLS = 'saved_national_bills'

	STATE_BILLS = 'state_bills'
	SAVED_STATE_BILLS = 'saved_state_bills'
