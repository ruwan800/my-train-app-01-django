from django.db import models
from station.models import Station
from update.models import addInsert, addConflict


class TrainType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    type = models.CharField(max_length=45, null=True, blank=True)
    category = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'mta_train_type'
    def __unicode__(self):
        return self.name


# TODO plenty of internationalization hacks
class Train(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    start = models.ForeignKey(Station, related_name='train_start')
    end = models.ForeignKey(Station, related_name='train_end')
    start_time = models.TimeField()
    end_time = models.TimeField()
    end_time_days = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    up = models.BooleanField()
    comment = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(TrainType)
    classes = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    facilities = models.IntegerField(null=True, blank=True, default=0)
    last_update = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'mta_train'

    def __unicode__(self):
        if self.name:
            return "{}:{}".format(self.number, self.name)
        else:
            return "{} : {} - {}".format(self.start_time, self.start.name, self.end.name)

    def get_name(self):
        if self.name:
            return self.name
        else:
            return "{} - {}".format(self.start, self.end)

    def get_uri(self):
        return self.number

    def get_info(self):
        if self.name:
            return "{} - {}".format(self.start, self.end)
        else:
            return "{} - {}".format(self.start_time, self.end_time)

# TODO plenty of internationalization hacks
class PrimaryTrain(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    start = models.ForeignKey(Station, related_name='pri_train_start')
    end = models.ForeignKey(Station, related_name='pri_train_end')
    start_time = models.TimeField()
    end_time = models.TimeField()
    end_time_days = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    up = models.BooleanField()
    comment = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(TrainType)
    classes = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    facilities = models.IntegerField(null=True, blank=True, default=0)
    last_update = models.DateField(auto_now=True)

    class Meta:
        db_table = 'mta_primary_train'

    def __unicode__(self):
        if self.name:
            return "{}:{}".format(self.number, self.name)
        else:
            return "{} : {} - {}".format(self.start_time, self.start.name, self.end.name)

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
    
class EngineType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    parent_category = models.IntegerField(null=True, blank=True)
    main_category = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'mta_train_engine_type'
    def __unicode__(self):
        return self.name
    
class EngineTypeForTrain(models.Model):
    id = models.IntegerField(primary_key=True)
    train = models.ForeignKey(Train)
    enginetype = models.ForeignKey(EngineType)
    class Meta:
        db_table = 'mta_train_engine_for_train'
    def __unicode__(self):
        return self.name

class Engine(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(EngineType)
    name = models.CharField(max_length=45, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    active = models.IntegerField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'mta_train_engine'
    def __unicode__(self):
        return self.name

def getTrainByNumber(text):
    Q1 = Train.objects.filter(number=text)
    if Q1:
        return Q1[0]
    else:
        addConflict("train", text, "Train with number '{}' not found".format(text))
        return None

def getTrain(text):
    return getTrainByNumber(text)

def getTrainType(text):
    Q1 = TrainType.objects.filter(type=text)
    if Q1:
        return Q1[0]
    else:
        Q2 = TrainType(type=text, name=text)
        Q2.save()
        Q3 = TrainType.objects.filter(type=text)
        addInsert("train_type", text, "Added new train type '{}'".format(text))
        return Q3[0]