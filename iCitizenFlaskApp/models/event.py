class Event:

	def __init__(self, title, link, time, location, price):
		self.title = title
		self.link = link
		self.time = time
		self.location = location
		self.price = price

	def printInfo(self):
		print('title : ', self.title)
		print('link for more info : ', self.link)
		print('date of event : ', self.time)
		print('location of event: ', self.location)
		print('price : ', self.price)