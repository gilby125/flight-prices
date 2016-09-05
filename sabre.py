import base64
import json
import time
import urllib2
from datetime import datetime, timedelta

import pymongo
import requests


def encodeBase64(stringToEncode):
	retorno = base64.b64encode(stringToEncode)
	return retorno


conn = pymongo.MongoClient('localhost', 27017)
db = conn['skypicker']
skypicker = db['results']

origins = [u'ORD', u'JFK']

dayCount = 25

while dayCount < 93:

	endpoint = "https://api.test.sabre.com/v1"
	urlByService = "/auth/token?="
	url = endpoint + urlByService
	password = "v68npJKN"
	encodedUserInfo = encodeBase64("V1:11dhmnwb72pizl3t:DEVCENTER:EXT")
	encodedPassword = encodeBase64(password)
	encodedSecurityInfo = encodeBase64(encodedUserInfo + ":" + encodedPassword)
	data = {'grant_type': 'client_credentials'}
	headers = {'content-type': 'application/x-www-form-urlencoded ', 'Authorization': 'Basic ' + encodedSecurityInfo}
	response = requests.post(url, headers=headers, data=data)
	access_token = response.json()
	token = 'Bearer ' + access_token[u'access_token']

	for origin in origins:

		if origin == 'JFK':
			destinations = ['LAX', 'MIA', ]
			# destinations = ['LAX', 'MIA', 'AMS', 'MAD', 'BCN', 'BER', 'FRA', 'DXB', 'PAR', 'BRU', 'HKG', 'SIN', 'IST', 'STT', 'TXL', 'LED', 'LON', 'MAD', 'MIL', 'MRV', 'MUC', 'NYC', 'ODS', 'OVB', 'PAR', 'PRG', 'PUJ', 'ROM', 'ROV', 'SIP', 'SVX', 'TAS', 'TBS', 'TCI', 'TIV', 'TLV', 'VIE']

		# elif origin == 'MOW':
		elif origin == 'ORD':
			destinations = ['LAX', 'MIA', ]
			# destinations = ['LAX', 'DFW', 'AMS', 'MAD', 'BCN', 'BER', 'FRA', 'DXB', 'PAR', 'BRU', 'HKG', 'SIN', 'IST', 'STT', 'TXL', 'LED', 'LON', 'MAD', 'MIL', 'MRV', 'MUC', 'NYC', 'ODS', 'OVB', 'PAR', 'PRG', 'PUJ', 'ROM', 'ROV', 'SIP', 'SVX', 'TAS', 'TBS', 'TCI', 'TIV', 'TLV', 'VIE']

		for dist in destinations:
			dd = datetime.now() + timedelta(dayCount)
			# .strftime("%Y-%m-%d %H:%M")
			departured = dd.strftime("%d/%m/%Y")
			departdte = str(dd)[:10]  # str(dd)#[:10]
			rd = datetime.now() + timedelta(dayCount + 7)
			returnd = str(rd)[:10]
		print departured
		url = "https://api.skypicker.com/flights?flyFrom=" + origin + "&to=" + dist + "&curr=USD&dateFrom=" + departured
		# url = "https://api.test.sabre.com/v1/shop/flights?origin=" + origin + "&destination=" + dist + "&departuredate=" + departured + "&returndate=" + returnd + "&onlineitinerariesonly=N&limit=300&offset=1&eticketsonly=N&sortby=totalfare&order=asc&sortby2=departuretime&order2=asc&pointofsalecountry=US"


		print url
		try:

			req = urllib2.Request(url, headers={'Authorization': token})

			response = urllib2.urlopen(req)

			data = json.load(response)

			date_string = time.strftime("%Y-%m-%d")

			filename = 'DataForThreeMonths\From= ' + origin + ' To= ' + dist + " Departure= " + departdte + ' Collected= ' + date_string + '.json'

			with open(filename, 'w') as outfile:
				json.dump(data, outfile)

		except urllib2.HTTPError, err:
			print(err)
			pass
		skypicker.insert_one(data)

	dayCount += 1
