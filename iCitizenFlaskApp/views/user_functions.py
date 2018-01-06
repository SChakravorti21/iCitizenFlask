from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging, json
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from pygeocoder import Geocoder

from iCitizenFlaskApp.forms import PreferencesForm
from iCitizenFlaskApp.dbconfig import db, QueryKeys
from iCitizenFlaskApp.data import SUBJECTS
from iCitizenFlaskApp.views.user_routes import is_logged_in
from iCitizenFlaskApp.views.user_data import call_celery_task

mod = Blueprint('functions', __name__)


@mod.route('/profile/', methods=['GET'])
@is_logged_in
def show_profile():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']
	user = users.find_one(query)

	return render_template('profile.html', user=user)


@mod.route('/update-prefs/', methods=['GET', 'POST'])
@is_logged_in
def update_preferences():
	form = PreferencesForm()
	topics = []
	error = None

	# Prefill the preferences if the user has set them before
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']
	user = users.find_one(query)

	# print(QueryKeys.INPUTTED_PREFERENCES)
	if user[QueryKeys.INPUTTED_PREFERENCES]:
		location = user[QueryKeys.LOCATION]

		form.address.data = location[QueryKeys.ADDRESS]
		form.city.data = location[QueryKeys.CITY]
		form.state.data = location[QueryKeys.STATE]
		form.country.data = location[QueryKeys.COUNTRY]
		form.zipcode.data = location[QueryKeys.ZIPCODE]

		prefs = user[QueryKeys.PREFERENCES]
		form.political_party.data = prefs[QueryKeys.PARTY]
		topics = prefs[QueryKeys.TOPICS]

	if request.method == 'POST':
		form = PreferencesForm(request.form)
		topics = request.form.getlist('subjects')
		if not topics or len(topics) == 0:
			error = 'Please choose at least one topic so that we can find bills that are relevant for you'

		if form.validate():
			party = form.political_party.data
			address = form.address.data
			city = form.city.data
			state = form.state.data
			country = form.country.data
			zipcode = form.zipcode.data

			try:
				location = Geocoder.geocode("{}, {}, {}, {}, {}".format(address, city, state, country, zipcode))
				print(location)
			except:
				flash('Sorry, we were unable to process your address at this time. Please try again 15 minutes later.', 'warning')
				return redirect(url_for('functions.update_preferences'))


			address_obj = {
				QueryKeys.ADDRESS: address,
				QueryKeys.CITY: city,
				QueryKeys.STATE: state,
				QueryKeys.COUNTRY: country,
				QueryKeys.ZIPCODE: zipcode,
				QueryKeys.LATLONG: {
					QueryKeys.LATITUDE: location.latitude,
					QueryKeys.LONGITUDE: location.longitude
				}
			}

			preferences_obj = {
				QueryKeys.PARTY: party,
				QueryKeys.TOPICS: topics
			}

			# print(address_obj)
			# print(preferences_obj)

			user = users.find_one_and_update(query, {'$set':
				{
					QueryKeys.INPUTTED_PREFERENCES: True,
					QueryKeys.PREFERENCES: preferences_obj,
					QueryKeys.LOCATION: address_obj,
					QueryKeys.UPDATE_DB: True,
					QueryKeys.UPDATE_EVENTS: True,
					QueryKeys.UPDATE_BILLS: True,
					QueryKeys.UPDATE_POLLS: True
				}})
			# print(user)

			# Uodate the database once preferences are updated
			#call_celery_task()
			flash('Your preferences have been updated!', 'success')
			return redirect( url_for('users.load_dashboard'))

	return render_template('update_preferences.html', form=form,
		subjects=[(str(subject).strip(), subject) for subject in SUBJECTS],
		selected_subjects=topics, error=error)


@mod.route('/save-event/', methods=['POST'])
@is_logged_in
def save_event():
	event_to_save = request.get_json()

	print('INSIDE SAVE EVENT === ', event_to_save)
	print(event_to_save.keys())

	event_id = event_to_save[QueryKeys.EVENT_ID]
	print(event_id)

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']
	user = users.find_one(query)

	#this is a dict, where key = event_id and value = event_json
	curr_saved_events = user[QueryKeys.SAVED_EVENTS] if QueryKeys.SAVED_EVENTS in user else {}

	#if already saved in there
	if len(curr_saved_events) > 0 and event_id in curr_saved_events:
		return 'False'

	event_query = QueryKeys.SAVED_EVENTS + '.' + str(event_id)

	# print('QUERY = ', query)
	# print('EVENT_QUERY = ', event_query)
	# print('EVENT TO SAVE = ', event_to_save)

	users.find_one_and_update(query, {'$set': {event_query: event_to_save}})

	#saved_events : {id: jbasjhfbjsh, another_id: ajsdbljsab}
	#dot notation selects a key

	return 'True'


@mod.route('/delete-saved-event/', methods=['POST'])
@is_logged_in
def delete_saved_event():
	response = request.get_json()
	print('RESPONSE ==', response)
	event_id = response['event_id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']
	user = users.find_one(query)

	print(event_id)

	event_query = QueryKeys.SAVED_EVENTS + "." + str(event_id)
	users.find_one_and_update(query, {'$unset': {event_query: event_id}})
	return 'True'



@mod.route('/save-poll/', methods=['POST'])
@is_logged_in
def save_poll():
	save = request.get_json()
	poll_id = save[QueryKeys.POLL_ID]

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)
	current_saved_polls = current_user_state['saved_polls'] if 'saved_polls' in current_user_state else None
	if current_saved_polls and poll_id in current_saved_polls:
		return 'False'

	print( poll_id)
	poll_query = QueryKeys.SAVED_POLLS + "." + poll_id
	users.find_one_and_update(query, {'$set': {poll_query: save}})

	return 'True'

@mod.route('/delete-saved-poll/', methods=['POST'])
@is_logged_in
def delete_saved_poll():
	save = request.get_json()
	poll_id = save[QueryKeys.POLL_ID]

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)

	print( poll_id)
	poll_query = QueryKeys.SAVED_POLLS + "." + poll_id
	users.find_one_and_update(query, {'$unset': {poll_query: save}})

	return 'True'

@mod.route('/save-legislator/', methods=['POST'])
@is_logged_in
def save_legislator():
	save = request.get_json()
	legislator_id = save['id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)

	current_saved_legislators = current_user_state[QueryKeys.SAVED_LEGISLATORS] if QueryKeys.SAVED_LEGISLATORS in current_user_state else None
	if current_saved_legislators and legislator_id in current_saved_legislators:
		return 'False'

	print( legislator_id)
	legislator_query = QueryKeys.SAVED_LEGISLATORS + "." + legislator_id
	users.find_one_and_update(query, {'$set': {legislator_query: save}})

	return 'True'

@mod.route('/delete-saved-legislator/', methods=['POST'])
@is_logged_in
def delete_saved_legislator():
	save = request.get_json()
	legislator_id = save['id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	print( legislator_id)
	legislator_query = QueryKeys.SAVED_LEGISLATORS + "." + legislator_id
	users.find_one_and_update(query, {'$unset': {legislator_query: save}})

	return 'Request to delete made'


@mod.route('/save-national-bill/', methods=['POST'])
@is_logged_in
def save_national_bill():
	save = request.get_json()
	bill_id = save['bill_id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)
	current_saved_bills = current_user_state['saved_national_bills'] if 'saved_national_bills' in current_user_state else None
	if current_saved_bills and bill_id in current_saved_bills:
		return 'False'

	print(bill_id)
	bill_query = "saved_national_bills" + "." + bill_id
	users.find_one_and_update(query, {'$set': {bill_query: save}})

	return 'True'

@mod.route('/save-state-bill/', methods=['POST'])
@is_logged_in
def save_state_bill():
	save = request.get_json()
	bill_id = save['bill_id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)
	current_saved_bills = current_user_state['saved_state_bills'] if 'saved_state_bills' in current_user_state else None
	if current_saved_bills and bill_id in current_saved_bills:
		return 'False'

	print(bill_id)
	bill_query = "saved_state_bills" + "." + bill_id
	users.find_one_and_update(query, {'$set': {bill_query: save}})

	return 'True'

@mod.route('/delete-saved-national-bill/', methods=['POST'])
@is_logged_in
def delete_national_bill():
	save = request.get_json()
	bill_id = save['bill_id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)

	print(bill_id)
	bill_query = 'saved_national_bills' + "." + bill_id
	users.find_one_and_update(query, {'$unset': {bill_query: save}})

	return 'True'

@mod.route('/delete-saved-state-bill/', methods=['POST'])
@is_logged_in
def delete_state_bill():
	save = request.get_json()
	bill_id = save['bill_id']

	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	current_user_state = users.find_one(query)

	print(bill_id)
	bill_query = 'saved_state_bills' + "." + bill_id
	users.find_one_and_update(query, {'$unset': {bill_query: save}})

	return 'True'
