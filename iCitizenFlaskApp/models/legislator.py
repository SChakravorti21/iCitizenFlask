'''
The Legislator class provides a standard template and format for legislator information to be used throughout the application
'''

import requests, json
from congress import Congress as national
from pygeocoder import Geocoder
import os

class Legislator(object):

    def __init__(self, level, first_name, last_name, state, chamber, id, party, photo_url = None, district=None):
        self.level = level
        self.first_name = first_name
        self.last_name = last_name
        self.state = state
        self.chamber = chamber
        self.id = id
        self.party = party
        self.photo_url = photo_url
        self.district = district

    def print_info(self):
        print("Name: {first_name} {last_name} ".format(first_name = self.first_name, last_name = self.last_name))
        print("Chamber: {chamber}, State: {state}, Party: {party}".format(chamber = self.chamber, state = self.state, party = self.party))
        if self.district is not None:
            print("District: {}".format(self.district))

        print('\n')

    def json(self):
        return {
            "level": self.level,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "state": self.state,
            "chamber": self.chamber,
            "id": self.id,
            "party": self.party,
            "photo_url": self.photo_url,
            "district": self.district
        }

    @classmethod
    def get_national_legislators(cls, address, city, state, zipcode):
        google_base = "https://www.googleapis.com/civicinfo/v2/"
    
        national_base = "https://api.propublica.org/congress/v1/"

        legislators = []
        fullAddress = address + ", " + city + ", " + state + " " + zipcode
        google_params = {"address": fullAddress, "includeOffices": True, "levels": "country", "roles": ["legislatorLowerBody","legislatorUpperBody"], "key": os.environ['GOOGLE_API_KEY']}
        google_response = requests.get(google_base+"representatives/", google_params)
        google_data = json.loads(google_response.text)

        offices = google_data['offices']
        districtId = offices[1]['divisionId'][36:]
        
        national_params = {"X-API-Key": os.environ['PROPUBLICA_API_KEY']}
        national_senate_response = requests.get(national_base+"members/senate/{}/current.json".format(state), headers=national_params)

        national_senate_data = json.loads(national_senate_response.text)

        senators = national_senate_data['results']
        for senator in senators:
            level = "national"
            first_name = senator['first_name']
            last_name = senator['last_name']
            chamber = "Senate"
            id = senator['id']
            party = senator['party']
            photo_url = "https://theunitedstates.io/images/congress/original/{}.jpg".format(id)
            legislators.append(cls(level, first_name, last_name, state, chamber, id, party, photo_url=photo_url))


        national_house_response = requests.get(national_base+"members/house/{}/{}/current.json".format(state, districtId), headers=national_params)

        national_house_data = json.loads(national_house_response.text)

        representatives = national_house_data['results']
        for rep in representatives:
            level = "national"
            first_name = rep['first_name']
            last_name = rep['last_name']
            chamber = "House"
            id = rep['id']
            party = rep['party']
            photo_url = "https://theunitedstates.io/images/congress/original/{}.jpg".format(id)
            legislators.append(cls(level, first_name, last_name, state, chamber, id, party, photo_url=photo_url, district=districtId))

        return legislators

    @classmethod
    def get_state_legislators(cls, address, city, state, zipcode, latitude=None, longitude=None):
        state_base = "https://openstates.org/api/v1/"

        legislators = []
        fullAddress = address + ", " + city + ", " + state + " " + zipcode
        if latitude is None:
            location = Geocoder.geocode(fullAddress)
            latitude = location.latitude
            longitude = location.longitude
        state_params = {"lat": latitude, "long": longitude, "apikey": os.environ['OPENSTATES_API_KEY']}

        state_legislative_response = requests.get(state_base+"legislators/geo/", state_params)
        state_legislative_data = json.loads(state_legislative_response.text)

        for rep in state_legislative_data:
            level = "state"
            first_name = rep['first_name']
            last_name = rep['last_name']
            chamber = rep['chamber']
            id = rep['id']
            party = rep['party']
            district = rep['district']
            photo_url = rep['photo_url']
            legislators.append(cls(level, first_name, last_name, state, chamber, id, party, photo_url =photo_url, district=district))

        return legislators
