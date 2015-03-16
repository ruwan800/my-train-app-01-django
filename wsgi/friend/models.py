from django.db import models
from advanced.user import getUser
from userinfo.models import UserInfo

class Friend(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, related_name='f_user')
    friend = models.ForeignKey(UserInfo, related_name='f_friend')
    mutual = models.BooleanField(default=False)
    class Meta:
        db_table = 'friend'

    def __unicode__(self):
        return self.user
    
        
    def isFriend(self, request):
        if request.user == self.user.user:
            return True;
        return False;


def getFriend(request, uname):
    Q1 = Friend.objects.get(friend_username=uname);
    if Q1.isFriend(request):
        return Q1
