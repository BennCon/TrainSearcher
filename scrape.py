from bs4 import BeautifulSoup
import requests
from requests.models import Response
from dotenv import load_dotenv
import os
load_dotenv()


def stationCode(name, type=None):
    """Returns a station code

    Keyword arguments:
    type -- set to 'list' to return a dictionary of top results
    """

    url = "http://transportapi.com/v3/uk/places.json?query={0}&type=train_station&app_id={1}&app_key={2}".format(name, os.getenv('APP_ID'), os.getenv('APP_KEY'))
    response = requests.get(url).json()

    if type == 'list':
        station_dict = {}
        for i in response['member']:
            station_dict[i['name']] = i['station_code']

        return station_dict
    else:
        return response['member'][0]['station_code']



# https://transportapi.com/v3/uk/train/station/SHF/2021-08-12/18:35/timetable.json?app_id=53735c36&app_key=adad89f5ffc159918082376619aa056b&calling_at=MAN&train_status=passenger


print(stationCode("wrexham"))




