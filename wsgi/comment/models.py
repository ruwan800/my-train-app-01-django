from django.db import models
from notification.models import saveTarget
from userinfo.models import UserInfo
from advanced.unique import uniqueKey
from advanced.user import getUser
from favourite.models import addToHistory

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=32)
    user = models.ForeignKey(UserInfo)
    dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    class Meta:
        db_table = 'comment'

    def __unicode__(self):
        return self.text

def saveComment(request, msg, target):
    """
        saveComment(msg, target) -> None
        save new comment.
        msg = Message text
        target = Target receiver list
    """
    Q1 = Comment(text=msg, user=getUser(request), ref=uniqueKey())
    Q1.save()
    for i in target:
        addToHistory(request,Comment,i[1])
    saveTarget(Comment,Q1.pk,target)
