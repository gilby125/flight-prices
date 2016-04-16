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

