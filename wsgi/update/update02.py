from advanced.dir import getFile
from station.models import Station, getStationsInBetween, LinePath
from update.models import  addConflict, addInsert
from urllib.request import urlopen, Request
import threading
from update.models import UPDATE_STRING
from process.models import setProgressBoundary, incrementProgress, getCurrentProgress
from advanced.pickle import readPickle, writePickle


def generateLinePaths():
    """
    Generate line paths using *start* and *end* of each :class:`.Train`.
    This function use **main_stations.data** and **main_stations_r.data** 
    text files to generate line paths. All the path information is saved in
    :class:`.LinePath`. line paths are saved as a string. each path number
    is enclosed with two '-' signs from both sides. For an example a line 
    path represent paths 1,2,3,12 will be like "*-1--2--3--12-*".
    """

    #TODO implement this method using starting and ending points of each line

    f = open(getFile("data", "main_stations.data"),'r')
    lines = f.readlines()
    f.close()
    f = open(getFile("data", "main_stations_r.data"),'r')
    lines_r = f.readlines()
    f.close()
    
    

    #generate LinePaths
    lineSets = []    
    up = True
    
    setProgressBoundary(UPDATE_STRING,len(lines)+len(lines_r))
    for Zlines in [lines,lines_r]:
        for line in Zlines:
            incrementProgress(UPDATE_STRING)
            print("STR:: "+str(line.strip()))#####
            x,z,y = line.partition(":")
            start = x.strip()
            finish = y.strip()
            Q1 = Station.objects.filter(name=start)
            if not Q1:
                addConflict("schedule",start, "failed to find station object by name '{}'".format(start))
                continue
            Q2 = Station.objects.filter(name=finish)
            if not Q2:
                addConflict("schedule",finish, "failed to find station object by name '{}'".format(finish))
                continue
            sl = Q1[0].getLines()
            fl = Q2[0].getLines()
            lineSet = [[x] for x in sl]
            found = False
            for i in sl:
                for j in fl:
                    if i == j:
                        found = True
            #print("Starting Line: {} Finishing Line: {}".format(str([x.number for x in sl]),str([x.number for x in fl])))
            i = 0 ####
            while not found:
                #print("----------------------------------"+str(i)+"---------------------------------")#####
                lineSetB = lineSet
                i +=1 ####
                #print("L1::LINES: "+str([[z.number for z in y] for y in lineSet]))#####
                lineSet = []
                for LSB in lineSetB:
                    if found:
                        break
                    junctions = LSB[-1].getJunctions()
                    #print("L1:JUNCS: "+str([z.name for z in junctions]))#####
                    for ju in junctions:
                        if found:
                            break
                        julns = ju.getLines()
                        #print("LX:LINES from "+str(ju.name)+": "+str([z.number for z in julns]))####
                        for li in julns:
                            #print("LAST LINE: {} Curr LINE: {}".format(LSB[-1].number,li.number))####
                            if li != LSB[-1]:
                                #print("COMP:: Curr LINE: {} Final LINE: {}".format(li.number,str([x.number for x in fl])))####
                                trueSet = LSB+[li]
                                if li in fl:
                                    found = True
                                    #print("FOUND:: {}".format(str([z.number for z in trueSet])))####
                                    exists = False
                                    if len(lineSets):
                                        for LSTS in lineSets:
                                            if "".join(["-{}-".format(str(i.number)) for i in trueSet]) in LSTS:
                                                exists = True
                                                break
                                    if not exists:
                                        text = "".join(["-{}-".format(str(i.number)) for i in trueSet])
                                        lineSets.append(text)
                                        #check exists in db and save if doesn't
                                        Q1 = LinePath.objects.filter(path=text)
                                        if not Q1:
                                            Q2 = LinePath(path=text, in_use=True, up = up)
                                            Q2.save()
                                            addInsert("linepath",text, "new path added")
                                    break
                                else:
                                    #print("ADD:: {}".format(str([x.number for x in trueSet])))####
                                    lineSet.append(trueSet)
        up = False


def generateCriteriaFile():
    """
    This function generates more optimized set of start and ending 
    station list that will used to download schedule data. This function 
    use **main_stations.data** and **main_stations_r.data** text files to 
    generate the output. The output is a CSV text file contains start
    station, end station and up value to represent direction of train 
    travel.
    """
    searchCriteria = {}
    
    f = open(getFile("data", "main_stations.data"),'r')
    lines = f.readlines()
    f.close()
    f = open(getFile("data", "main_stations_r.data"),'r')
    lines_r = f.readlines()
    f.close()
    
    up = True
    setProgressBoundary(UPDATE_STRING,len(lines)+len(lines_r))
    for lineset in [lines,lines_r]:
        #assign weights to stations based on occurence
        stations = {}
        for line in lineset:
            x,z,y = line.partition(":")
            start = x.strip()
            finish = y.strip()
            if start in stations:
                stations[start] += 1
            else:
                stations[start] = 1
            if finish in stations:
                stations[finish] += 1
            else:
                stations[finish] = 1
    
        for line in lineset:
            incrementProgress(UPDATE_STRING)
            x,z,y = line.partition(":")
            start = x.strip()
            finish = y.strip()
            Q1 = Station.objects.filter(name=start)
            if not Q1:
                addConflict("schedule",start, "failed to find station object by name '{}'".format(start))
                continue
            Q2 = Station.objects.filter(name=finish)
            if not Q2:
                addConflict("schedule",finish, "failed to find station object by name '{}'".format(finish))
                continue
            Lstart = Q1[0]
            Lfinish = Q2[0]
            if not start+" - "+finish in searchCriteria:
                searchCriteria[start+" - "+finish] = {"start":start,"finish":finish,"up":up}
            betweens = getStationsInBetween(Lstart,Lfinish)
            for st in betweens:
                stn = st.name
                if stations[start] < stations[finish]:
                    if not stn+" - "+finish in searchCriteria and not stn == finish:
                        searchCriteria[stn+" - "+finish] = {"start":stn,"finish":finish,"up":up}
                else:
                    if not start+" - "+stn in searchCriteria and not start == stn:
                        searchCriteria[start+" - "+stn] = {"start":start,"finish":stn,"up":up}
        up = False

    f = open(getFile("gen","schedule_criteria"),'w')
    criteria = list(searchCriteria.keys())
    criteria.sort()
    for cr in criteria:
        sc = searchCriteria[cr]
        text = "{:<20},{:<20},{:<4}\n".format(sc["start"], sc["finish"], sc["up"])
        f.write(text)
    f.close()


def readpage(info):
    """
    Each occurrence of this function is called in a separate thread since it 
    downloads schedule information and it takes time.
    """
    print("RSP:: {} - {} - {}".format(info[0],info[1],info[2]))####
    Zurl = "http://m.icta.lk/services/railwayservicev2/train/searchTrain?startStationID={}&endStationID={}&searchDate=2014-01-21&startTime=00:00:00&endTime=23:59:59&lang=en"
    #http://m.icta.lk/services/railwayservicev2/train/searchTrain?startStationID=184&endStationID=61&searchDate=2014-01-21&startTime=00:00:00&endTime=23:59:59&lang=en
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    Q1 = Station.objects.filter(name=info[0])
    if Q1:
        start = Q1[0].number
    Q2 = Station.objects.filter(name=info[1])
    if Q1:
        finish = Q2[0].number
    if not start or not finish:
        addConflict("retrieve_schedule", info[0]+" - "+info[1],"Atleast {} or {} don't have a number.({},{})".format(info[0], info[1], start, finish) )
        incrementProgress(UPDATE_STRING)
        return False
    up = info[2]
    mod_url = Zurl.format(start,finish)
    Zreqest = Request(mod_url,headers=hdr)
    try:
        response = urlopen(Zreqest).read()
    except:
        response = urlopen(Zreqest).read()
    incrementProgress(UPDATE_STRING)
    content = readPickle("gen","schedule_downloads")
    if not content:
        content = {}
    text = "{}_{}_{}".format(info[0],info[1],up)
    content[text] = response
    writePickle("gen","schedule_downloads",content)

def retrieveSchedulePages():
    """
    This method creates a pool of threads to retrieve schedule information
    from web-service using **schedule_criteria** file. All information received 
    in each result will be save in **schedule_downloads.pickle** as dictionary 
    value under a key generated with "*<start>_<end>_<up>*" format.
    """
    thread_list = []
    parralle_downloads = 10
    f = open(getFile("gen","schedule_criteria"),'r')
    lines = f.readlines()
    f.close()
    setProgressBoundary(UPDATE_STRING,len(lines))
    for i in range(getCurrentProgress(UPDATE_STRING),len(lines)):
        info = [ x.strip() for x in lines[i].split(",")]
        #page download threads
        t = threading.Thread(target=readpage, args=(info,))
        thread_list.append(t)
    
    for i in range(0,len(thread_list),parralle_downloads):
        for j in range(i,i+parralle_downloads):
            if j+1 < len(lines):
                thread_list[j].start()
    
        for j in range(i,i+parralle_downloads):
            if j+1 < len(lines):
                thread_list[j].join()
