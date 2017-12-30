from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from iCitizenFlaskApp.forms import RegisterForm, LoginForm, PreferencesForm

from iCitizenFlaskApp.dbconfig import db, QueryKeys
from iCitizenFlaskApp.data import SUBJECTS

mod = Blueprint('users', __name__)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)

	if request.method == 'POST' and form.validate():
		# Add user to database
		name = form.name.data
		email = form.email.data
		username = form.username.data
		plain_password = str(form.password.data)

		password = sha256_crypt.encrypt(plain_password)

		users = db['users']
		insert_id = users.insert_one({
			QueryKeys.NAME: name,
			QueryKeys.EMAIL: email,
			QueryKeys.USERNAME: username,
			QueryKeys.PASSWORD: password,
			QueryKeys.INPUTTED_PREFERENCES: False
		}).inserted_id

		print(str(insert_id))

		flash('You are now registered and can log in!', 'success')

		return redirect( url_for('users.login'))

	# Just render the template if it wasn't a POST request, or if the form failed to validate
	return render_template('register.html', form=form)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate():

		username = form.username.data
		entered_password = str(form.password.data)

		query = {'username': username}
		users = db['users']

		user = users.find_one(query)
		print(user)

		if user is None or not sha256_crypt.verify(entered_password, user['password']):
			flash('Invalid username or password', 'danger')
		else:
			session['logged_in'] = True
			session[QueryKeys.USERNAME] = username

			flash('You have successfully logged in!', 'success')
			return redirect( url_for('index'))

	# Just render the template if it wasn't a POST request, or if the form failed to validate
	return render_template('login.html', form=form)

@mod.route('/logout/', methods=['GET'])
def logout():
	session['logged_in'] = False
	session[QueryKeys.USERNAME] = None

	flash('You have successfully logged out!', 'success')
	return redirect( url_for('index'))

@mod.route('/dashboard/', methods=['GET'])
def load_dashboard():
	# Check if preferences have been inputted
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	print(user[QueryKeys.INPUTTED_PREFERENCES])
	if not user[QueryKeys.INPUTTED_PREFERENCES]:
		# Redirect to input those preferences

		return redirect( url_for('users.update_preferences') )

	return render_template('dashboard.html')

@mod.route('/update-prefs/', methods=['GET', 'POST'])
def update_preferences():
	form = PreferencesForm(request.form)
	topics = []
	error = None

	# Prefill the preferences if the user has set them before
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']
	user = users.find_one(query)

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
		topics = request.form.getlist('subjects')
		if not topics or len(topics) == 0:
			error = 'Please choose at least one topic so that we can find bills that are relevant for you'
			pass

		if form.validate():
			party = form.political_party.data
			address = form.address.data
			city = form.city.data
			state = form.state.data
			country = form.country.data
			zipcode = form.zipcode.data

			address_obj = {
				QueryKeys.ADDRESS: address,
				QueryKeys.CITY: city,
				QueryKeys.STATE: state,
				QueryKeys.COUNTRY: country,
				QueryKeys.ZIPCODE: zipcode,
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

	return render_template('update_preferences.html', form=form, 
		subjects=[(str(subject).strip().lower(), subject) for subject in SUBJECTS], 
		selected_subjects=topics, error=error)
