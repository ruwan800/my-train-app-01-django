from django.db import models
from notification.models import saveTarget
from reference.models import Reference, getReferenceObject
from advanced.user import getUser, getReferenceObject as GRO
from group.models import Group

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Reference, related_name='s_user')
    status = models.ForeignKey(Reference, related_name='s_status')
    dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    class Meta:
        db_table = 'status'

    def __unicode__(self):
        return self.text

def saveStatus(request, status, msg):
    """
        saveStatus(equest, status, msg) -> None
        save new comment.
        request = request object
        status = reference
        msg = Message text
    """
    profile = getUser(request)
    user = GRO(request)
    ref = getReferenceObject(status)
    public = profile.status_is_public
    Q = Status(text=msg, user=user, public=public, status=ref)
    Q.save()
    friends = Group.objects.get(name="friends")
    saveTarget(Status,Q.pk,[[friends, user.code]])
