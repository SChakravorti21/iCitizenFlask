from iCitizenFlaskApp.models.legislator import Legislator
import requests, json
from heapq import heappush, heappop, heapify

class Bill(object):
    def __init__(self, level, title, description, author, author_id, bill_id, id, govtrack_link=None, url=None):
        self.level = level
        self.title = title
        self.description = description
        self.author = author,
        self.author_id = author_id
        self.bill_id = bill_id
        self.id = id
        self.govtrack_link = govtrack_link
        self.url = url

    def printBill(self):
        print(str(self.level) + "\n")
        print(str(self.title) + "\n")
        print(str(self.description) + "\n")
        print(str(self.author) + "\n")

    def json(self):
        return {
            "level": self.level,
            "title": sef.title,
            "description": self.description,
            "author": self.author,
            "author_id": self.author_id,
            "bill_id": self.bill_id,
            "id": self.id,
            "govtrack_link": self.govtrack_link,
            "url": self.url
        }

    @classmethod
    def get_national_bills(cls, legislators, subjects):

        bills = {}
        billPoints = {}

        bill_heap = []
        sorted_bills = []

        leg_ids = []

        national_base = "https://api.propublica.org/congress/v1/"
        national_params = {"X-API-Key": "Fl38VvBXk8EFlAmEcG4N0Wq1hi6YPnyzi5YODT9k", "congress": "115"}

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
                govtrack_link = bill['govtrack_url']

                if bill_id in billPoints:
                    if author_id == legislator.id:
                        billPoints[bill_id] += 9
                    else:
                        billPoints[bill_id] += 4
                else:
                    if author_id == legislator.id:
                        billPoints[bill_id] = 9
                    else:
                        billPoints[bill_id] = 4
                    billPoints[bill_id] += (bill['cosponsors'] / 5)
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, govtrack_link = govtrack_link)
                    bills[bill_id] = created_bill



        for subject in subjects:
            sub_bill_response = requests.get(national_base+"bills/subjects/{}.json".format(subject), headers=national_params)

            sub_bill_data = json.loads(sub_bill_response.text)['results']

            for bill in sub_bill_data:
                level = "national"
                title = bill['short_title']
                description = bill['title']
                author = bill['sponsor_name']
                author_id = bill['sponsor_id']
                bill_id = bill['bill_id']
                id = bill_id
                govtrack_link = bill['govtrack_url']

                if bill_id in billPoints:
                    if author_id in leg_ids:
                        billPoints[bill_id] += 9
                    billPoints[bill_id] += 4
                else:
                    billPoints[bill_id] = 4
                    billPoints[bill_id] += bill['cosponsors'] / 5
                    created_bill = cls(level, title, description, author, author_id, bill_id, govtrack_link = govtrack_link)
                    bills[bill_id] = created_bill

        count = 0

        for bill_id in billPoints:
            bill_heap.append((billPoints[bill_id] * -1, count, bills[bill_id]))
            count = count + 1

        heapify(bill_heap)

        for bill in bill_heap:
            popped = heappop(bill_heap)
            sorted_bills.append(popped[2])

        return sorted_bills

    @classmethod
    def get_state_bills(cls, legislators, subjects, state):
        state_base = "https://openstates.org/api/v1/"

        bills = {}
        billPoints = {}

        bill_heap = []
        sorted_bills = []

        leg_ids = []

        for legislator in legislators:
            leg_ids.append(legislator.id)

            state_params = {"state": state, "sponsor_id": legislator.id, "search_window": "session", "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}
            state_params_version = {"state": state, "sponsor_id": legislator.id, "search_window": "session", "fields": "versions", "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}
            state_params_sponsor = {"state": state, "sponsor_id": legislator.id, "search_window": "session", "fields": "sponsors", "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}

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
                bill_urls[id] = version['versions'][0]['url']

            for sponsor in state_bill_sponsor_data:
                id = sponsor['id']
                sponsor_names[id] = sponsor['sponsors'][0]['name']
                sponsor_ids[id] = sponsor['sponsors'][0]['leg_id']
                sponsor_num[id] = len(sponsor['sponsors'])
    
            for bill in state_bill_data:
                bill_id = bill['id']

                if bill_id not in sponsor_names or bill_id not in bill_urls:
                    continue

                level = "national"
                title = bill['title']
                description = None
                id = bill['bill_id']
                author_id = sponsor_ids[bill_id]
                url = bill_urls[bill_id]
                author = sponsor_names[bill_id]

                if bill_id in billPoints:
                    if author_id == legislator.id:
                        billPoints[bill_id] += 9
                    else:
                        billPoints[bill_id] += 4
                else:
                    if author_id == legislator.id:
                        billPoints[bill_id] = 9
                    else:
                        billPoints[bill_id] = 4
                    
                    billPoints[bill_id] += (sponsor_num[bill_id] / 5)
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, url = url)
                    bills[bill_id] = created_bill

        for subject in subjects:
            
            state_params = {"state": state, "subject": subject, "search_window": "session", "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}

            state_params_version = {"state": state, "subject": subject, "search_window": "session", "fields": "versions", "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}
            state_params_sponsor = {"state": state, "subject": subject, "search_window": "session", "fields": "sponsors", "apikey": "70e23970-e0b4-409b-a7d2-3e34f6b88905"}

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
                bill_urls[id] = version['versions'][0]['url']

            for sponsor in state_bill_sponsor_data:
                id = sponsor['id']
                sponsor_names[id] = sponsor['sponsors'][0]['name']
                sponsor_ids[id] = sponsor['sponsors'][0]['leg_id']
                sponsor_num[id] = len(sponsor['sponsors'])

            for bill in state_bill_data:
                level = "national"
                bill_id = bill['id']

                if bill_id not in bill_urls or bill_id not in sponsor_names:
                    continue

                title = bill['title']
                description = None
                id = bill['bill_id']
                author_id = sponsor_ids[bill_id]
                url = bill_urls[bill_id]
                author = sponsor_names[bill_id]

                if bill_id in billPoints:
                    if author_id in leg_ids:
                        billPoints[bill_id] += 9
                    billPoints[bill_id] += 4
                else:
                    billPoints[bill_id] = 4
                    billPoints[bill_id] += sponsor_num[bill_id] / 5
                    created_bill = cls(level, title, description, author, author_id, bill_id, id, url = url)
                    bills[bill_id] = created_bill
                         
                    
        count = 0

        for bill_id in billPoints:
            bill_heap.append((billPoints[bill_id] * -1, count, bills[bill_id]))
            count = count + 1

        heapify(bill_heap)

        for bill in bill_heap:
            popped = heappop(bill_heap)
            sorted_bills.append(popped[2])
            print(popped[2].id + ": " + str(popped[0]))

        return sorted_bills        





    

    