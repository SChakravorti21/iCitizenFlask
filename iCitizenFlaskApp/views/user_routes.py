from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from iCitizenFlaskApp.forms import RegisterForm, LoginForm

from iCitizenFlaskApp.dbconfig import db, QueryKeys

from iCitizenFlaskApp.models.legislator import Legislator
from iCitizenFlaskApp.models.bill import Bill

mod = Blueprint('users', __name__)

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		print("logged_in in session: {}".format('logged_in' in session))
		if 'logged_in' in session and session['logged_in'] is not False:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, please login', 'danger')
			return redirect(url_for('users.login'))
	return wrap

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
			QueryKeys.INPUTTED_PREFERENCES: False,
			QueryKeys.UPDATE_DB: True
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
@is_logged_in
def logout():
	session['logged_in'] = False
	session[QueryKeys.USERNAME] = None
	session.clear()

	flash('You have successfully logged out!', 'success')
	return redirect( url_for('index'))

@mod.route('/dashboard/', methods=['GET'])
@is_logged_in
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

	return render_template('dashboard.html', db_client=user)

@mod.route('/events/', methods=['GET'])
@is_logged_in
def load_events():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	return render_template('events.html', db_client=user)

@mod.route('/polls/', methods=['GET'])
@is_logged_in
def load_polls():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	return render_template('events.html', db_client=user)

@mod.route('/legislators/', methods=['GET'])
@is_logged_in
def load_legislators():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	return render_template('events.html', db_client=user)

@mod.route('/bills/', methods=['GET'])
@is_logged_in
def load_bills():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	return render_template('events.html', db_client=user)

@mod.route('/update_db/', methods=['POST'])
@is_logged_in
def update_db():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	if 'national_legislators' not in user:
    		set_legislators()
	user = users.find_one(query)
	
	national_legislators = [Legislator(**kwargs) for kwargs in user['national_legislators']]
	state_legislators = [Legislator(**kwargs) for kwargs in user['state_legislators']]

	subjects = [subject for subject in user[QueryKeys.PREFERENCES]['subjects']]

	national_bills = Bill.get_national_bills(national_legislators, subjects)
	state_bills = Bill.get_state_bills(state_legislators, ["Crime", "Health"], user['location']['state'])

	user_national_bills = db["{}_national_bills".format(session[QueryKeys.USERNAME])]
	user_state_bills = db["{}_state_bills".format(session[QueryKeys.USERNAME])]

	for bill in national_bills:
    		user_national_bills.insert(bill.json())

	for bill in state_bills:
    		user_state_bills.insert(bill.json())

	user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_DB : False}})


	return "Test wrote to DB"

def set_legislators():
	query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
	users = db['users']

	user = users.find_one(query)
	location = user[QueryKeys.LOCATION]

	address = location[QueryKeys.ADDRESS]
	city = location[QueryKeys.CITY]
	state = location[QueryKeys.STATE]
	zipcode = location[QueryKeys.ZIPCODE]
	latitude = location[QueryKeys.LATLONG][QueryKeys.LATITUDE]
	longitude = location[QueryKeys.LATLONG][QueryKeys.LONGITUDE]

	national_legislators = Legislator.get_national_legislators(address, city, state, zipcode)
	state_legislators = Legislator.get_state_legislators(address, city, state, zipcode, latitude, longitude)

	national_legislators_jsons = [bill.json() for bill in national_legislators]
	state_legislators_jsons = [bill.json() for bill in state_legislators]

	users.find_one_and_update(query, {'$set': {'national_legislators': national_legislators_jsons}})

	users.find_one_and_update(query, {'$set': {'state_legislators' : state_legislators_jsons}})