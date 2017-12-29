class Legislator(object):

    def __init__(self, level, firstName, lastName, state, chamber, id, party, streetAddress, city, stateAddress, zipcode, phone):
        self.level = level
        self.firstName = firstName
        self.lastName = lastName
        self.state = state
        self.chamber = chamber
        self.id = id
        self.party = party
        self.streetAddress = streetAddress
        self.city = city
        self.stateAddress = stateAddress
        self.zipcode = zipcode
        self.phone = phone

    def printLegislator(self):
        print(str(self.level) + "\n")
        print(str(self.firstName) + "\n")
        print(str(self.lastName) + "\n")
        print(str(self.state) + "\n")
        print(str(self.chamber) + "\n")
        print(str(self.id) + "\n")
        print(str(self.party) + "\n")
        print(str(self.streetAddress) + "\n")
        print(str(self.city) + "\n")
        print(str(self.stateAddress) + "\n")
        print(str(self.zipcode) + "\n")
        print(str(self.phone) + "\n")


