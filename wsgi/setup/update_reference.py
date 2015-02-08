##update references for existing object
from more import notify
from schedule.models import Schedule
from train.models import Train
from station.models import Station
from reference.models import getReference
from userinfo.models import UserInfo
from group.models import Group


#models = [Station, Train, User, Schedule, Group]
models = [UserInfo]
for model in models:
    objs = model.objects.all()
    _all_count = len(objs)
    _count = 0
    for obj in objs:
        _count += 1
        getReference(model, obj.id)
        notify("Adding reference to "+model.__name__+". "+str(int(100*_count/_all_count))+"% completed.")
print("\n")