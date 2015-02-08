from django.db import models
from reference.models import Reference
from userinfo.models import UserInfo

class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    subscription = models.ForeignKey(Reference)
    dt = models.DateTimeField(auto_now_add=True)
    manual = models.BooleanField(default=False)
    class Meta:
        db_table = 'subscribe'

    def __unicode__(self):
        return self
