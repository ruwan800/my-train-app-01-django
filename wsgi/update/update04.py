from schedule.models import Schedule
from station.models import getStationsInBetween, getStation
from advanced.pickle import writePickle, readPickle
from process.models import setProgressBoundary, getCurrentProgress, breakNow
from update.models import UPDATE_STRING
from urllib.request import urlopen, Request
from train.models import getTrainByNumber
from datetime import datetime
import threading
import json



def departureNoneHackPrepare():
    """
    This function has been created to fix *departure* value being **None** 
    in some values in :class:`.Schedule`. This issue was occurred due to 
    a problem of the selecting method of starting-finishing points for 
    download schedule information in :func:`.generateCriteriaFile`. However
    this function creates yet another criteria in **departure_hack_retrive_list**
    pickle. based on :class:`.Schedule` values which has departure values
    set to **None**.
    """ 
    print("process started.")
    scheduleSet = Schedule.objects.filter(departure=None)
    orderedSchedules = {}
    
    for schedule in scheduleSet:
        if schedule.station != schedule.train.end:
            if schedule.station.name in orderedSchedules:
                orderedSchedules[schedule.station.name].append(schedule)
            else:
                orderedSchedules[schedule.station.name] = [schedule]
    last_exec = getCurrentProgress(UPDATE_STRING)
    if not last_exec:
        writePickle("gen", "departure_hack_retrive_list", [])
    setProgressBoundary(UPDATE_STRING,len(orderedSchedules))
    for keyI in range(last_exec,len(orderedSchedules)):
        if breakNow(UPDATE_STRING):
            break
        key = list(orderedSchedules.keys())[keyI]
        print("DHP:: {} {}".format(keyI,key))####
        
        querySet = []
        scheduleSet2 = orderedSchedules[key]
        stopsSet = []
        for sch in scheduleSet2:
            start = sch.station
            finish = sch.train.end
            allStations = getStationsInBetween(start,finish)[1:]
            allStops = [x.station for x in Schedule.objects.filter(train=sch.train)]
            stops = set(allStations).intersection(allStops)
            stopsSet.append(stops)
        selectedSet = []
        count = 0
        while(count != len(stopsSet)):
            count = 0
            distinctCount = {}
            for i in stopsSet:
                if set(selectedSet).intersection(i):
                    count += 1
                else:
                    for j in i:
                        if j in distinctCount:
                            distinctCount[j] += 1
                        else:
                            distinctCount[j] = 1
            if count == len(stopsSet):
                break
            max = 0
            maxValue = None
            for key2 in distinctCount.keys():
                if max < distinctCount[key2]:
                    max = distinctCount[key2]
                    maxValue = key2
            selectedSet.append(maxValue)
            querySet.append([start.number, maxValue.number])
        data = readPickle("gen","departure_hack_retrive_list")
        writePickle("gen", "departure_hack_retrive_list", data+querySet)
        

def readpage(info):
    """
    Each occurrence of this function is called in a separate thread since it 
    downloads schedule information and it takes time.
    """
    print("DLH:: {} - {} ".format(info[0], info[1]))####
    Zurl = "http://m.icta.lk/services/railwayservicev2/train/searchTrain?startStationID={}&endStationID={}&searchDate=2014-01-21&startTime=00:00:00&endTime=23:59:59&lang=en"
    #http://m.icta.lk/services/railwayservicev2/train/searchTrain?startStationID=184&endStationID=61&searchDate=2014-01-21&startTime=00:00:00&endTime=23:59:59&lang=en
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    mod_url = Zurl.format(info[0], info[1])
    Zreqest = Request(mod_url,headers=hdr)
    try:
        response = urlopen(Zreqest).read()
    except:
        response = urlopen(Zreqest).read()
    if breakNow(UPDATE_STRING):
        return
    content = readPickle("gen","departure_hack_downloaded_data")
    if not content:
        content = {}
    text = "{}_{}".format(info[0],info[1])
    content[text] = response
    writePickle("gen","departure_hack_downloaded_data",content)

def retrieveSchedulePages():
    """
    This method creates a pool of threads to retrieve schedule information
    from web-service using **departure_hack_retrive_list** pickle. All 
    information received in each result will be save in 
    **departure_hack_downloaded_data** pickle as dictionary value under a 
    key generated with "*<start>_<end>*" format.
    """
    thread_list = []
    parralle_downloads = 10
    data = readPickle("gen","departure_hack_retrive_list")
    setProgressBoundary(UPDATE_STRING,len(data))
    for i in range(getCurrentProgress(UPDATE_STRING),len(data)):
        info = data[i]
        #page download threads
        t = threading.Thread(target=readpage, args=(info,))
        thread_list.append(t)
    
    for i in range(0,len(thread_list),parralle_downloads):
        for j in range(i,i+parralle_downloads):
            if j+1 < len(data):
                thread_list[j].start()
    
        for j in range(i,i+parralle_downloads):
            if j+1 < len(data):
                thread_list[j].join()


def scheduleDataFormat2():
    """
    This function update empty departure values in :class:`.Schedule` with 
    new values using **departure_hack_downloaded_data** pickle. 
    """
    data = readPickle("gen","departure_hack_downloaded_data")
    keyset = list(data.keys())
    setProgressBoundary(UPDATE_STRING,len(keyset))
    for i in range(getCurrentProgress(UPDATE_STRING),len(keyset)):
        if breakNow(UPDATE_STRING):
            break
        key = keyset[i]
        print("SDF2 :: "+key)####
        keyinfo = key.split("_")
        c1 = data[key]
        c2 = json.loads(c1.decode('utf-8'))
        if c2['SUCCESS']:
            content = c2["RESULTS"]["directTrains"]['trainsList']
            for sch in content:
                train = getTrainByNumber(sch['trainNo'])
                station = getStation(sch['startStationName'])
                try:
                    Q1 = Schedule.objects.get(train=train, station=station)
                    if not Q1.departure:
                        Q1.departure = datetime.strptime(sch['depatureTime'],"%H:%M:%S").time()
                        Q1.save()
                except:
                    pass
            
