from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging, json

from iCitizenFlaskApp.dbconfig import db, QueryKeys
from iCitizenFlaskApp.views.user_routes import is_logged_in

mod = Blueprint('saved_data', __name__)

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
	saved_legislators = user[QueryKeys.SAVED_LEGISLATORS] if QueryKeys.SAVED_LEGISLATORS in user else {}

	return json.dumps(saved_legislators, sort_keys=True, indent=4)