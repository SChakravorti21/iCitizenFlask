from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from iCitizenFlaskApp.forms import RegisterForm, LoginForm

from iCitizenFlaskApp.dbconfig import db, QueryKeys

from iCitizenFlaskApp.models.legislator import Legislator
from iCitizenFlaskApp.models.bill import Bill

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
			return redirect( url_for('users.load_dashboard'))

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
		flash('''We noticed that your profile is incomplete. 
				This information will be useful in helping us find relevant
				information for you. We will never share any of this information externally.''', 'info')
		return redirect( url_for('functions.update_preferences') )

	return render_template('dashboard.html')

@mod.route('/update_db/', methods=['POST'])
def update_dashboard():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	location = user[QueryKeys.LOCATION]

	address = location[QueryKeys.ADDRESS]
	city = location[QueryKeys.CITY]
	state = location[QueryKeys.STATE]
	zipcode = location[QueryKeys.ZIPCODE]
	#latitude = location[QueryKeys.LATITUDE]
	#longitude = location[QueryKeys.LONGITUDE]

	national_legislators = Legislator.get_national_legislators(address, city, state, zipcode)
	state_legislators = Legislator.get_state_legislators(address, city, state, zipcode)

	return "Done"