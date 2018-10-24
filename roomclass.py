import json

class Room:
	def __init__(self):
		self.location = "testing"
		self.long_description = ""
		self.short_description = ""
		self.look_at =""
		self.exits = ""
	# basically a constructor/ initializer
	def populate(self, location, long_description, short_description, look_at, exits):
		self.location = location
		self.long_description = long_description
		self.short_description = short_description
		self.lookat = look_at
		self.exits = exits


