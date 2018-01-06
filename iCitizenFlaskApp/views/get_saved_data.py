from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging, json

from iCitizenFlaskApp.dbconfig import db, QueryKeys
from iCitizenFlaskApp.views.user_routes import is_logged_in

from bson import json_util

mod = Blueprint('saved_data', __name__)

@mod.route('/saved-events/', methods=['GET'])
@is_logged_in
def saved_events():
	return render_template('saved_events.html')

@mod.route('/fetch-saved-events/', methods=['GET'])
@is_logged_in
def fetch_saved_events():
	print('==================================================================')
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	saved_events = user[QueryKeys.SAVED_EVENTS] if QueryKeys.SAVED_EVENTS in user else {}

	return json.dumps(saved_events, sort_keys=True, indent=4)

@mod.route('/saved-polls/', methods=['GET'])
@is_logged_in
def saved_polls():
	return render_template('saved_polls.html')

@mod.route('/fetch-saved-polls/', methods=['GET'])
@is_logged_in
def fetch_saved_polls():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)

	if(user[QueryKeys.UPDATE_POLLS]):
		return None

	saved_polls = user[QueryKeys.SAVED_POLLS] if QueryKeys.SAVED_POLLS in user else {}

	return json.dumps(saved_polls, sort_keys=True, indent=4)

@mod.route('/saved-legislators/', methods=['GET'])
@is_logged_in
def saved_legislators():
	return render_template('saved_legislators.html')

@mod.route('/fetch-saved-legislators/', methods=['GET'])
@is_logged_in
def fetch_saved_legislators():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	if user[UPDATE_]
	saved_legislators = user[QueryKeys.SAVED_LEGISLATORS] if QueryKeys.SAVED_LEGISLATORS in user else {}

	return json.dumps(saved_legislators, sort_keys=True, indent=4)

@mod.route('/saved-bills/', methods=['GET'])
@is_logged_in
def saved_bills():
	return render_template('saved_bills.html')

@mod.route('/get-saved-national-bills/', methods=['POST'])
@is_logged_in
def get_saved_national_bills():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    saved_bills_jsons = user[QueryKeys.SAVED_NATIONAL_BILLS] if QueryKeys.SAVED_NATIONAL_BILLS in user else {}

    return json.dumps(saved_bills_jsons, sort_keys=True, indent=4, default=json_util.default)

@mod.route('/get-saved-state-bills/', methods=['POST'])
@is_logged_in
def get_saved_state_bills():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    saved_bills_jsons = user[QueryKeys.SAVED_STATE_BILLS] if QueryKeys.SAVED_STATE_BILLS in user else {}

    return json.dumps(saved_bills_jsons, sort_keys=True, indent=4, default=json_util.default)
