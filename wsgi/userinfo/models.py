from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=96)
    key = models.CharField(max_length=200)
    status_is_public = models.BooleanField(default=True)

    class Meta:
        db_table = 'mta_user_info'

    def __unicode__(self):
        return self.name

def saveUser():
    pass

