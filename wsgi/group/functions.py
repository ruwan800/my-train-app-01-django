from advanced.autoimport import importModel
from datetime import datetime, timedelta
from reference.models import getReferenceByObject

def defaultFunction(ref):
    return [ref]

def UsersSubscribed(ref):
    model = importModel("Subscribe")
    obj = model.objects.filter(user=ref)
    return [i.subscription for i in obj]

def UsersOfFriend(ref):
    model = importModel("Friend")
    obj = model.objects.filter(user=ref)
    return [i.friend for i in obj]

def UsersAtStation(ref):
    #model = importModel("Status")
    #past_hour = datetime.today() - timedelta(hours = 1)
    #obj = model.objects.filter(status__code=ref, public=True, dt__gt=past_hour)
    #return [getReferenceByObject(i) for i in obj]
    return []

def UsersFavouredStation(ref):
    return []

def UsersNearStation(ref):
    return []

