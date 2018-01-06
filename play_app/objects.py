class Artist:
	def __init__(self, json, id):
		self.name = json['name']
		self.mbid = json['mbid']
		self.heading = "heading"+str(id)
		self.body = "body"+str(id)

	def toString():
		return "Name: " + str(name) + " ||| mbid: " + str(mbid)

class Setlist:
	def __init__(self, setlist):
		self.name = setlist['artist']['name']
		self.venue_name = setlist['venue']['name']
		self.venue_city = setlist['venue']['city']['name']
		self.venue_state = setlist['venue']['city']['state']
		self.date = setlist['eventDate']

		try:
			self.tour_name = setlist['tour']['name']
		except KeyError:
			self.tour_name = ""

		try:
			self.set_list = setlist['sets']['set'][0]['song'] #list of songs
		except IndexError:
			self.set_list = []

		try:
			self.encore_list = setlist['sets']['set'][1]['song'] #list of encore songs
		except IndexError:
			self.encore_list = []	
