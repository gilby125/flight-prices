import requests
from datetime import datetime


class SkyPickerApi(object):
    """docstring for SkyPickerApi"""
    def __init__(self):
        self.base = 'https://api.skypicker.com/'
        self.path = 'flights?flyFrom=FOR&to=LIS&curr=BRL&'
        self.date = ''
        self.time = ''


    @property
    def url(self):
        return '{}{}{}'.format(self.base, self.path, self.date)


    def fetch_data(self):
        today = datetime.now()
        self.time = today.strftime('%H:%M')
        self.date = today.strftime('%m/%d/%Y')

        headers = {'content-type': 'application/json'}
        resp = requests.get(self.url, headers=headers)
        return resp.json()


