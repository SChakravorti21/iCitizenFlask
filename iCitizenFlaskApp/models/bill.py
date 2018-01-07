'''
The Bill class helps organize data from the Open States and Propublica APIS into a single standard used by the rest of the application.
The class includes static methods to retrieve both state and national bills, while also defining the JSON format for every Bill object.
'''

from iCitizenFlaskApp.models.legislator import Legislator
import requests, json
from heapq import heappush, heappop, heapify
import os

class Bill(object):
    
    '''
    A Bill is defined by a number of attributes:

        Level: Whether the bill was introduced on a NATIONAL or STATE level

        Title: If available, a short title for the bill

        Description: What the bill intends to accomplish

        Author: The primary sponsor of the bill. If there are multiple primary sponsors, only the first is selected

        Author Id: The legislative id of the author, unique in both Congress and in state legislatures

        Bill Id: The unique legislative id assigned to each bill

        Id: (For State Bills only) - a different legislative id assigned to each bill

        Author Party: The party that the author belongs to

        Author State: Indicates the author's home state(mainly for national bills)

        Cosponsor Number: The number of total sponsors for the bill

        Created Date: The date that the bill was first introduced to the legislature

        Last Action: The date of the last recorded action taken on the bill, and if available, a description of said action

        Govtrack Link: (For National Bills Only) - the govtrack url for the bill

        Url: (For State Bills Only) - A link to the bill text
    '''

    def __init__(self, level, title, description, author, author_id, bill_id, id, author_party, author_state, cosponsor_num, created_date,
                 last_action = None, govtrack_link=None, url=None):
        self.level = level
        self.title = title
        self.description = description
        self.author = author,
        self.author_id = author_id
        self.bill_id = bill_id
        self.id = id
        self.author_party = author_party
        self.author_state = author_state
        self.cosponsor_num = cosponsor_num
        self.created_date = created_date
        self.last_action = last_action
        self.govtrack_link = govtrack_link
        self.url = url

    def json(self):
        return {
            "level": self.level,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "author_id": self.author_id,
            "bill_id": self.bill_id,
            "id": self.id,
            "author_party": self.author_party,
            "author_state": self.author_state,
            "cosponsor_num": self.cosponsor_num,
            "created_date": self.created_date,
            "last_action": self.last_action,
            "govtrack_link": self.govtrack_link,
            "url": self.url
        }

    @classmethod
    def get_national_bills(cls, legislators, subjects):
        
        '''
        The get_national_bills() method retrieves information from the ProPublica API, creates Bill objects, and then sorts them
            - Bills are first pulled based on the user's legislator, assigned points based on their relevancy, and put into a dictionary with Bill id as key
            - Then Bills are pulled based on subject, and their respective points are either updated or set in the dictionary
            - All bills in the dictionary are sorted and returned in sorted order
                - The ranking system is as follows:
                    - Bill's primary sponsor is one of the user's representatives: 4 points
                    - Bill is cosponsored by user's representatives: 2 points
                    - For each subject the bill is categorized according to: 4 points
                    - The (cosponsor_num / 5) is added to the point total of every bill
        '''

        bills = {}
        billPoints = {}

        bill_heap = []
        sorted_bills = []

        leg_ids = []

        national_base = "https://api.propublica.org/congress/v1/"
        national_params = {"X-API-Key": os.environ['PROPUBLICA_API_KEY'], "congress": "115"}

        #Loops through all legislators and ranks all bills sponsored or cosponsored by them
        for legislator in legislators:
            leg_ids.append(legislator.id)
            rep_bill_response = requests.get(national_base+"members/{}/bills/updated.json".format(legislator.id), headers=national_params)
            rep_bill_data = json.loads(rep_bill_response.text)['results'][0]['bills']

            for bill in rep_bill_data:
                level = "national"
                title = bill['short_title']
                description = bill['title']
                author = bill['sponsor_name']
                author_id = bill['sponsor_id']
                id = bill['bill_id']
                bill_id = id
                author_state = bill['sponsor_state']
                author_party = bill['sponsor_party']
                created_date = bill['introduced_date']
                last_action = "{} on {}".format(bill['latest_major_action'], bill['latest_major_action_date'])
                govtrack_link = bill['govtrack_url']
                cosponsor_num = bill['cosponsors']

                if bill_id in billPoints:
                    if author_id == legislator.id:
                        billPoints[bill_id] += 4
                    else:
                        billPoints[bill_id] += 2
                else:
                    if author_id == legislator.id:
                        billPoints[bill_id] = 4
                    else:
                        billPoints[bill_id] = 2
                    billPoints[bill_id] += (bill['cosponsors'] / 5)
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, author_party, author_state, cosponsor_num, created_date, 
                                        last_action = last_action, govtrack_link = govtrack_link)
                    bills[bill_id] = created_bill

        #For every subject that interests the user, bills are pulled and ranked
        for subject in subjects:
            sub_bill_response = requests.get(national_base+"bills/subjects/{}.json".format(subject), headers=national_params)

            sub_bill_json = json.loads(sub_bill_response.text)
            if 'results' not in sub_bill_json:
                continue
            sub_bill_data = sub_bill_json['results']

            for bill in sub_bill_data:
                level = "national"
                title = bill['short_title']
                description = bill['title']
                author = bill['sponsor_name']
                author_id = bill['sponsor_id']
                bill_id = bill['bill_id']
                id = bill_id
                author_state = bill['sponsor_state']
                author_party = bill['sponsor_party']
                created_date = bill['introduced_date']
                last_action = "{} on {}".format(bill['latest_major_action'], bill['latest_major_action_date'])
                govtrack_link = bill['govtrack_url']
                cosponsor_num = bill['cosponsors']

                if bill_id in billPoints:
                    if author_id in leg_ids:
                        billPoints[bill_id] += 4
                    billPoints[bill_id] += 5
                else:
                    billPoints[bill_id] = 5
                    billPoints[bill_id] += bill['cosponsors'] / 5
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, author_party, author_state, cosponsor_num, created_date, 
                                        last_action = last_action, govtrack_link = govtrack_link)
                    bills[bill_id] = created_bill

        count = 0

        for bill_id in billPoints:
            bill_heap.append((billPoints[bill_id] * -1, count, bills[bill_id]))
            count = count + 1

        #All bills are put into an array and then heapified in linear time

        heapify(bill_heap)

        #10 bills are popped from the heap to return a sorted list of the 10 highest ranked bills
        i = 0
        while i < 10:
            popped = heappop(bill_heap)
            sorted_bills.append(popped[2])
            i = i + 1

        print('success')
        return sorted_bills

    @classmethod
    def get_state_bills(cls, legislators, subjects, state):
        
        '''
        The get_state_bills() method retrieves information from the OpenStates API, creates Bill objects, and then sorts them
            - Bills are first pulled based on legislator, assigned points based on their relevancy, and put into a dictionary with Bill id as key
            - Then Bills are pulled based on subject, and their respective points are either updated or set in the dictionary
            - All bills in the dictionary are sorted and returned in sorted order
                - The ranking system is as follows:
                    - Bill's primary sponsor is one of the user's representatives: 4 points
                    - Bill is cosponsored by user's representatives: 2 points
                    - For each subject the bill is categorized according to: 4 points
                    - The cosponsor_num is added to the point total of every bill
        '''

        state_base = "https://openstates.org/api/v1/"

        bills = {}
        billPoints = {}

        bill_heap = []
        sorted_bills = []

        leg_ids = []

        #For every state legislator that represents the user, bills are pulled and ranked
        for legislator in legislators:
            leg_ids.append(legislator.id)

            #Due to the structuring of the OpenStates API, multiple requests must be made to the OpenStates API to retrieve all necessary information

            state_params = {"state": state, "sponsor_id": legislator.id, "search_window": "session", "apikey": os.environ['OPENSTATES_API_KEY']}
            state_params_version = {"state": state, "sponsor_id": legislator.id, "search_window": "session", "fields": "versions", "apikey": os.environ['OPENSTATES_API_KEY']}
            state_params_sponsor = {"state": state, "sponsor_id": legislator.id, "search_window": "session", "fields": "sponsors", "apikey": os.environ['OPENSTATES_API_KEY']}

            state_bill_response = requests.get(state_base+"bills/", state_params)
            state_bill_data = json.loads(state_bill_response.text)

            state_bill_version_response = requests.get(state_base+"bills/", state_params_version)
            state_bill_version = json.loads(state_bill_version_response.text)

            state_bill_sponsor_response = requests.get(state_base+"bills/", state_params_sponsor)
            state_bill_sponsor_data = json.loads(state_bill_sponsor_response.text)

            bill_urls = {}
            sponsor_names = {}
            sponsor_ids = {}
            sponsor_num = {}

            #Bill id is used as a key for all populated dictionaries below so that each bill can be created with correct information

            for version in state_bill_version:
                if len(version['versions']) < 1:
                    continue
                id = version['id']
                bill_urls[id] = version['versions'][0]['url']

            for sponsor in state_bill_sponsor_data:
                if len(sponsor['sponsors']) < 1:
                    continue
                id = sponsor['id']
                sponsor_names[id] = sponsor['sponsors'][0]['name']
                sponsor_ids[id] = sponsor['sponsors'][0]['leg_id']
                sponsor_num[id] = len(sponsor['sponsors'])
    
            for bill in state_bill_data:
                bill_id = bill['id']

                if bill_id not in sponsor_names or bill_id not in bill_urls:
                    continue

                level = "state"
                title = None
                description = bill['title']
                id = bill['bill_id']
                author_id = sponsor_ids[bill_id]
                url = bill_urls[bill_id]
                author = sponsor_names[bill_id]
                author_state = bill['state']
                author_party = legislator.party
                created_date = bill['created_at']
                last_action = bill['updated_at']
                cosponsor_num = sponsor_num[bill_id]

                if bill_id in billPoints:
                    if author_id == legislator.id:
                        billPoints[bill_id] += 4
                    else:
                        billPoints[bill_id] += 2
                else:
                    if author_id == legislator.id:
                        billPoints[bill_id] = 4
                    else:
                        billPoints[bill_id] = 2
                    
                    billPoints[bill_id] += sponsor_num[bill_id]
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, author_party, author_state, cosponsor_num, created_date, 
                                     last_action = last_action, url = url)
                    bills[bill_id] = created_bill

        #For every subject that interests the user, bills are pulled and ranked
        for subject in subjects:
            
            #Due to the structuring of the OpenStates API, multiple requests must be made to the OpenStates API to retrieve all necessary information
            
            state_params = {"state": state, "subject": subject, "search_window": "session", "apikey": os.environ['OPENSTATES_API_KEY']}

            state_params_version = {"state": state, "subject": subject, "search_window": "session", "fields": "versions", "apikey": os.environ['OPENSTATES_API_KEY']}
            state_params_sponsor = {"state": state, "subject": subject, "search_window": "session", "fields": "sponsors", "apikey": os.environ['OPENSTATES_API_KEY']}

            state_bill_response = requests.get(state_base+"bills/", state_params)
            state_bill_data = json.loads(state_bill_response.text)

            state_bill_version_response = requests.get(state_base+"bills/", state_params_version)
            state_bill_version = json.loads(state_bill_version_response.text)

            state_bill_sponsor_response = requests.get(state_base+"bills/", state_params_sponsor)
            state_bill_sponsor_data = json.loads(state_bill_sponsor_response.text)

            bill_urls = {}
            sponsor_names = {}
            sponsor_ids = {}
            sponsor_num = {}

            for version in state_bill_version:
                id = version['id']
                if len(version['versions']) > 0:
                    bill_urls[id] = version['versions'][0]['url']

            for sponsor in state_bill_sponsor_data:
                if len(sponsor['sponsors']) < 1:
                    continue
                id = sponsor['id']
                sponsor_names[id] = sponsor['sponsors'][0]['name']
                sponsor_ids[id] = sponsor['sponsors'][0]['leg_id']
                sponsor_num[id] = len(sponsor['sponsors'])

            for bill in state_bill_data:
                level = "state"
                bill_id = bill['id']

                if bill_id not in bill_urls or bill_id not in sponsor_names:
                    continue

                title = None
                description = bill['title']
                id = bill['bill_id']
                author_id = sponsor_ids[bill_id]
                url = bill_urls[bill_id]
                author = sponsor_names[bill_id]
                author_state = bill['state']
                author_party = None
                created_date = bill['created_at']
                last_action = bill['updated_at']
                cosponsor_num = sponsor_num[bill_id]

                if bill_id in billPoints:
                    if author_id in leg_ids:
                        billPoints[bill_id] += 4
                    billPoints[bill_id] += 5
                else:
                    billPoints[bill_id] = 5
                    billPoints[bill_id] += sponsor_num[bill_id]
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, author_party, author_state, cosponsor_num, created_date, 
                                        last_action = last_action, url = url)
                    bills[bill_id] = created_bill
                         
                    
        count = 0

        for bill_id in billPoints:
            bill_heap.append((billPoints[bill_id] * -1, count, bills[bill_id]))
            count = count + 1

        #All bills are put into array and then heapified
        heapify(bill_heap)

        #10 highest ranked bills are returned
        i = 0
        while i < 10:
            popped = heappop(bill_heap)
            sorted_bills.append(popped[2])
            i = i + 1

        print('success')
        return sorted_bills

    

    
