from __future__ import unicode_literals

from advanced.structure import Structure
from django.db import models
from update.models import addConflict


class Station(models.Model, Structure):
    id = models.AutoField(primary_key=True)
    line = models.ForeignKey('Line')
    pos = models.IntegerField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=3, unique=False, blank=True)
    name = models.CharField(max_length=45, blank=True)
    primary_name = models.CharField(max_length=45, blank=True)

    def getLines(self):
        lines = [self.line]
        Q1 = Line.objects.filter(begin=self)
        Q2 = Line.objects.filter(end=self)
        return list(set(lines+list(Q1)+list(Q2)))

    class Meta:
        db_table = 'mta_station'
        ordering = ['-name']

    def __unicode__(self):
        return self.name

    def getData(self):
        return {'name':self.name}

    def getStructure(self):
        structure = [{'row':{},
                      'columns':[
                            {'type':"TEXTVIEW",'name':"Name"},
                            {'type':"TEXTVIEW",'name_target':"name"},
                                ]
                      }]
        return structure

    def get_name(self):
        return self.name

    def get_uri(self):
        return self.name.lower().replace(" ", "-")

    def get_info(self):
        return self.line.name

class Line(models.Model, Structure):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(null=True, blank=True)
    begin = models.ForeignKey('Station', related_name='line_begin', null=True, blank=True)
    end = models.ForeignKey('Station', related_name='line_end', null=True, blank=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    code = models.CharField(max_length=45, null=True, blank=True)
    class Meta:
        db_table = 'mta_line'
    
    def __unicode__(self):
        return "{} - {} - {}".format(self.number,self.begin.name,self.end.name)
    
    def getJunctions(self):
        Q1 = Station.objects.filter(line=self)
        Q2 = Line.objects.all()
        junctions = [self.begin, self.end]
        for li in Q2:
            if li.begin in Q1:
                junctions.append(li.begin)
            if li.end in Q1:
                junctions.append(li.end)
        return list(set(junctions))


class LinePath(models.Model, Structure):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    path = models.TextField(null=True, blank=True)
    up = models.BooleanField(null=False)
    in_use = models.BooleanField(null=False, default=True)
    priority = models.IntegerField(null=False, default=1)
    class Meta:
        db_table = 'mta_linepath'
    
    def __unicode__(self):
        return str(self.id)+" - "+self.name+" - "+self.path+" - "+str(self.priority)


def getStationsInBetween(start, finish):
    path = getLinePath(start, finish)
    stationList = [start]
    for i in range(len(path)):
        CL = path[i]
        if 0 < i:
            st1 = getCommonJunction(path[i-1],path[i])
        else:
            st1 = start
        if i+1 < len(path):
            st2 = getCommonJunction(path[i],path[i+1])
        else:
            st2 = finish

        if st1.line == st2.line:
            if st1.pos < st2.pos:
                Q1 = Station.objects.filter(line=CL, pos__gt=st1.pos, pos__lt=st2.pos).order_by('pos')
            else:
                Q1 = Station.objects.filter(line=CL, pos__gt=st2.pos, pos__lt=st1.pos).order_by('-pos')
        elif st1.line == CL:
            if st2 == CL.end:
                Q1 = Station.objects.filter(line=CL, pos__gt=st1.pos).order_by('pos')
            else:
                Q1 = Station.objects.filter(line=CL, pos__lt=st1.pos).order_by('-pos')
        elif st2.line == CL:
            if st1 == CL.begin:
                Q1 = Station.objects.filter(line=CL,  pos__lt=st2.pos).order_by('pos')
            else:
                Q1 = Station.objects.filter(line=CL, pos__gt=st2.pos).order_by('-pos')
        else:
            if st1 == CL.begin:
                Q1 = Station.objects.filter(line=CL).order_by('pos')
            else:
                Q1 = Station.objects.filter(line=CL).order_by('-pos')
        stationList += list(Q1)
        if st2 not in stationList:
            stationList.append(st2)
    return stationList
    

def getLinePath(start, finish):
    for line in start.getLines():
        if line in finish.getLines():
            return [line]
    Q1 = LinePath.objects.all()
    pathSet = []
    for i in Q1:
        for j in start.getLines():
            for k in finish.getLines():
                if "-{}-".format(j.number) in i.path:
                    a,b,path = i.path.partition("-{}-".format(j.number))
                    if "-{}-".format(k.number) in path:
                        path,a,b = path.partition("-{}-".format(k.number))
                        text = path.strip("-").split("--")
                        if len(text[0]):
                            pathSet.append([j.number]+[int(x) for x in text]+[k.number])
                        else:
                            return [Line.objects.get(number=int(i)) for i in [j.number, k.number]]
    sorted(pathSet, key=len)
    truePath = [Line.objects.get(number=int(i)) for i in pathSet[0]]
    return truePath

def isUpLinePath(start, finish):
    if start.line == finish.line:
        if start.pos < finish.pos:
            return True
        else:
            return False
    Q1 = LinePath.objects.all()
    pathSet = []
    min = 100000
    up = True
    for i in Q1:
        for j in start.getLines():
            for k in finish.getLines():
                if "-{}-".format(j.number) in i.path:
                    a,b,path = i.path.partition("-{}-".format(j.number))
                    if "-{}-".format(k.number) in path:
                        path,a,b = path.partition("-{}-".format(k.number))
                        text = path.strip("-").split("--")
                        if len(text[0]):
                            if len(text) < min:
                                min = len(text)
                                up = i.up
                        else:
                            return i.up
    return up

def getCommonJunction(l1, l2):
    for i in l1.getJunctions():
        if i in l2.getJunctions():
            return i
        
def getStation(text):
    Q1 = Station.objects.filter(name=text.upper())
    if Q1:
        return Q1[0]
    addConflict("station", text, "Station '{}' not found".format(text))
    Q2 = Station.objects.filter(primary_name=text)
    if Q2:
        return Q2[0]
    Q3 = Station.objects.filter(primary_name=text.title())
    if Q3:
        return Q3[0]
    Q4 = Station.objects.filter(primary_name=text.upper())
    if Q4:
        return Q4[0]
    else:
        return None