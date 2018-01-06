from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from functools import wraps
from apiclient.discovery import build

from iCitizenFlaskApp.dbconfig import db, QueryKeys

from iCitizenFlaskApp.models.legislator import Legislator
from iCitizenFlaskApp.models.bill import Bill
from iCitizenFlaskApp.models.event import Event as EventClass

from iCitizenFlaskApp import celery_worker_bills, celery_worker_events, celery_worker_polls

mod = Blueprint('data', __name__)

def call_celery_task():
    username = session[QueryKeys.USERNAME]
    load_bills.delay(username)
    load_events.delay(username)
    load_polls.delay(username)
    return "Work assigned to celery workers"


@celery_worker_bills.task
def load_bills(username):
    print("started bills")
    update_bills(username)

@celery_worker_events.task
def load_events(username):
    print("started events")
    update_events(username)

@celery_worker_polls.task
def load_polls(username):
    print("started polls")
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

    users.find_one_and_update(query, {'$set': {'national_bills': national_bills_jsons}})

    users.find_one_and_update(query, {'$set': {'state_bills' : state_bills_jsons}})

    user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_BILLS : False}})
    user = users.find_one(query)
    if user[QueryKeys.UPDATE_EVENTS] == False:
        user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_DB : False,
                                                            QueryKeys.IS_UPDATING: False}})

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
        user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_DB : False,
                                                            QueryKeys.IS_UPDATING: False}})

    return "Events have been written"

def update_polls(username):
    import hashlib

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

    if info:
        # Set a unique id for each poll, used when saving polls
        contests = info['contests']
        for data in contests:
            # First cast the data into a string, encode that to bytes, and finally get a hash for it
            # (does not need to be cyptographically secure, just need to store in db)
            hash_obj = hashlib.md5(str(data).encode('utf-8'))
            poll_id = hash_obj.hexdigest()
            print('ID when storing: {}'.format(poll_id))
            data[QueryKeys.POLL_ID] = poll_id

    users.find_one_and_update(query, {'$set': {'user_polls': info}})

    user = users.find_one_and_update(query, {'$set': {QueryKeys.UPDATE_POLLS : False}})

    return "Polls written to DB"
