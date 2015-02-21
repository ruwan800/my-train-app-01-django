from django.db import models
from userinfo.models import UserInfo

class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    thread = models.IntegerField()
    dt = models.DateTimeField(auto_now_add=True)
    manual = models.BooleanField(default=False)
    class Meta:
        db_table = 'mta_contact'

    def __unicode__(self):
        return self
