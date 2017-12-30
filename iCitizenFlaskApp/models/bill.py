from iCitizenFlaskApp.models.legislator import Legislator
import requests, json
from heapq import heappush, heappop, heapify

class Bill(object):
    def __init__(self, level, title, description, author, author_id, bill_id, govtrack_link, subjects=None, cosponsors=None):
        self.level = level
        self.title = title
        self.description = description
        self.author = author,
        self.author_id = author_id
        self.bill_id = bill_id
        self.govtrack_link = govtrack_link
        self.subjects = subjects
        self.cosponsors = cosponsors

    def printBill(self):
        print(str(self.level) + "\n")
        print(str(self.title) + "\n")
        print(str(self.description) + "\n")
        print(str(self.author) + "\n")
        if subjects is not None:
            print(str(subjects))
        if cosponsors is not None:
            print(str(self.level) + "\n")

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
                bill_id = bill['bill_id']
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
                    created_bill = cls(level, title, description, author, author_id, bill_id, govtrack_link)
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
                govtrack_link = bill['govtrack_url']

                if bill_id in billPoints:
                    if author_id in leg_ids:
                        billPoints[bill_id] += 9
                    billPoints[bill_id] += 4
                else:
                    billPoints[bill_id] = 4
                    billPoints[bill_id] += bill['cosponsors']
                    created_bill = cls(level, title, description, author, author_id, bill_id, govtrack_link)
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
    def get_state_bills(cls, legislators, subjects):
        
                         
                    
                
                









    

    