from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging, json

from iCitizenFlaskApp.dbconfig import db, QueryKeys
from iCitizenFlaskApp.views.user_routes import is_logged_in

from bson import json_util

mod = Blueprint('saved_data', __name__)

@mod.route('/saved-events/', methods=['GET'])
@is_logged_in
def saved_events():
	"""Renders the saved events page. This page later makes ajax requests
	for saved events to /fetch-saved-events/.
	"""

	return render_template('saved_events.html')

@mod.route('/fetch-saved-events/', methods=['GET'])
@is_logged_in
def fetch_saved_events():
	"""This method is called from get_saved_events.js and returns the list of 
	saved events that is in the database for the current user

	Returns:
		json: A JSON document with all saved events and their respective data.
			This data is used by the saved-events endpoint to display saved polls.
	"""

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	# Get the user and their saved events
	user = users.find_one(query)
	saved_events = user[QueryKeys.SAVED_EVENTS] if QueryKeys.SAVED_EVENTS in user else {}

	return json.dumps(saved_events, sort_keys=True, indent=4)

@mod.route('/saved-polls/', methods=['GET'])
@is_logged_in
def saved_polls():
	"""Renders the saved polls page. This page later makes ajax requests
	for saved events to /fetch-saved-polls/.
	"""

	return render_template('saved_polls.html')

@mod.route('/fetch-saved-polls/', methods=['GET'])
@is_logged_in
def fetch_saved_polls():
	"""This function is called from get_saved_polls.js and returns the list of 
	saved polls that is in the database for the current user

	Returns:
		json: A JSON document with all saved polls and their respective data.
			This data is used by the saved-polls endpoint to display saved polls.
	"""

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	# Get the user and their saved polls
	user = users.find_one(query)
	saved_polls = user[QueryKeys.SAVED_POLLS] if QueryKeys.SAVED_POLLS in user else {}

	# dump to a JSON document
	return json.dumps(saved_polls, sort_keys=True, indent=4)

@mod.route('/saved-legislators/', methods=['GET'])
@is_logged_in
def saved_legislators():
	"""Renders the saved legislators page. This page later makes ajax requests
	for saved events to /fetch-saved-legislators/.
	"""

	return render_template('saved_legislators.html')

@mod.route('/fetch-saved-legislators/', methods=['GET'])
@is_logged_in
def fetch_saved_legislators():
	"""This function is called from get_saved_legislators.js and returns the list of 
	saved legislators that is in the database for the current user

	Returns:
		json: A JSON document with all saved legislators and their respective data.
			This data is used by the saved-legislators endpoint to display saved 
			legislators.
	"""

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	# Get the user and their saved legislators, then dump to JSON
	user = users.find_one(query)
	saved_legislators = user[QueryKeys.SAVED_LEGISLATORS] if QueryKeys.SAVED_LEGISLATORS in user else {}

	return json.dumps(saved_legislators, sort_keys=True, indent=4)

@mod.route('/saved-bills/', methods=['GET'])
@is_logged_in
def saved_bills():
	"""Renders the saved bills page. This page later makes ajax requests
	for saved bills to /get-saved-state-bills/ and /get-saved-national-bills/.
	"""

	return render_template('saved_bills.html')

@mod.route('/get-saved-national-bills/', methods=['POST'])
@is_logged_in
def get_saved_national_bills():
	"""This function is called from get_saved_bills.js and returns the list of 
	saved national bills that is in the database for the current user

	Returns:
		json: A JSON document with all saved national bills and their respective data.
			This data is used by the saved-bills endpoint to display saved 
			national bills.
	"""

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	# Get the user, respective national bills that are saved, and dump to JSON
	user = users.find_one(query)
	saved_bills_jsons = user[QueryKeys.SAVED_NATIONAL_BILLS] if QueryKeys.SAVED_NATIONAL_BILLS in user else {}

	return json.dumps(saved_bills_jsons, sort_keys=True, indent=4, default=json_util.default)

@mod.route('/get-saved-state-bills/', methods=['POST'])
@is_logged_in
def get_saved_state_bills():
	"""This function is called from get_saved_bills.js and returns the list of 
	saved state bills that is in the database for the current user

	Returns:
		json: A JSON document with all saved state bills and their respective data.
			This data is used by the saved-bills endpoint to display saved 
			state bills.
	"""

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	# Get the user, respective state bills that are saved, and dump to JSON
	user = users.find_one(query)
	saved_bills_jsons = user[QueryKeys.SAVED_STATE_BILLS] if QueryKeys.SAVED_STATE_BILLS in user else {}

	return json.dumps(saved_bills_jsons, sort_keys=True, indent=4, default=json_util.default)
