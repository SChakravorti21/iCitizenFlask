import requests, json
from congress import Congress as national
from pygeocoder import Geocoder

google_base = "https://www.googleapis.com/civicinfo/v2/"
state_base = "https://openstates.org/api/v1/"
national_base = "https://api.propublica.org/congress/v1/"

def getLegislators(address, city, state, zipcode):
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
        print(senator['name'])

    national_house_response = requests.get(national_base+"members/house/{}/{}/current.json".format(state, districtId), headers=national_params)

    national_house_data = json.loads(national_house_response.text)

    representatives = national_house_data['results']
    for rep in representatives:
        print(rep['name'])

    location =  Geocoder.geocode(fullAddress)
    state_params = {"lat":location.latitude, "long":location.longitude, "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}

    state_legislative_response = requests.get(state_base+"legislators/geo/", state_params)
    state_legislative_data = json.loads(state_legislative_response.text)

    for rep in state_legislative_data:
        print(rep['full_name'])


#Legislator.get_national_legislators("17 Queensboro Terrace", "East Windsor",  "NJ",  "08520").print_info()
#getLegislators("17 Queensboro Terrace", "East Windsor",  "NJ",  "08520")
#getStateBills("nj", "Crime")

