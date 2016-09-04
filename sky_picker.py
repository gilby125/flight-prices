import requests
from datetime import datetime

class SkyPickerApi(object):
    """docstring for SkyPickerApi"""
    def __init__(self):
        self.base = 'https://api.skypicker.com/'
        self.path = 'flights?flyFrom=FOR&to=LIS&curr=BRL&dateFrom='
        self.date = ''
        self.time = ''
        self.travel_date = '10/07/2016'


    @property
    def url(self):
        return '{}{}{}'.format(self.base, self.path, self.travel_date)


    def fetch_data(self):
        today = datetime.now()
        self.time = today.strftime('%H:%M')
        self.date = today.strftime('%m/%d/%Y')

        headers = {'content-type': 'application/json'}
        resp = requests.get(self.url, headers=headers)
        return resp.json()


    def save_lowest_price(self):
        import csv

        request = self.fetch_data()
        date_time = '{} {}'.format(self.date, self.time)
        price_brl = request['data'][0]['conversion']['BRL']
        price_eur = request['data'][0]['conversion']['EUR']
        price_usd = request['data'][0]['conversion']['USD']
        writer = csv.writer(open('data.csv', 'a'), delimiter=',')
        writer.writerow([date_time, price_brl, price_eur])

        return True