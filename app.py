from chalice import Chalice
import requests
from bs4 import BeautifulSoup

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
    print(days[0])
    for item in days[0].find_all('div'):
        print(item.text)
    #print(soup.prettify())


@app.route('/')
def index():
    return {'hello': 'world'}

# Gets the Current Eskom Load Shedding Stage from Eskom API and presents it as an Int
# 0 - no Load shedding, 1-8 Stage 1-8
@app.route('/Stage')
def current_stage():
    stage = get_stage()
    return stage


#Gets the Next Shedding window for a given Area ID and Load Shedding Stage

@app.route('/NextShedding/{area_id}/{stage}')
def next_shedding_stage(area_id,stage):
    return get_schedule(area_id,stage)

#Gets next shedding when stage is not supplied (dynamically go and get current stage)
@app.route('/NextShedding/{area_id}')
def next_shedding(area_id):
    return { 'area': area_id, 'stage': get_stage()}