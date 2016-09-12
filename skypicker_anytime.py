import base64
import json
import urllib2
from datetime import datetime, timedelta

from sqlalchemy import create_engine, MetaData

# from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.sql.expression import Insert
# import requests




# @compiles(Insert)
# def prefix_inserts(insert, compiler, **kw):
#   return compiler.visit_insert(insert, **kw) + "ON CONFLICT DO NOTHING"



conn_str = 'postgresql://gilby:Lokifish123@192.168.32.133:5432/api_results_dev'

engine = create_engine(conn_str, client_encoding='utf8')

# meta = MetaData()
# meta2 = MetaData()
# meta.reflect(engine, only=['fares','routes'])

meta = MetaData()
meta.reflect(bind=engine)
# users_table = meta.tables['fares']
addresses_table = meta.tables['routes']


# cur.execute("""SELECT datname from pg_database""")
def encodeBase64(stringToEncode):
	retorno = base64.b64encode(stringToEncode)
	return retorno


origins = [u'ORD', u'PDX', u'IAH', u'MSP', u'DEN', u'PHX', u'LAX', u'SFO', u'SEA', u'ATL', u'DTW', u'CVG', u'NYC',
           u'WAS', u'CLT', u'ATL', u'MIA', u'FLL', u'YYZ', u'YTO', u'YVR', u'MSP', u'FLL', u'MSP', u'BOS']

dayCount = 10
length = 7
stops = 3
i = datetime.now()
limit_int = 10

while dayCount < 27:

	for origin in origins:

		if origin == 'ORD':

			destinations = [u'-', 'DPS', 'GUM', 'BKK', 'HKG', 'SYD', 'AKL', 'MEB', 'CHC', 'PPT', 'RAR', 'GUM', 'TYO',
			                'PEK', 'HNL', 'LIH', 'OGG', 'KOA', 'MEX', 'GIG', 'CMB', 'FRA', 'BRU', 'LHR', 'PAR', 'MAD',
			                'BCN', 'AMS', 'TXL', 'MXP', 'FCO', 'GVA']

		else:

			destinations = [u'-', 'CGK', 'BKK', 'HKG', 'SYD', 'AKL', 'MEB', 'CHC', 'PPT', 'RAR', 'GUM', 'TYO', 'PEK',
			                'HNL', 'LIH', 'OGG', 'KOA', 'MEX', 'GIG', 'CMB', 'FRA', 'BRU', 'LHR', 'PAR', 'MAD', 'BCN',
			                'AMS', 'TXL', 'MXP', 'FCO', 'GUM']

		for dist in destinations:

			dd = datetime.now() + timedelta(dayCount)
			departured = dd.strftime("%d/%m/%Y")

			returned = dd + timedelta(length)
			rd = datetime.now() + timedelta(dayCount + 7)
			returnd = rd.strftime("%d/%m/%Y")

			print departured
			print returnd

			url_skypicker = "https://api.skypicker.com/flights?flyFrom=" + origin + "&flyto=" + dist + "&curr=USD&dateFrom=" + \
			                departured + "&daysInDestinationTo=" + str(length) + "&stopNumber=" + \
			                str(stops) + "&price_to=575" + "&radiusFrom=200" + "&radiusTo=200" + \
			                "&sortBy=price" + "&partner=picky" + "&limit=" + str(limit_int)

			print url_skypicker

			try:
				req_skypicker = urllib2.Request(url_skypicker)
				# req_sabre = urllib2.Request(url_sabre, headers={'Authorization': token})
				response_skypicker = urllib2.urlopen(req_skypicker)
				# response_sabre = urllib2.urlopen(req_sabre)

				data_skypicker = json.load(response_skypicker)
				data_skypicker_2 = data_skypicker['data']
				data_skypicker_3 = data_skypicker_2[0]['route']
				# data_sabre = json.load(response_sabre)
				# date_string = time.strftime("%Y-%m-%d")


				# filename = 'DataForThreeMonths/From= ' + origin + ' To= ' + dist + '.json'
				# with open(filename, 'w') as outfile:
				# json.dump(data_sabre, outfile)

				for row in data_skypicker_3: engine.execute(meta.tables['routes'].insert().values(
					route_atimeutc=row['aTimeUTC'], route_mapidfrom=row['mapIdfrom'], route_mapidto=row['mapIdto'],
					route_id=row['id'],
					route_flightno=row['flight_no'], route_dtime=row['dTime'], route_latto=row['latTo'],
					route_flyfrom=row['flyFrom'],
					route_airline=row['airline'], route_lngto=row['lngTo'], route_cityto=row['cityTo'],
					route_cityfrom=row['cityFrom'],
					route_lngfrom=row['lngFrom'], route_atime=row['aTime'], route_price=row['price'],
					route_flyto=row['flyTo'],
					route_latfrom=row['latFrom'], route_dtimeutc=row['dTimeUTC']), route_return=row['return'],
					route_source=row['source'],
					created_at=i, updated_at=i)

				for row1 in data_skypicker_2: engine.execute(
					meta.tables['fares'].insert().values(created_at=i, updated_at=i,
					                                     booking_token=row1['booking_token'], _id_=row1['id'],
					                                     deep_link=row1['deep_link'], flyto=str(row["flyTo"]),
					                                     countryto=row1['countryTo']), distance=row1['distance'],
					flyFrom=str(row1['flyFrom']),
					route=row1['route'], _id_=row1['booking_token'], deep_link=row1['deep_link'],
					mapIdfrom=row1['mapIdfrom'],
					cityTo=str(row1['cityTo']), flyTo=str(row1['flyTo']), price=row1['price'], data=row1)


			except urllib2.HTTPError, err:

				print(err)

				pass

			# time.sleep(0.3)

	dayCount += 1
