from advanced.dir import getFile
from station.models import Station, Line, getStation
from update.models import addUpdate, addConflict, addInsert, UPDATE_STRING
from process.models import incrementProgress, setProgressBoundary
from urllib.request import urlopen
import json

def updateStations():
    """
    1. Getting station list from web-service,
    2. Getting station list from local file **data/all_stations.data**.
    3. Compare stations from both streams and ignore unidentified stations
       in web-service result.
    4. Update line information.
    """
    response = urlopen('http://m.icta.lk/services/railwayservicev2/station/getAll?lang=en')
    content = response.read()
    data0 = json.loads(content.decode('utf-8'))
    stationData = data0["RESULTS"]["stationList"]
    stationList = {}
    [ stationList.update({station["stationName"]:station}) for station in stationData ]
    
    #get processed station list from local file
    f = open(getFile("data", "all_stations.data"),'r')
    lines = f.readlines()
    f.close()
    setProgressBoundary(UPDATE_STRING,2*len(lines))
    for ln in lines:
        incrementProgress(UPDATE_STRING)
        stations = ln.strip().split(",")
        for st in stations:
            Q0 = Line.objects.filter(number=lines.index(ln))
            if not Q0:
                line = Line(number=lines.index(ln))
                line.save()
            else:
                line = Q0[0]
            pos = stations.index(st)
            name = st.strip()
            print("ST:: "+st)####
            if name in stationList:
                station = stationList[name]
                code = station["stationCode"]
                num = station["stationID"]
                obj = getStation(name)
                if obj:
                    update = False
                    if not obj.number == num:
                        addUpdate("station", "number", name, obj.number, num);
                        obj.number = num
                        update = True
                    if not obj.code == code:
                        addUpdate("station", "code", name, obj.code, code);
                        obj.code = code
                        update = True
                    if obj.pos == 0 and 0 < pos:
                        if not obj.line == line:
                            addUpdate("station", "line", name, obj.line, line);
                            obj.line = line
                            update = True
                        if not obj.pos == pos:
                            addUpdate("station", "pos", name, obj.pos, pos);
                            obj.pos = pos
                            update = True
                    elif obj.pos == pos:
                        if not obj.line == line:
                            addUpdate("station", "line", name, obj.line, line);
                            obj.line = line
                            update = True
                    if update:
                        obj.save()
                else:
                    obj = Station(line=line, pos=pos, number=num, code=code, name=name.upper(), primary_name=name)
                    addInsert("station", name, str(Station));
                    obj.save()
                del stationList[name]
            else:
                Q = getStation(name)
                if not Q:
                    obj = Station(line=line, pos=pos, name=name.upper(), primary_name=name)
                    obj.save()
                    msg =   """ Station name not exists in webservice. Added to station
                                list without number and code.
                            """
                    addConflict("station", name, msg);
    for st in stationList.keys():
        msg =   """ Station name not exists in local. Not Added to station
                    list.
                """
        name = stationList[st]["stationName"]
        addConflict("station", name, msg);
        
    #update lines
    for ln in lines:
        print("LINE:: "+ln[:100])####
        incrementProgress(UPDATE_STRING)
        num = lines.index(ln)
        stations = ln.strip().split(",")
        begin = Station.objects.get(name=stations[0].strip())
        end = Station.objects.get(name=stations[-1].strip())
        Q = Line.objects.filter(number=num)
        if Q:
            Q = Q[0]
        if not Q:
            line = Line(number=num, begin=begin, end=end)
            line.save()
            name = stationList[st]["stationName"]
            addInsert("line", str(begin)+" - "+str(end), "New line added.");
        elif not Q.begin and not Q.end:
            Q.begin=begin
            Q.end=end
            Q.save()
            name = stationList[st]["stationName"]
            addInsert("line", str(begin)+" - "+str(end), "New line added.");
        elif Q.begin != begin and Q.end != end:
            Q.begin=begin
            Q.end=end
            Q.save()
            name = stationList[st]["stationName"]
            addUpdate("line", str(begin)+" - "+str(end), "New line added.");
        
    
    #return data0 #str(lines)