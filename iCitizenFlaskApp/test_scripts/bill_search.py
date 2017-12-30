import requests, json
from congress import Congress as national
from pygeocoder import Geocoder

google_base = "https://www.googleapis.com/civicinfo/v2/"
state_base = "https://openstates.org/api/v1/"
national_base = "https://api.propublica.org/congress/v1/"



def get_national_bills(legislators, subjects, party):
    national_params = {"X-API-Key": "Fl38VvBXk8EFlAmEcG4N0Wq1hi6YPnyzi5YODT9k"}
    for legislator in legislators:
        rep_bill_response = requests.get(national_base+"members/{}/bills/introduced.json".format(legislator.id), headers=national_params)
        rep_bill_data = json.loads(rep_bill_response.text)['results'][0]['bills']

        for bill in rep_bill_data:
            print(bill['bill_id'])



    