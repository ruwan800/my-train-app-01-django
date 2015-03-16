from django.db import models
from group import functions

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    func = models.CharField(max_length=45)
    info = models.CharField(max_length=45, default=None)
    class Meta:
        db_table = 'group'

    def __unicode__(self):
        return "{}-{}".format(self.name, self.info)

def createGroup(name, func, info):
    """
    createGroup(name, func, info) -> None
    Save newly created group
    name = group name
    func = target function name for the group.
    info = more info about this group
    """
    Q1 = Group(name=name, func=func, info=info)
    Q1.save()
    #registerObject(Q1)
    

def getGroupList(ref):
    """
    getGroups(ref) -> group_list
    Returns list of groups for given reference
    ref = reference code
    group_list = list of groups related to reference.
    """
    group_list = {}
    groups = Group.objects.all()
    for group in groups:
        func = getattr(functions, group.func)
        items = func(ref)
        if items:
            group_list[group] = items
    return group_list
