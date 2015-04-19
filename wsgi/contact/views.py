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
    contact[C_TYPE] = subscription.thread.c_type
    contact[NAME] = ref.get_name()
    contact[INFO] = ref.get_info()
    contact[THREAD_ID] = subscription.thread.pk
    contact[FAVOURITE] = subscription.manual
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
    ctype = request.POST.get(C_TYPE, None)
    if not ctype:
        return renderJSON(request, {})
    if ctype == "station":
        uri = request.POST.get("uri", None)
        Q0 = Station.objects.get(name=uri)
        r_contact = Q0.name
        r_name = Q0.name
        r_info = Q0.name
    if ctype == "train":
        number = request.POST.get("number", None)
        Q0 = Train.objects.get(number=number)
        r_contact = Q0.number
        r_name = Q0.name
        r_info = "{}-{}".format(Q0.start, Q0.end)
    if not Q0:
        return renderJSON(request, {})
    thread = getThread(ctype, Q0.id)
    if not thread:
        type_id = get_thread_type_id(ctype)
        thread = Thread(c_type=type_id, ref=Q0.id)
        thread.save()
    Q = Contact.objects.filter(user=user, thread=thread)
    if not len(Q):
        Q = Contact(user=user, thread=thread, favourite=True)
        Q.save()
    else:
        Q = Q[0]
    if not Q.favourite:
        Q.favourite = True
        Q.save()

    response = {C_TYPE: ctype, NAME: r_name, INFO: r_info, THREAD_ID: thread.pk,
                FAVOURITE: True, USAGE: 1}
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
