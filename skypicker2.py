import base64
import json
import time
import urllib2
from datetime import datetime, timedelta

import pymongo


def encodeBase64(stringToEncode):
	retorno = base64.b64encode(stringToEncode)
	return retorno

conn = pymongo.MongoClient('localhost', 27017)
db = conn['skypicker']
skypicker = db['results']

origins = [u'ORD', u'JFK']

dayCount = 25
length = 7

while dayCount < 27:

	for origin in origins:

		if origin == 'ORD':

			destinations = ['AAQ', 'AER', 'AMS']

		elif origin == 'JFK':

			destinations = ['AAQ', 'AER', 'AMS']

		for dist in destinations:

			dd = datetime.now() + timedelta(dayCount)
			departured = dd.strftime("%d/%m/%Y")
			returned = dd + timedelta(length)
			rd = datetime.now() + timedelta(dayCount + 7)
			returnd = rd.strftime("%d/%m/%Y")

			print departured
			print  returnd
			url = "https://api.skypicker.com/flights?flyFrom=" + origin + "&to=" + dist + "&curr=USD&dateFrom=" + departured + "&dateTo=" + returnd
			print url
			try:

				req = urllib2.Request(url)

				response = urllib2.urlopen(req)

				data = json.load(response)

				date_string = time.strftime("%Y-%m-%d")

				filename = 'DataForThreeMonths/From= ' + origin + ' To= ' + dist + " Departure= " + departured + ' Collected= ' + date_string + '.json'

				# with open(filename,'w') as outfile:
				#    json.dump(data, outfile)
				skypicker.insert_one(data)
			except urllib2.HTTPError, err:
				print(err)
				pass

			time.sleep(0)

	dayCount += 1
