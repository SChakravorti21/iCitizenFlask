from iCitizenFlaskApp.models.legislator import Legislator
from heapq import heappush, heappop

class Bill(object):
    def __init__(self, level, title, description, author, authorId, billId, govtrack_link, subjects=None, cosponsors=None):
        self.level = level
        self.title = title
        self.description = description
        self.author = author,
        self.authorId = authorId
        self.billId = billId
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
    def get_national_bills(cls, legislators, subjects, party):

        national_base = "https://api.propublica.org/congress/v1/"
        national_params = {"X-API-Key": "Fl38VvBXk8EFlAmEcG4N0Wq1hi6YPnyzi5YODT9k", "congress": "115"}

        for legislator in legislators:
            rep_bill_response = requests.get(national_base+"members/{}/bills/updated.json".format(legislator.id), headers=national_params)
            rep_bill_data = json.loads(rep_bill_response.text)['results'][0]['bills']
            for bill in rep_bill_data:
                level = "national"
                title = bill['short_title']
                description = bill['title']
                author = bill['sponsor_name']
                authorId = bill['sponsor_id']
                billId = bill['bill_id']
                govtrack_link = bill['govtrack_url']

                



    

    