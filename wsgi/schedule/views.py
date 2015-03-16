from advanced.render import renderJSON
from schedule.models import Schedule
from reference.models import getReferenceByObject, getObject
from station.models import isUpLinePath, getStation
from datetime import timedelta

def find(request, begin, end):
    result = []
    if begin == end:
        return renderJSON(request, [])
    station_start = getStation(begin.replace("-"," "))
    station_finish = getStation(end.replace("-"," "))
    up = isUpLinePath(station_start,station_finish)
    Q1 = Schedule.objects.filter(station=station_start).order_by('departure')
    Q2 = Schedule.objects.filter(station=station_finish)
    for i in Q1:
        for j in Q2:
            if i.train.up == up and i.train == j.train:
                data = {}
                data['start'] = i.train.start.name
                data['finish'] = i.train.end.name
                data['ref1'] = getReferenceByObject(i)
                data['ref2'] = getReferenceByObject(j)
                data['begin_time'] = str(i.departure)
                data['begin_arrival'] = str(i.arrival)
                data['end_time'] = str(j.arrival)
                data['duration'] = _duration(i.departure, j.arrival)
                result.append(data)
    return renderJSON(request, result)

def info(request, ref1, ref2):
    structure = [{'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Arrival"},
                    {'type':"TEXTVIEW",'name_target':"arrival"},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Departure"},
                    {'type':"TEXTVIEW",'name_target':"departure"},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Arrival at Destination"},
                    {'type':"TEXTVIEW",'name_target':"destination"},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Duration"},
                    {'type':"TEXTVIEW",'name_target':"duration"},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"from Station"},
                    {'type':"BUTTON",'name_target':'begin', 'link_target':'ref_begin'},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"to Station"},
                    {'type':"BUTTON",'name_target':'end', 'link_target':'ref_end'},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Train"},
                    {'type':"BUTTON",'name_target':'train', 'link_target':'ref_train'},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Train Starts from"},
                    {'type':"BUTTON",'name_target':'start', 'link_target':'ref_start'},
                            ]
                 },
                 {'row':{},
                  'columns':[
                    {'type':"TEXTVIEW",'name':"Train ends at"},
                    {'type':"BUTTON",'name_target':'finish', 'link_target':'ref_finish'},
                            ]
                 }
                ]
    r = {}
    Q1 = getObject(ref1)
    Q2 = getObject(ref2)
    if Q1.train.name:
        r['train'] = Q1.train.name
    else:
        r['train'] = "{}-{}".format(Q1.train.start.name.title(),Q1.train.end.name.title())
    r['arrival'] = str(Q1.arrival)
    r['departure'] = str(Q1.departure)
    r['destination'] = str(Q2.arrival)
    r['duration'] = _duration(Q1.departure,Q2.arrival)
    r['ref_train'] = getReferenceByObject(Q1.train)
    r['start'] = Q1.train.start.name
    r['ref_start'] = getReferenceByObject(Q1.train.start)
    r['finish'] = Q1.train.end.name
    r['ref_finish'] = getReferenceByObject(Q1.train.end)
    r['begin'] = Q1.station.name
    r['ref_begin'] = getReferenceByObject(Q1.station)
    r['end'] = Q2.station.name
    r['ref_end'] = getReferenceByObject(Q2.station)
    return renderJSON(request, {'structure':structure, 'data':r})

def _duration(begin,end):
    d_begin = timedelta(hours=begin.hour,minutes=begin.minute)
    d_end = timedelta(hours=end.hour,minutes=end.minute)
    dt = d_end - d_begin
    return "{:02d}:{:02d}:00".format(dt.seconds//3600, (dt.seconds//60)%60)
