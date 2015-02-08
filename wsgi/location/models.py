from django.db import models
from userinfo.models import UserInfo

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    gps = models.BooleanField(default=False)


    class Meta:
        db_table = 'mta_location'
        ordering = ['-time']

    def __unicode__(self):
        return "{}:{}".format(self.x,self.y)
