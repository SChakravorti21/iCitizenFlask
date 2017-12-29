class Bill(object):
    def __init__(self, level, title, description, author, subjects=None, cosponsors=None):
        self.level = level
        self.title = title
        self.description = description
        self.author = author
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

    

    