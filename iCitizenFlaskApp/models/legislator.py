import requests, json
from congress import Congress as national
from pygeocoder import Geocoder

class Legislator(object):


    def __init__(self, level, firstName, lastName, state, chamber, id, party, district=None):
        self.level = level
        self.first_name = firstName
        self.last_name = lastName
        self.state = state
        self.chamber = chamber
        self.id = id
        self.party = party
        self.district = district

    def print_info(self):
        print("Name: {first_name} {last_name} ".format(first_name = self.first_name, last_name = self.last_name))
        print("Chamber: {chamber}, State: {state}, Party: {party}".format(chamber = self.chamber, state = self.state, party = self.party))
        if self.district is not None:
            print("District: {}".format(self.district))

        print('\n')

    @classmethod
    def get_national_legislators(cls, address, city, state, zipcode):
        google_base = "https://www.googleapis.com/civicinfo/v2/"
    
        national_base = "https://api.propublica.org/congress/v1/"

        legislators = []
        fullAddress = address + ", " + city + ", " + state + " " + zipcode
        google_params = {"address": fullAddress, "includeOffices": True, "levels": "country", "roles": ["legislatorLowerBody","legislatorUpperBody"], "key": "AIzaSyBLns0lxH3J7iMYIMaWCUtOX5lwsKhdBd4"}
        google_response = requests.get(google_base+"representatives/", google_params)
        google_data = json.loads(google_response.text)

        offices = google_data['offices']
        districtId = offices[1]['divisionId'][36:]
        
        national_params = {"X-API-Key": "Fl38VvBXk8EFlAmEcG4N0Wq1hi6YPnyzi5YODT9k"}
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
            legislators.append(cls(level, first_name, last_name, state, chamber, id, party))


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
            legislators.append(cls(level, first_name, last_name, state, chamber, id, party, districtId))

        return legislators

    @classmethod
    def get_state_legislators(cls, address, city, state, zipcode):
        state_base = "https://openstates.org/api/v1/"

        legislators = []
        fullAddress = address + ", " + city + ", " + state + " " + zipcode
        location =  Geocoder.geocode(fullAddress)
        state_params = {"lat":location.latitude, "long":location.longitude, "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}

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
            legislators.append(cls(level, first_name, last_name, state, chamber, id, party, district))

        return legislators
