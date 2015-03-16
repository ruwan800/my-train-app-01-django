from advanced.pickle import readPickle, writePickle
from process.models import setProgressBoundary, getCurrentProgress, breakNow
from update.models import UPDATE_STRING, addConflict, addInsert, addUpdate
from train.models import getTrainType, Train, PrimaryTrain, getTrainByNumber
from station.models import getStation, getStationsInBetween
from schedule.models import Schedule, PrimarySchedule
from datetime import datetime, date
import json

def scheduleDataFormat():
    """
    Formats data in **schedule_downloads** pickle and save in 
    **schedule_formatted_data** pickle. Each identified schedule
    element will be saved as a list item. Each item consists 
    following information
    
    - *trainName* - Name of the train.
    - *trainNo* - Number of the train.
    - *startStationName* - Requested travel stating station.
    - *arrivalTime* - Train arrival time at the travel stating station.
    - *depatureTime* - Train departure time from the travel stating station.
    - *endStationName* - Finishing station of the requested travel schedule.
    - *arrivalTimeEndStation* - Arrival time to the finishing station of the requested travel schedule.
    - *finalStationName* - Ending station of the train.
    - *arrivalTimeFinalStation* - Arrival time to the ending station of the train.
    - *trainType* - Type of the train *eg:EXPRESS TRAIN*.
    - *classList* - List of dictionaries which contain **classID**, **className** keys.
    - *trainID* - Id of the train(*Not used*).
    - *trainFrequncy* - Availability of the train within the days of the week.
        + **DAILY**
        + **MONDAY TO FRIDAY**
        + **MONDAY TO FRIDAY ( EXCEPT HOLIDAYS)**
        + **MONDAY TO FRIDAY & SUNDAY**
        + **MONDAY TO SATURDAY**
        + **NOT ON SUNDAY & HOLIDAY**
        + **OTHER**
        + **NSO**
    """
    data = readPickle("gen","schedule_downloads")
    keyset = list(data.keys())
    setProgressBoundary(UPDATE_STRING,len(keyset))
    for i in range(getCurrentProgress(UPDATE_STRING),len(keyset)):
        if breakNow(UPDATE_STRING):
            break
        key = keyset[i]
        print("SDF :: "+key)####
        keyinfo = key.split("_")
        c1 = data[key]
        c2 = json.loads(c1.decode('utf-8'))
        if c2['SUCCESS']:
            content = c2["RESULTS"]["directTrains"]['trainsList']
            scheduleList = []
            for schedule in content:
                schedule['start'] = keyinfo[0]
                schedule['finish'] = keyinfo[1]
                schedule['up'] = keyinfo[2]
                scheduleList.append(schedule)
            data2 = readPickle("gen","schedule_formatted_data")
            if not data2:
                data2 = []
            writePickle("gen","schedule_formatted_data",data2+scheduleList)

def updateTrains():
    """
    **WARNING:This function generates memory overhead**.
    
    This function update :class:`.Train` using data in 
    **schedule_formatted_data** pickle. All the information not in or
    different in the :class:`.PrimaryTrain` will be updated. All the 
    updates in made to the :class:`.PrimaryTrain` will also updated in
    :class:`.Train` as well.
    """
    data = readPickle("gen","schedule_formatted_data")
    setProgressBoundary(UPDATE_STRING,len(data))
    for i in range(getCurrentProgress(UPDATE_STRING),len(data)):
        sch = data[i]
        if breakNow(UPDATE_STRING):
            break

        freq = sch['trainFrequncy']
        #0b[holiday][sun][sat][fri][thu][wed][tue][mon]
        if freq == 'DAILY':
            frequency = 0b11111111
        elif freq == 'MONDAY TO FRIDAY':
            frequency = 0b10011111
        elif freq == 'MONDAY TO FRIDAY ( EXCEPT HOLIDAYS)':
            frequency = 0b00011111
        elif freq == 'MONDAY TO FRIDAY & SUNDAY':
            frequency = 0b11011111
        elif freq == 'MONDAY TO SATURDAY':
            frequency = 0b10111111
        elif freq == 'NOT ON SUNDAY & HOLIDAY':
            frequency = 0b00111111
        elif freq == 'OTHER' or freq == 'NSO':
            frequency = 0b00000000
        else:
            frequency = 0b11111111
            addConflict("system", freq, "type '{}' not mentioned as a frequency type in update.updatedataformat.scheduleDataFormat line 54".format(freq))
        
        Zcls = [x['classID'] for x in sch['classList']]
        #0b[1][2][3]
        classes = 0
        if 3 in Zcls:
            classes += 0b1
        if 2 in Zcls:
            classes += 0b10
        if 1 in Zcls:
            classes += 0b100
        
        start_station = getStation(sch['start']) #sch['startStationName']
        finish_station = getStation(sch['finalStationName'])
        if not start_station and not finish_station:
            continue
        
        number = sch['trainNo']
        name = sch['trainName']
        up = int(sch['up'])
        Ztype = getTrainType(sch['trainType'])
        start_time = datetime.strptime(sch['depatureTime'],"%H:%M:%S").time()
        end_time = datetime.strptime(sch['arrivalTimeFinalStation'],"%H:%M:%S").time()
        
        Q1 = PrimaryTrain.objects.filter(number=number)
        if not Q1:
            Q2 = PrimaryTrain( number = number,
                        name = name,
                        start = start_station,
                        end = finish_station,
                        start_time = start_time,
                        end_time = end_time,
                        up = up,
                        type = Ztype,
                        classes = classes,
                        frequency = frequency)
            Q2.save()
            Q3 = Train( number = number,
                        name = name,
                        start = start_station,
                        end = finish_station,
                        start_time = start_time,
                        end_time = end_time,
                        up = up,
                        type = Ztype,
                        classes = classes,
                        frequency = frequency)
            Q3.save()
            addInsert("train", number, "Added new train with number '{}' (name:'{}')".format(number,name))
            print("UTI :: {} - {}".format(number,name))
        else:
            changed = False
            ss_changed = False
            obj0 = Q1[0]
            obj1 = Train.objects.get(number=number)
            
            if obj0.number != number:
                obj0.number = number
                obj1.number = number
                changed = True
            if obj0.name != name:
                obj0.name = name
                obj1.name = name
                changed = True
            if obj0.end != finish_station:
                obj0.end = finish_station
                obj1.end = finish_station
                changed = True
            if obj0.end_time != end_time:
                obj0.end_time = end_time
                obj1.end_time = end_time
                changed = True
            if obj0.up != up:
                obj0.up = up
                obj1.up = up
                changed = True
            if obj0.type != Ztype:
                obj0.type = Ztype
                obj1.type = Ztype
                changed = True
            if obj0.classes != classes:
                obj0.classes = classes
                obj1.classes = classes
                changed = True
            if obj0.frequency != frequency:
                obj0.frequency = frequency
                obj1.frequency = frequency
                changed = True
            #TODO we have no method to identify if start station changes if it come closer to end station in an update
            if len(getStationsInBetween(Q1[0].start, finish_station)) < len(getStationsInBetween(start_station, finish_station)):
                obj0.start = start_station
                obj1.start = start_station
                
                obj0.start_time = start_time
                obj1.start_time = start_time
                
                changed = True
                ss_changed = True
            if changed:
                if Q1[0].last_update == date.today():
                    if not ss_changed:
                        addConflict("train", obj0.id, "Something not write with this object: {}".format(obj0.id))
                    else:
                        print("UTU :: {} - {}".format(number,name))
                else:
                    addUpdate("train", "somefields", obj0.id, None, None)        
                obj0.save()
                obj1.save()


def updateSchedule():
    """
    This function update :class:`.Schedule` using data in 
    **schedule_formatted_data** pickle. All the information not in or
    different in the :class:`.PrimarySchedule` will be updated. All the 
    updates in made to the :class:`.PrimarySchedule` will also updated in
    :class:`.Schedule` as well.
    """
    data = readPickle("gen","schedule_formatted_data")
    setProgressBoundary(UPDATE_STRING,len(data))
    for i in range(getCurrentProgress(UPDATE_STRING),len(data)):
        if breakNow(UPDATE_STRING):
            break
        sch = data[i]
        train = getTrainByNumber(sch['trainNo'])
        schInfo =   [{  'station' : getStation(sch['start']), #sch['startStationName']
                        'arrival' : datetime.strptime(sch['arrivalTime'],"%H:%M:%S").time(),
                        'departure' : datetime.strptime(sch['depatureTime'],"%H:%M:%S").time() },
                    {   'station' : getStation(sch['finish']), #sch['endStationName']
                        'arrival' : datetime.strptime(sch['arrivalTimeEndStation'],"%H:%M:%S").time(),
                        'departure' : None } ]
        
        print("STATION  :: {}".format([x['station'].name for x in schInfo]))####
        print("ARRIVAL  :: {}".format([x['arrival'] for x in schInfo]))####
        print("DEPARTURE:: {}".format([x['departure'] for x in schInfo]))####
        for si in schInfo:
            changed = False
            Q1 = PrimarySchedule.objects.filter(train=train,station=si['station'])
            if Q1:
                try:
                    Q2 = Schedule.objects.get(train=train,station=si['station'])
                except:
                    Q2 = Schedule(train=train,station=Q1[0].station,arrival=Q1[0].arrival, departure=Q1[0].departure)
                    Q2.save()
                Q1[0]
                if si['arrival']:
                    Q1[0].arrival = si['arrival']
                    Q2.arrival = si['arrival']
                    changed =True
                    if not Q1[0].lastUpdatedArrivalToday():
                        if not Q1[0].arrival:
                            addUpdate("schedule", "arrival", "{} - {}".format(Q2.train.number,Q2.station.name), Q2.arrival, si['arrival'])
                        else:
                            addConflict("schedule", "{} - {}".format(Q2.train.number,Q2.station.name), "{} is been replaced by {}".format(Q2.arrival, si['arrival']))
                if si['departure']:
                    Q1[0].departure = si['departure']
                    changed =True
                    if not Q1[0].lastUpdatedDepartureToday():
                        if not Q1[0].departure:
                            addUpdate("schedule", "departure", "{} - {}".format(Q2.train.number,Q2.station.name), Q2.departure, si['departure'])
                        else:
                            addConflict("schedule", "{} - {}".format(Q2.train.number,Q2.station.name), "{} is been replaced by {}".format(Q2.departure, si['departure']))
                if changed:
                    Q1[0].save()
                    Q2.save()
            else:
                Q3 = PrimarySchedule(train=train,station=si['station'],arrival=si['arrival'], departure=si['departure'] )
                Q4 = Schedule(train=train,station=si['station'],arrival=si['arrival'], departure=si['departure'] )
                
                Q3.save()
                Q4.save()
                addInsert("schedule", "{} - {}".format(Q3.train.number,Q3.station.name), "{} is been replaced by {}".format(Q3.departure, si['departure']))










