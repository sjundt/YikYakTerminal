#! /usr/bin/env python3
import API as pk
import pygeocoder
import requests
import datetime

from time import strftime, gmtime, sleep
from datetime import datetime, timedelta

class YikYakApi:
	def __init__(self, location_str="Claremont Colleges", user=None):
		# Initialize Google Geocoder API
		geocoder = pygeocoder.Geocoder("AIzaSyAGeW6l17ATMZiNTRExwvfa2iuPA1DvJqM")
		self.coordlocation = self.setLocation(geocoder, location_str)
		if (self.coordlocation==None):
			raise "BAD LOCATION"
		self.remoteyakker = pk.Yakker(user, self.coordlocation, True)
		currentlist = []

	def get_current_yaks(self):
		currentlist = self.remoteyakker.get_yaks()
		return(self.read(currentlist))
	
	def setUserID(self, location, userID=None):
		self.remoteyakker = pk.Yakker(userID, location, False)
		return self.remoteyakker
	
	def setLocation(self, geocoder, address=""):
		# newLoc = newLocation(geocoder, address)
		new_loc_lat_long = geocoder.geocode(address)
		new_loc = pk.Location(new_loc_lat_long.latitude, new_loc_lat_long.longitude)

		# If location retrieval succeeds, set it
		if new_loc != 0:
			self.coordlocation = new_loc
			
		return self.coordlocation
	
	def read(self, yaklist):
		yakNum = 1
		result = []
		for yak in yaklist:
			# yak number
			thisYak = {}
			thisYak["num"] = str(yakNum) + "\n"
			thisYak["time"] = yak.time
			thisYak["likes"] = yak.likes
			thisYak["latitude"] = yak.latitude
			thisYak["longitude"] = yak.longitude
			thisYak["message"] = yak.message
						
			# commentNum = 1
			# # comments header
			# comments = yak.get_comments()
			# commentList = []
			# for comment in comments:
			# 	commentList.append(comment.asDict())
			# 	commentNum += 1
			# thisYak[comments] = commentList
			result.append(thisYak)
			yakNum += 1
		return result
		
yak = YikYakApi()
print(yak.get_current_yaks())