from chalice import Chalice
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

app = Chalice(app_name='EskomLoadShedding')


#HELPER Functions - called in actual API routes

#get current stage
def get_stage():
    print("Getting Current Load Shedding Stage")
    # GetStage Endpoint
    URL = "http://loadshedding.eskom.co.za/LoadShedding/GetStatus"
    r = requests.get(url = URL)
    data = r.json()
    stage = data -1
    return stage

#scrape the schedule based on area and stage
#example ESKOM CALL:
# first number is suburb ID
# second is stage (only 1-4 at this time)
# 3rd appears to relate to province but appears to have no effect but fails if empty
# 4th also appears to have no known reason or effect but fails if empty
# http://loadshedding.eskom.co.za/LoadShedding/GetScheduleM/1020663/2/3/8
def get_schedule(area_id,stage):
    uri = "http://loadshedding.eskom.co.za/LoadShedding/GetScheduleM/" + area_id + "/" + stage + "/3/8"
    data_raw = requests.get(uri)
    soup = BeautifulSoup(data_raw.text, 'html.parser')
    days = soup.find_all(class_='scheduleDay')
    # we need current date for to exclude schedules in the past
    now = datetime.now()

    data_dict = {}

    for day in days:
        day_obj = day.find_all('div')
        #Wed, 11 Mar
        date_str = str(now.year) + " " + day_obj[0].text.strip()
        date = datetime.strptime(date_str, '%Y %a, %d %b')
        #print("date: ", date)
        #print("items-----")
        # ITEM 0 is date
        # ITEM 1... is windows
        shedding_list = day.find_all('div')

        #SKIP first item in each list - its the date we grabbed it above - here is purely iterating over the actual load shedding windows
        shedding_iterator = iter(shedding_list)
        next(shedding_iterator)

        # day list
        day_dict = {}
        count = 1
        for item in shedding_iterator:

            #build a list of starts and stops
            # item 0 and 2 is start and end
            # TODO convert the strings to times
            shedding_window =  item.text.strip().split()
            day_dict[count] = {'start': shedding_window[0], 'end': shedding_window[2]}
            #print(item.text.strip().split())
            count += 1
        #print(day_dict)
        data_dict[date_str] = day_dict
    #print(data_dict)
    #return json.dumps(data_dict)
    return data_dict

        #print(soup.prettify())
        # add the list to data_dict with date as key
    #output data_dict as json


@app.route('/')
def index():
    return {'hello': 'world'}

# Gets the Current Eskom Load Shedding Stage from Eskom API and presents it as an Int
# 0 - no Load shedding, 1-8 Stage 1-8
@app.route('/Stage')
def current_stage():
    stage = get_stage()
    return stage

#get full available schedule for an area and stage
@app.route('/Schedule/{area_id}/{stage}')
def get_full_schedule(area_id,stage):
    return get_schedule(area_id,stage)

#Gets the Next Shedding window for a given Area ID and Load Shedding Stage

@app.route('/NextShedding/{area_id}/{stage}')
def next_shedding_stage(area_id,stage):
    return get_schedule(area_id,stage)

#Gets next shedding when stage is not supplied (dynamically go and get current stage)
@app.route('/NextShedding/{area_id}')
def next_shedding(area_id):
    return { 'area': area_id, 'stage': get_stage()}