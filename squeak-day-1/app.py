import API as pk
import pygeocoder
import requests
import datetime

from time import strftime, gmtime, sleep
from datetime import datetime, timedelta
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

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
		current_yaks = self.read(currentlist)
		sorted_yaks = sorted(current_yaks, key=lambda k: k['likes'])
		sorted_yaks.reverse()
		return(sorted_yaks)
	
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

app = Flask(__name__, static_path='/static')
app.debug = True

API = YikYakApi()
YAKS = 0

@app.route('/')
def index():
	API = YikYakApi()
	YAKS = API.get_current_yaks()
	return render_template('index.html', yaks=YAKS)

@app.route('/results', methods=['POST'])
def results():
	if (YAKS ==0):
		YAKS = API.get_current_yaks()
	return render_template('static/results.html',
		yaks = YAKS)


# @app.route('/todos/', methods=['POST'])
# def todo_create():
#     todo = request.get_json()
#     db.session.add(Item(todo))
#     db.session.commit()
#     return "Good"


# @app.route('/todos/<int:id>')
# def todo_read(id):
#     todo = db.session.query(Item).filter(Item.id==id).first()
#     if todo==None:
#         abort(404) #send error message
#     return jsonify(todo.serialize())


# @app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
# def todo_update(id):
#     new_item = request.get_json()
#     print request.get_json
#     print new_item[u'title']
#     db.session.query(Item).filter(Item.id==id).update({Item.title:new_item[u'title']})
#     print "NEW IN DB:", db.session.query(Item).filter(Item.id==id).all()
#     db.session.commit()
#     return "Fine"


# @app.route('/todos/<int:id>', methods=['DELETE'])
# def todo_delete(id):
#     db.session.query(Item).filter(Item.id==id).delete()
#     db.session.commit()
#     return "Fine"

if __name__ == '__main__':
    app.run(port=8000)
