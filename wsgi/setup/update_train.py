
import pickle
from more import notify
from station.models import Station
from train.models import Train

stations = {}
for item in Station.objects.all():
    stations[str(item.name)] = item



pk = open('setup/data/data.pkl', 'rb')
sh = pickle.load(pk)
pk.close()

pk = open('setup/data/data_r.pkl', 'rb')
shr = pickle.load(pk)
pk.close()

trains = []
trainid = []

for key in sh.keys():
    i = sh[key]
    if i['startStationEng'] == i['frtrstationnameeng'] and i['totrstationnameeng'] == i['endStationEng']:
        if int(i['name']) not in trainid:
            trainid.append(int(i['name']))
            temp = {}
            temp['number'] = i['name']
            temp['start'] =  i['frtrstationnameeng']
            temp['end'] =  i['totrstationnameeng']
            temp['start_time'] =  i['departure']
            temp['end_time'] =  i['destination']
            temp['comment'] =  i['comment']
            temp['description'] =  i['fdescriptioneng']
            temp['type'] =  i['tydescriptioneng']
            temp['up'] =  True
            trains.append(temp)

for key in shr.keys():
    i = shr[key]
    if i['startStationEng'] == i['frtrstationnameeng'] and i['totrstationnameeng'] == i['endStationEng']:
        if int(i['name']) not in trainid:
            trainid.append(int(i['name']))
            temp = {}
            temp['number'] = i['name']
            temp['start'] =  i['frtrstationnameeng']
            temp['end'] =  i['totrstationnameeng']
            temp['start_time'] =  i['departure']
            temp['end_time'] =  i['destination']
            temp['comment'] =  i['comment']
            temp['description'] =  i['fdescriptioneng']
            temp['type'] =  i['tydescriptioneng']
            temp['up'] =  False
            trains.append(temp)
for key in sh.keys():
    i = sh[key]
    if int(key.partition('_')[2]) not in trainid:
        trainid.append(int(key.partition('_')[2]))
        temp = {}
        temp['number'] = i['name']
        temp['start'] =  i['frtrstationnameeng']
        temp['end'] =  i['totrstationnameeng']
        temp['start_time'] =  "00:00:00"
        temp['end_time'] =  "00:00:00"
        temp['comment'] =  i['comment']
        temp['description'] =  i['fdescriptioneng']
        temp['type'] =  i['tydescriptioneng']
        temp['up'] = False
        trains.append(temp)

for key in shr.keys():
    i = shr[key]
    if int(key.partition('_')[2]) not in trainid:
        trainid.append(int(key.partition('_')[2]))
        temp = {}
        temp['number'] = i['name']
        temp['start'] =  i['frtrstationnameeng']
        temp['end'] =  i['totrstationnameeng']
        temp['start_time'] =  "00:00:00"
        temp['end_time'] =  "00:00:00"
        temp['comment'] =  i['comment']
        temp['description'] =  i['fdescriptioneng']
        temp['type'] =  i['tydescriptioneng']
        temp['up'] =  False
        trains.append(temp)

Train.objects.all().delete()
count = len(trains)
xi = 0

for i in trains:
    one = Train( number=i['number'], start=stations[i['start']], end=stations[i['end']], start_time=i['start_time'], end_time=i['end_time'], comment=i['comment'], description=i['description'], type=i['type'], up=i['up'])
    one.save()
    xi+=1
    notify(str(xi)+"::"+str(int(xi/count))+" done.")


