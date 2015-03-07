from django.db import models
from userinfo.models import UserInfo
from message.models import Thread

class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    thread = models.ForeignKey(Thread)
    dt = models.DateTimeField(auto_now_add=True)
    manual = models.BooleanField(default=False)
    class Meta:
        db_table = 'mta_contact'

    def __unicode__(self):
        return self
