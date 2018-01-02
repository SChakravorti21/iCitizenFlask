from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from functools import wraps
from apiclient.discovery import build

from iCitizenFlaskApp.dbconfig import db, QueryKeys

from iCitizenFlaskApp.models.legislator import Legislator
from iCitizenFlaskApp.models.bill import Bill
from iCitizenFlaskApp.models.event import Event as EventClass

from iCitizenFlaskApp.views.user_routes import is_logged_in

from iCitizenFlaskApp import celery_app

mod = Blueprint('data', __name__)

@mod.route('/load_db/', methods=["POST"])
@is_logged_in
def call_celery_task():
    username = session[QueryKeys.USERNAME]
    load_db.delay(username)
    return "Work assigned to celery worker"

@celery_app.task
def load_db(username):
    update_bills(username)
    update_events(username)
    update_polls(username)

def update_bills(username):
    import time

    start_time = time.time()

    query = {QueryKeys.USERNAME: username}
    users = db['users']

    user = users.find_one(query)
    if 'national_legislators' not in user:
        set_legislators(username)
        user = users.find_one(query)

    national_legislators = [Legislator(**kwargs) for kwargs in user['national_legislators']]
    state_legislators = [Legislator(**kwargs) for kwargs in user['state_legislators']]

    subjects = [subject for subject in user[QueryKeys.PREFERENCES]['subjects']]

    national_bills = Bill.get_national_bills(national_legislators, subjects)
    state_bills = Bill.get_state_bills(state_legislators, ["Crime", "Health"], user['location']['state'])

    national_bills_jsons = [bill.json() for bill in national_bills]
    state_bills_jsons = [bill.json() for bill in state_bills]

    users.find_one_and_update(query, {'$set': {'national_bils': national_bills_jsons}})

    users.find_one_and_update(query, {'$set': {'state_bills' : state_bills_jsons}})

    user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_BILLS : False}})
    user = users.find_one(query)
    if user[QueryKeys.UPDATE_EVENTS] == False:
        user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_DB : False}})

    print("Time for bills to finish: {} seconds".format(str(time.time() - start_time)))
    return "Bills written to DB"

def set_legislators(username):
    query = {QueryKeys.USERNAME: username}
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


def update_events(username):
    query = {QueryKeys.USERNAME: username}
    users = db['users']
    user = users.find_one(query)

    location = user[QueryKeys.LOCATION]
    state = location['state']
    city = location['city']
    prefs = user[QueryKeys.PREFERENCES]
    subjects = prefs['subjects']

    event_list = EventClass.get_top_n_events(state=state, city=city, pref_subjs = subjects, num_pages = 3, num_events = 15)

    user_events_jsons = [event.json() for event in event_list]

    users.find_one_and_update(query, {'$set': {'user_events': user_events_jsons}})

    user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_EVENTS : False}})
    user = users.find_one(query)
    if user[QueryKeys.UPDATE_BILLS] == False:
        user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_DB : False}})

    return "Events have been written"

def update_polls(username):
    query = {QueryKeys.USERNAME: username}
    users = db['users']
    user = users.find_one(query)

    service = build('civicinfo', 'v2', developerKey='AIzaSyBPGcxWwvhkETJav0mjck4jF1lHRuKiQmc')
    elections = service.elections()

    location = user[QueryKeys.LOCATION]
    address = "{}, {}, {}, {} {}".format(location[QueryKeys.ADDRESS],
                                            location[QueryKeys.CITY],
                                            location[QueryKeys.STATE],
                                            location[QueryKeys.COUNTRY],
                                            location[QueryKeys.ZIPCODE])
    info = service.elections().voterInfoQuery(address=address, electionId="2000", 
        returnAllAvailableData=True, officialOnly=False).execute()

    print(info)

    users.find_one_and_update(query, {'$set': {'user_polls': info}})

    user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_POLLS : False}})

    return "Polls written to DB"
