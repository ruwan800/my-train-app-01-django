import pickle
from more import notify
from train.models import Train
from station.models import Station
from schedule.models import Schedule



stations = {}
for item in Station.objects.all():
    stations[str(item.name)] = item

trains = {}
for item in Train.objects.all():
    trains[str(item.number)] = item

pk = open('setup/data/data.pkl', 'rb')
sh = pickle.load(pk)
pk.close()

pk = open('setup/data/data_r.pkl', 'rb')
shr = pickle.load(pk)
pk.close()

timekeys = []
times = []

for key in sh.keys():
    if key not in timekeys:
        timekeys.append(key)
        i = sh[key]
        temp = {}
        temp['station'] = i['startStationEng']
        temp['train'] = i['name']
        temp['arrival'] = i['arrival']
        temp['departure'] = i['departure']
        times.append(temp)

for key in shr.keys():
    if key not in timekeys:
        timekeys.append(key)
        i = shr[key]
        temp = {}
        temp['station'] = i['startStationEng']
        temp['train'] = i['name']
        temp['arrival'] = i['arrival']
        temp['departure'] = i['departure']
        times.append(temp)

for i in sh.keys():
    if sh[i]['startStationEng'] == sh[i]['frtrstationnameeng'] and sh[i]['totrstationnameeng'] == sh[i]['endStationEng']:
        key = "{}_{}".format(sh[i]['totrstationnameeng'],str(sh[i]['name']))
        if key not in timekeys:
            timekeys.append(key)
            j = sh[i]
            temp = {}
            temp['station'] = j['totrstationnameeng']
            temp['train'] = j['name']
            temp['arrival'] = j['departure']
            temp['departure'] = None
            times.append(temp)

for i in shr.keys():
    if shr[i]['startStationEng'] == shr[i]['frtrstationnameeng'] and shr[i]['totrstationnameeng'] == shr[i]['endStationEng']:
        key = "{}_{}".format(shr[i]['totrstationnameeng'],str(shr[i]['name']))
        if key not in timekeys:
            timekeys.append(key)
            j = shr[i]
            temp = {}
            temp['station'] = j['totrstationnameeng']
            temp['train'] = j['name']
            temp['arrival'] = j['departure']
            temp['departure'] = None
            times.append(temp)

f= open("setup/log/error_time.log",'w')

Schedule.objects.all().delete()
count = len(times)
xi = 0
print(str(count)+" items found.")
for i in times:
    try:
        one = Schedule( station=stations[i['station']], train=trains[str(i['train'])], arrival=i['arrival'], departure=i['departure'])
        one.save()
    except:
        f.write(str(i)+"\n")
    xi+=1
    notify(str(xi)+"::"+str(int(xi/count))+" done.")

f.close()











