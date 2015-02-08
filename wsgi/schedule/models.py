# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from station.models import Station
from train.models import Train
from reference.models import Reference
from datetime import date

class Schedule(models.Model):
    id = models.IntegerField(primary_key=True)
    ##ref = models.ForeignKey(Reference) ##TODO
    station = models.ForeignKey(Station)
    train = models.ForeignKey(Train)
    arrival = models.TimeField(null=True)
    departure = models.TimeField(null=True)
    arrival_days = models.IntegerField(default=0)
    departure_days = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'mta_schedule'
        
    def __unicode__(self):
        return "{}:{} - {}".format(self.departure, self.station, self.train)


class PrimarySchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    station = models.ForeignKey(Station)
    train = models.ForeignKey(Train)
    arrival = models.TimeField(null=True)
    departure = models.TimeField(null=True)
    arrival_days = models.IntegerField(default=0)
    departure_days = models.IntegerField(default=0)
    last_update_arrival = models.DateField(auto_now=True)
    last_update_departure = models.DateField(auto_now=True)
    class Meta:
        db_table = 'mta_primary_schedule'
        
    def __unicode__(self):
        return "{}:{} - {}".format(self.departure, self.station, self.train)

    def getTrains(self,station,time,duration):
        return self.objects.filter(station=station,departure__range=[time, time+duration])

    def lastUpdatedArrivalToday(self):
        if self.last_update_arrival == date.today():
            return True
        return False

    def lastUpdatedDepartureToday(self):
        if self.last_update_departure == date.today():
            return True
        return False


