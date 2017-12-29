import pyopenstates as states
from congress import Congress as national
import requests

states.set_api_key('70e23970-e0b4-409b-a7d2-3e34f6b88905')
cong = national('Fl38VvBXk8EFlAmEcG4N0Wq1hi6YPnyzi5YODT9k')

base = "https://www.googleapis.com/civicinfo/v2/"

def getLegislators(address):
    params = {"address": address, "key": "AIzaSyBLns0lxH3J7iMYIMaWCUtOX5lwsKhdBd4"}
    response = requests.get(base+"representatives/", params)
    print(response.content)

getLegislators("17 Queensboro Terrace, East Windsor, NJ 08520")
