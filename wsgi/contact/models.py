from django.db import models
from userinfo.models import UserInfo
from message.models import Thread


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    thread = models.ForeignKey(Thread)
    dt = models.DateTimeField(auto_now_add=True)
    favourite = models.BooleanField(default=False)
    usage = models.IntegerField(default=0)

    class Meta:
        db_table = 'mta_contact'

    def __unicode__(self):
        return self