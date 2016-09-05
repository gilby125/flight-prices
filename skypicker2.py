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

	# endpoint = "https://api.test.sabre.com/v1"
	# urlByService = "/auth/token?="
	# url = endpoint + urlByService
	# password = "v68npJKN"
	# encodedUserInfo =  encodeBase64("V1:11dhmnwb72pizl3t:DEVCENTER:EXT")
	# encodedPassword =  encodeBase64(password)
	# encodedSecurityInfo = encodeBase64(encodedUserInfo + ":" + encodedPassword)
	# data = {'grant_type':'client_credentials'}
	# headers = {'content-type': 'application/x-www-form-urlencoded ','Authorization': 'Basic ' + encodedSecurityInfo}
	# response = requests.post(url, headers=headers,data=data)
	# access_token = response.json()
	# token = 'Bearer ' + access_token[u'access_token']


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
			# url = "https://api.test.sabre.com/v1/shop/flights?origin=" + origin + "&destination=" + dist + "&departuredate=" + departured + "&returndate=" + returnd + "&onlineitinerariesonly=N&limit=300&offset=1&eticketsonly=N&sortby=totalfare&order=asc&sortby2=departuretime&order2=asc&pointofsalecountry=US"
			# url = "https://api.skypicker.com/flights?flyFrom=" + origin + "&to=" + dist + "&curr=USD&dateFrom=" + departured
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

			time.sleep(.15)

	dayCount += 1
