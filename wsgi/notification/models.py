from django.db import models
from importlib import import_module
from reference.models import ReferenceModel,Reference, getObject as refGetObject,\
    getReferenceObject
from advanced.unique import uniqueKey
from group.models import Group, getGroupList
from advanced.uri import formatText
from userinfo.models import UserInfo

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=40, unique=True)
    ref_model = models.ForeignKey(ReferenceModel)
    ref_id = models.IntegerField(max_length=40)
    class Meta:
        db_table = 'notification'

    def __unicode__(self):
        return self.id

def getObject(ref):
    """
    Reference.getObject(reference) -> object
    Return a required object for the given reference value
    """
    try:
        row = Notification.objects.get(code=ref)
    except:
        return False
    #import external model related to request
    obj = import_module("{}.models".format(row.ref_model.file))
    mod = getattr(obj, row.ref_model.name)
    #retrive row from model
    return mod.objects.get(id=row.ref_id)

def getModel(ref):
    """
    Reference.getModel(reference) -> model
    Return the model of required object for the given reference value
    """
    try:
        row = Notification.objects.get(code=ref)
    except:
        return False
    return row.ref_model

class Target(models.Model):
    id = models.AutoField(primary_key=True)
    reference = models.ForeignKey(Notification)
    group = models.ForeignKey(Group)
    target = models.ForeignKey(Reference)
    class Meta:
        db_table = 'target'

    def __unicode__(self):
        return self.id

class ViewedNotification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo)
    reference = models.ForeignKey(Notification)
    
    class Meta:
        db_table = 'notification_viewed'

    def __unicode__(self):
        return self.id
    

def saveTarget(model, reference, target):
    """
    saveTarget(model, reference, target) -> None
    Save notification and target
    model = model instance(self)
    reference = reference id
    target = list of group and target value lists [[group,target],]
    """
    Q0 = ReferenceModel.objects.filter(name=model.__name__)
    if Q0:
        model = Q0[0]
    else:
        n = model.__name__
        Q0 = ReferenceModel(name=n,file=n.lower(),uri=formatText(n))
        Q0.save()
        model = Q0
    Q1 = Notification(code=uniqueKey(), ref_model=model, ref_id=reference)
    Q1.save()
    for i in target:
        Q2 = Target(reference=Q1, group=i[0], target=getReferenceObject(i[1]))
        Q2.save()

def getNotificationReferenceList(ref):
    """
    getNotificationReferenceList(ref) -> ref_list
    Get notification references related to a given reference
    ref = reference
    ref_list = related list of reference values
    """
    ref_list = []
    groups = getGroupList(ref)
    for key in groups.keys():
        items = Target.objects.filter(group=key, target__code__in=groups[key])
        #print(key.id)
        #print(getReferenceObject(ref).id)
        for item in items:
            #print(str(groups[key]))
            #print("SSSSSSSSSSSSSSSSSS")
            #print(str(item.group))
            if item.group in groups[key]:
                ref_list.append(item.reference)
    print(len(ref_list))
    return ref_list
