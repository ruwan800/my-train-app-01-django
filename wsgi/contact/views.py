from django.views.decorators.csrf import csrf_exempt
from advanced import db

from advanced.render import renderJSON
from contact.models import Contact
from advanced.user import getUser
from station.models import Station
from message.models import getThread, Thread, get_thread_type_id
from train.models import Train

C_TYPE = "c_type"
NAME = "name"
USER = "user"
INFO = "info"
THREAD_ID = "thread_id"
FAVOURITE = "favourite"
USAGE = "usage"


def get_contact(subscription):
    ref = subscription.thread.get_reference()
    contact = dict()
    contact[C_TYPE] = subscription.thread.get_c_type()
    contact[NAME] = ref.get_name()
    contact[INFO] = ref.get_info()
    contact[THREAD_ID] = subscription.thread.pk
    contact[FAVOURITE] = subscription.favourite
    contact[USAGE] = subscription.usage
    return contact

@csrf_exempt
def get(request):
    user = getUser(request)
    subscriptions = Contact.objects.filter(user=user)
    response = []
    for subscription in subscriptions:
        contact = get_contact(subscription)
        response.append(contact)
    return renderJSON(request, response)


@csrf_exempt
def add(request):
    user = getUser(request)
    c_type = request.POST.get(C_TYPE, None)
    if not c_type:
        raise Exception("c_type is empty")
    if c_type == "station":
        uri = request.POST.get("uri", None)
        q0 = Station.objects.get(name=uri)
    elif c_type == "train":
        number = request.POST.get("number", None)
        q0 = Train.objects.get(number=number)
    else:
        raise Exception("c_type is incorrect")
    if not q0:
        raise Exception("reference {} is not available".format(c_type))
    thread = getThread(c_type, q0.id)
    if not thread:
        type_id = get_thread_type_id(c_type)
        thread = Thread(c_type=type_id, ref=q0.id)
        thread.save()
    q = Contact.objects.filter(user=user, thread=thread)
    if not len(q):
        q = Contact(user=user, thread=thread, favourite=True)
        q.save()
    else:
        q = q[0]
    if not q.favourite:
        q.favourite = True
        q.save()
    response = get_contact(q)
    return renderJSON(request, response)


@csrf_exempt
def edit(request):
    condition = db.get_where(request, THREAD_ID)
    condition[USER] = getUser(request)
    q = Contact.objects.get(**condition)
    favourite = request.POST.get(FAVOURITE, None)
    usage = request.POST.get(USAGE, None)
    if favourite:
        q.favourite = favourite
    if usage:
        q.usage = usage
    q.save()
    contact = get_contact(q)
    return renderJSON(request, contact)


@csrf_exempt
def delete(request):
    condition = db.get_where(request, THREAD_ID)
    condition[USER] = getUser(request)
    q = Contact.objects.get(**condition)
    q.delete()
