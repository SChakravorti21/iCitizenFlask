from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from iCitizenFlaskApp.forms import RegisterForm, LoginForm

from iCitizenFlaskApp.dbconfig import db, QueryKeys

from iCitizenFlaskApp.models.legislator import Legislator
from iCitizenFlaskApp.models.bill import Bill
from iCitizenFlaskApp.models.event import Event as EventClass

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
            QueryKeys.UPDATE_DB: True,
            QueryKeys.UPDATE_EVENTS: True,
            QueryKeys.UPDATE_BILLS: True,
			QueryKeys.SAVED_EVENTS: []
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

@mod.route('/events/', methods = ['GET', 'POST'])
@is_logged_in
def show_events():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']
    user = users.find_one(query)
    '''
    if request.method == 'POST':
        prev_saved_events = user[QueryKeys.SAVED_EVENTS]
		update_user_saved_events(prev_saved_events)
        flash('TESTFLASH', 'success')
    '''


    event_list = [EventClass(**kwargs) for kwargs in user[QueryKeys.EVENT_LIST]]

    return render_template('events.html', event_list = event_list, db_client=user)


def update_user_saved_events(prev_saved_events):
	print('PREV SAVED EVENTS ARE', prev_saved_events)

	new_saved_events = request.form.getlist('box')

	if new_saved_events:

		mergedlist = list(set(prev_saved_events + new_saved_events))

		user = users.find_one_and_update(query, {'$set':{QueryKeys.SAVED_EVENTS: mergedlist}})
		print('NEW SAVED EVENTS iS ', mergedlist)


@mod.route('/polls/', methods=['GET'])
@is_logged_in
def load_polls():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)
    return render_template('polls.html', db_client=user)

@mod.route('/legislators/', methods=['GET'])
@is_logged_in
def load_legislators():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)
    return render_template('legislators.html', db_client=user)

@mod.route('/bills/', methods=['GET'])
@is_logged_in
def load_bills():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)
    return render_template('bills.html', db_client=user)
