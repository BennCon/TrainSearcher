from bs4 import BeautifulSoup
import requests

from dotenv import load_dotenv
import os
load_dotenv()
app_id = os.getenv('APP_ID')
app_key = os.getenv('APP_KEY')


def stationCode(name, type=None):
    """Returns a station code

    Keyword arguments:
    type -- set to 'list' to return a dictionary of top results
            set to 'info' for the top result and full name
    """

    url = "http://transportapi.com/v3/uk/places.json?query={0}&type=train_station&app_id={1}&app_key={2}".format(name, app_id, app_key)
    response = requests.get(url).json()

    if type == 'list':
        station_dict = {}
        for i in response['member']:
            station_dict[i['name']] = i['station_code']
        return station_dict
    elif type == "info":
        return response['member'][0]['station_code'] + ": " + response['member'][0]['name']
    else:
        return response['member'][0]['station_code']



def trainSearch(origin, destination, date, time, num):
    """Returns a list of journeys from one station to another

    Arguments:
    Origin & destination -- should be entered as station codes
    Station codes can be searched for with stationCode() function
    Num -- number of results to generated
    """

    #Sends request for journeys for matching journeys
    url = "https://transportapi.com/v3/uk/train/station/{0}/{1}/{2}/timetable.json?app_id={3}&app_key={4}&calling_at={5}&train_status=passenger".format(
        origin, date, time, app_id, app_key, destination)
    response = requests.get(url).json()

    #Objects for loop
    search_res = []
    train_info = {}
    trainURL = ""
    for i in response['departures']['all']:
        #Requests detailed information about the train
        trainURL = i['service_timetable']['id']
        train_res = requests.get(trainURL).json()

        #Gets time train arrives at destination
        for stop in train_res['stops']:
            if stop['station_code'] == destination:
                arrival_time = stop['aimed_arrival_time']

        train_info = {
            'Departure Time': i['aimed_departure_time'],
            'Arrival Time' : arrival_time,
            'Operator' : train_res['operator_name'],
        }

        search_res.append(train_info)
        if len(search_res) == num: break

    search_res = sorted(search_res, key=lambda k: k['Arrival Time']) 

    return search_res

def changeTrain(origin, destination, change_location, date, time, num):
    return_string = ""
    for i in trainSearch(stationCode(origin), stationCode(change_location), date, time, num):
        return_string += str(i) + " >>>>>>> " + str(trainSearch(stationCode(change_location), stationCode(destination), date, i['Arrival Time'], num)[0]) + "\n"

    return return_string

print(changeTrain("Sheffield", "chester", "Manchester Pic", "2021-08-14", "18:40", 5))


# for i in (trainSearch(stationCode("Sheffield"), stationCode("Manchester pic"), "2021-08-14", "18:40", 2)):
#     print(i)






