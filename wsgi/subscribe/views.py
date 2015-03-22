from advanced.render import renderJSON
from subscribe.models import Subscribe
from advanced.user import getUser
from advanced import db
from django.views.decorators.csrf import csrf_exempt
from station.models import Station
from message.models import getThread, Thread
from train.models import Train

# def subscribed(request):
#     subscriptions = Subscribe.objects.filter(user=getUser(request.user), manual=True)
#     return renderJSON(request, [str(getObject(x.subscription.code)) for x in subscriptions])
# 
# def suggestions(request):
#     subscriptions = Subscribe.objects.filter(user=getUser(request.user), manual=False)
#     return renderJSON(request, [str(getObject(x.subscription.code)) for x in subscriptions])
# 
# def add(request, ref):
#     ref = getReferenceObject(ref)
#     Q = Subscribe(user=getUser(request), subscription=ref, manual=True)
#     Q.save()
#     return renderJSON(request, {'success':True})
# 
# def remove(request, ref):
#     ref = getReferenceObject(ref)
#     Q = Subscribe.objects.get(subscription=ref)
#     Q.delete()
#     return renderJSON(request, {'success':True})

@csrf_exempt
def get(request):
    fieldMap = {}
    contacts = db.get(Subscribe, request, fieldMap)
    return renderJSON(request, contacts)

@csrf_exempt
def add(request):
    user = getUser(request)
    ctype=request.POST.get("type", None)
    if not ctype:
        return renderJSON(request, {})
    if ctype=="station" :
        uri=request.POST.get("uri", None)
        Q0 = Station.objects.get(name=uri)
        r_contact = Q0.name
        r_name = Q0.name
        r_info = Q0.name
    if ctype=="train" :
        number=request.POST.get("number", None)
        Q0 = Train.objects.get(number=number)
        r_contact = Q0.number
        r_name = Q0.name
        r_info = "{}-{}".format(Q0.start, Q0.end)
    if not Q0:
        return renderJSON(request, {})
    thread = getThread(ctype, Q0.id)
    if not thread:
        thread = Thread(ctype=ctype, ref=Q0.id)
        thread.save()
    Q = Subscribe.objects.filter(user=user, thread=thread)
    if not len(Q):
        Q = Subscribe(user=user, thread=thread, manual=True)
        Q.save()
    else:
        Q=Q[0]
    if not Q.manual:
        Q.manual=True;
        Q.save()
    
    response = {"contact":r_contact, "type":ctype, "name":r_name, "info":r_info, "thread_id":Q.pk, "favourite":True}
    return renderJSON(request, response)
    

@csrf_exempt
def edit(request):
    pass #TODO

@csrf_exempt
def delete(request):
    pass #TODO
