from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from pygeocoder import Geocoder

from iCitizenFlaskApp.forms import PreferencesForm
from iCitizenFlaskApp.dbconfig import db, QueryKeys
from iCitizenFlaskApp.data import SUBJECTS
from iCitizenFlaskApp.views.user_routes import is_logged_in

mod = Blueprint('functions', __name__)

@mod.route('/events', methods = ['GET', 'POST'])
@is_logged_in
def show_events():
	from iCitizenFlaskApp.models import Event as EventClass
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']
	user = users.find_one(query)

	location = user[QueryKeys.LOCATION]
	state = location['state']
	city = location['city']
	prefs = user[QueryKeys.PREFERENCES]
	subjects = prefs['subjects']
	print(state, city)

	event_list = EventClass.get_top_n_events(state=state, city=city, pref_subjs = subjects, num_pages = 5, num_events = 10)


	return render_template('events.html', event_list = event_list)

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

	print(QueryKeys.INPUTTED_PREFERENCES)
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
			location = Geocoder.geocode("{}, {}, {}, {}, {}".format(address, city, state, country, zipcode))

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

			print(address_obj)
			print(preferences_obj)

			user = users.find_one_and_update(query, {'$set':
				{
					QueryKeys.INPUTTED_PREFERENCES: True,
					QueryKeys.PREFERENCES: preferences_obj,
					QueryKeys.LOCATION: address_obj
				}})
			print(user)

			flash('Your preferences have been updated!', 'success')
			return redirect( url_for('functions.show_profile'))

	return render_template('update_preferences.html', form=form,
		subjects=[(str(subject).strip(), subject) for subject in SUBJECTS],
		selected_subjects=topics, error=error)
