from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import json
from bson import json_util

from iCitizenFlaskApp.forms import RegisterForm, LoginForm

from iCitizenFlaskApp.dbconfig import db, QueryKeys

from iCitizenFlaskApp.views.user_data import call_celery_task

from iCitizenFlaskApp.models.legislator import Legislator
from iCitizenFlaskApp.models.bill import Bill
from iCitizenFlaskApp.models.event import Event as EventClass

mod = Blueprint('users', __name__)

# Check if user logged in
def is_logged_in(f):
    """This wrapper function is used to ensure that user-related routes
    are only accessed by a user who is logged in.

    Args:
        f (function): a function for handling a user route, such as
            showing polls or showing events.

    Returns:
        The function passed in if a user is logged in, otherwise a redirect
        to the login page with a flashed error.
    """

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
    """This function supports HTTP GET and POST requests to the registration page.

    The custom WTForm RegisterForm is used to validate user input. The form
    imposes required input fields (username, password, confirm). Passwords are
    encrypted using the sha256_crypt module in the passlib library to prevent saving
    plain-text passwords in the database.
    """

    # If this was a POST request, get the form from the request
    form = RegisterForm(request.form)

    # Validate the form before processing inputted information
    if request.method == 'POST' and form.validate():
        # Get all form data
        name = form.name.data
        email = form.email.data
        username = form.username.data
        plain_password = str(form.password.data)

        # Encrypt the password using a modified sha256 algorithm
        password = sha256_crypt.encrypt(plain_password)

        """
        Add the user to the database. Since INPUTTED_PREFS is False, user will
        first get redirected to enter their preferences. The UPDATE flags are True
        so that celery workers can be allocated the task of fetching civic
        information for the user.
        """
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
            QueryKeys.UPDATE_POLLS: True,
			QueryKeys.SAVED_EVENTS: {},
            QueryKeys.SAVED_NATIONAL_BILLS: {},
            QueryKeys.SAVED_STATE_BILLS: {},
            QueryKeys.SAVED_POLLS: {},
            QueryKeys.SAVED_LEGISLATORS: {}
        }).inserted_id

        # Confirm registration of the user and redirect to login page
        flash('You are now registered and can log in!', 'success')
        return redirect( url_for('users.login'))

    # Just render the template if it was a GET request, or if the POST form failed to validate
    return render_template('register.html', form=form)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """This function supports HTTP GET and POST requests to the login page.

    The custom WTForm LoginForm is used to validate user input. The form
    imposes required input fields (username, password). Passwords are
    decrypted using the sha256_crypt module in the passlib library since
    they are encrypted before storing in the database.
    """

    # Get the form if this was a POST request
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():

        username = form.username.data
        entered_password = str(form.password.data)

        # Get the user from db
        query = {QueryKeys.USERNAME: username}
        users = db['users']
        user = users.find_one(query)

        """
        If the user does not exist or their password does not get decrypted to the stored
        password, prevent them from logging in.
        """
        if user is None or not sha256_crypt.verify(entered_password, user['password']):
            flash('Invalid username or password', 'danger')
        else:
            # Otherwise set the session variables to identify the user
            session['logged_in'] = True
            session[QueryKeys.USERNAME] = username

            flash('You have successfully logged in!', 'success')

            # Indicate to dashboard that celery workers need to be assigned work
            users.find_one_and_update(query, {'$set':{
                QueryKeys.UPDATE_DB: True,
                QueryKeys.UPDATE_BILLS: True,
                QueryKeys.UPDATE_POLLS: True,
                QueryKeys.UPDATE_EVENTS: True,
                QueryKeys.IS_UPDATING: False}
            })

            # Redirect to dashboard
            return redirect( url_for('users.load_dashboard'))

    # Just render the template if it wasn't a POST request, or if the form failed to validate
    return render_template('login.html', form=form)

@mod.route('/logout/', methods=['GET'])
@is_logged_in
def logout():
    """This function handles logging users out.

    This is achieved quite simply by resetting the session values and
    clearing the session cookies.
    """
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']
    session['logged_in'] = False
    session[QueryKeys.USERNAME] = None
    session.clear()

    # Redirect to login page if user logged out accidentally
    flash('You have successfully logged out!', 'success')
    return redirect( url_for('index'))

@mod.route('/dashboard/', methods=['GET'])
@is_logged_in
def load_dashboard():
    """This function handles getting the user's dashboard.

    If the user is logging in for the first time during this session,
    celery workers will be tasked with fetching user-related civic
    information.
    """
    # Check if preferences have been inputted
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)
    # Check if the user has inputted their preferences, as these are critical in
    # fetching relevant information.
    if not user[QueryKeys.INPUTTED_PREFERENCES]:
        # Redirect to input those preferences
        flash('''We noticed that your profile is incomplete.
                This information will be useful in helping us find relevant
                information for you. We will never share any of this information externally.''', 'info')
        return redirect( url_for('functions.update_preferences'))

    # If the database needs to be updated, do so.
    if user[QueryKeys.UPDATE_DB] and not user[QueryKeys.IS_UPDATING]:
        users.find_one_and_update(query, {'$set':{QueryKeys.IS_UPDATING: True}})
        print('calling celery task')
        call_celery_task()

    return render_template('dashboard.html', db_client=user)

@mod.route('/events/', methods = ['GET', 'POST'])
@is_logged_in
def show_events():
    """Loads the user's events page. 

    Loading of events is handled asynchronously through ajax POST requests to a
    separate endpoint (/get-user-events-db/).
    """
    return render_template('events.html')


@mod.route('/polls/', methods=['GET'])
@is_logged_in
def show_polls():
    """Loads the user's polls page. 

    Loading of polls is handled asynchronously through ajax POST requests to a
    separate endpoint (/get-user-polls/).
    """
    return render_template('polls.html')

@mod.route('/legislators/', methods=['GET'])
@is_logged_in
def show_legislators():
    """Loads the user's legislators page. 

    Loading of legislators is handled asynchronously through ajax POST requests to
    separate endpoints (/get-national-legislators-db/ and /get-state-legislators-db/).
    """
    return render_template('legislators.html')

@mod.route('/bills/', methods=['GET'])
@is_logged_in
def show_bills():
    """Loads the user's bills page. 

    Loading of bills is handled asynchronously through ajax POST requests to
    separate endpoints (/get-national-bills-db/ and /get-state-bills-db/).
    """
    return render_template('bills.html')

@mod.route('/get-state-bills-db/', methods=['POST'])
@is_logged_in
def get_state_bills():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    state_bills_jsons = user['state_bills'] if 'state_bills' in user else None
    saved_bills_jsons = user[QueryKeys.SAVED_STATE_BILLS] if QueryKeys.SAVED_STATE_BILLS in user else None

    jsons = {
        QueryKeys.STATE_BILLS: state_bills_jsons,
        QueryKeys.SAVED_STATE_BILLS: saved_bills_jsons
    }

    if user[QueryKeys.UPDATE_BILLS] == True:
        jsons = None

    return json.dumps(jsons, sort_keys=True, indent=4, default=json_util.default)

@mod.route('/get-national-bills-db/', methods=['POST'])
@is_logged_in
def get_national_bills():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    national_bills_jsons = user[QueryKeys.NATIONAL_BILLS] if QueryKeys.NATIONAL_BILLS in user else None
    saved_bills_jsons = user[QueryKeys.SAVED_NATIONAL_BILLS] if QueryKeys.SAVED_NATIONAL_BILLS in user else None

    jsons = {
        QueryKeys.NATIONAL_BILLS: national_bills_jsons,
        QueryKeys.SAVED_NATIONAL_BILLS: saved_bills_jsons
    }

    if user[QueryKeys.UPDATE_BILLS] == True:
        jsons = None

    return json.dumps(jsons, sort_keys=True, indent=4, default=json_util.default)


'''
Looks at user database to get the saved events and the top n event list, and puts them in a Dictionary

@param None
@return Dictionary of user_events and saved_events to be accessed by the event_data_loader.js
'''
@mod.route('/get-user-events-db/', methods=['POST'])
@is_logged_in
def get_user_events():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']
    user = users.find_one(query)

    user_events_jsons = user[QueryKeys.USER_EVENTS] if QueryKeys.USER_EVENTS in user else None
    saved_events_jsons = user[QueryKeys.SAVED_EVENTS] if QueryKeys.SAVED_EVENTS in user else {}
    comb_json = {QueryKeys.USER_EVENTS: user_events_jsons,
                QueryKeys.SAVED_EVENTS: saved_events_jsons}

    if user[QueryKeys.UPDATE_EVENTS] == True:
        comb_json = None

    # print('SAVED EVENTS = ', saved_events_jsons)
    return json.dumps(comb_json, sort_keys=True, indent=4, default=json_util.default)

@mod.route('/get-user-polls/', methods=['POST'])
@is_logged_in
def get_user_polls():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    user_polls_jsons = user[QueryKeys.USER_POLLS] if QueryKeys.USER_POLLS in user else None
    saved_polls_json = user[QueryKeys.SAVED_POLLS] if QueryKeys.SAVED_POLLS in user else {}

    ret_json = {
        QueryKeys.USER_POLLS: user_polls_jsons,
        QueryKeys.SAVED_POLLS: saved_polls_json
    }

    if user[QueryKeys.UPDATE_POLLS] == True:
        ret_json = None

    return json.dumps(ret_json, sort_keys=True, indent=4, default=json_util.default)

@mod.route('/get-state-legislators-db/', methods=['POST'])
@is_logged_in
def get_state_legislators():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    user_legislators_jsons = user[QueryKeys.STATE_LEGISLATORS] if QueryKeys.STATE_LEGISLATORS in user else {}
    saved_legislators_jsons = user[QueryKeys.SAVED_LEGISLATORS] if QueryKeys.SAVED_LEGISLATORS in user else {}

    ret_json = {
        QueryKeys.STATE_LEGISLATORS: user_legislators_jsons,
        QueryKeys.SAVED_LEGISLATORS: saved_legislators_jsons
    }

    if user[QueryKeys.UPDATE_DB] == True:
        ret_json = None

    return json.dumps(ret_json, sort_keys=True, indent=4, default=json_util.default)

@mod.route('/get-national-legislators-db/', methods=['POST'])
@is_logged_in
def get_national_legislators():
    query = {QueryKeys.USERNAME: session[QueryKeys.USERNAME]}
    users = db['users']

    user = users.find_one(query)

    user_legislators_jsons = user[QueryKeys.NATIONAL_LEGISLATORS] if QueryKeys.NATIONAL_LEGISLATORS in user else {}
    saved_legislators_jsons = user[QueryKeys.SAVED_LEGISLATORS] if QueryKeys.SAVED_LEGISLATORS in user else {}

    ret_json = {
        QueryKeys.NATIONAL_LEGISLATORS: user_legislators_jsons,
        QueryKeys.SAVED_LEGISLATORS: saved_legislators_jsons
    }

    if user[QueryKeys.UPDATE_DB] == True:
        ret_json = None

    return json.dumps(ret_json, sort_keys=True, indent=4, default=json_util.default)
