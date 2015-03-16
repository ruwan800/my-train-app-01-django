from django.db import models
from reference.models import Reference, getModel, getObject
from userinfo.models import UserInfo
from importlib import import_module
from advanced.user import getUser
#import change.forms as Forms

class Change(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    target = models.ForeignKey(Reference)
    field = models.CharField(max_length=45)
    old = models.TextField(null=True, blank=True)
    new = models.TextField(null=True, blank=True)
    revieved = models.BooleanField(default=False)
    class Meta:
        db_table = 'change'

    def __unicode__(self):
        return self.target

class DropList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    target = models.ForeignKey(Reference)
    revieved = models.BooleanField(default=False)
    class Meta:
        db_table = 'droplist'

    def __unicode__(self):
        return self.target
    
def suggestForm(ref):
    """
    suggestForm(ref) -> form
    ref = object reference
    """
    target = getModel(ref)
    #import model form related to request from forms
    obj = import_module("{}.forms".format(target.file))
    Form = getattr(obj, "{}Form".format(target.name))
    return Form(instance=getObject(ref))

def suggestFormAccept(request, ref, params):
    """
    suggestFormAccept(ref,params) -> None
    ref = object reference
    params = request.POST
    """
    reference = Reference.objects.get(code=ref)
    old = getModel(ref)
    old_obj = getObject(ref)
    old_fields = [ i.name for i in old._meta.fields ] #TODO is that okay to use _meta?
    new_fields = params.keys()
    for field in old_fields:
        if field in new_fields:
            print(getattr(old_obj, field))
            print(params[field])
            if getattr(old_obj, field) != params[field]:
                Q = Change.objects.filter(user=getUser(request), target=reference, field=field)
                if Q:
                    Q[0].new=params[field]
                    Q[0].save()
                else:
                    Q1 = Change(target=reference, field=field, old=getattr(old_obj, field), new=params[field], user=getUser(request))
                    Q1.save()
