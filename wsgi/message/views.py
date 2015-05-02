from advanced.render import renderJSON
from advanced.user import getUser
from django.views.decorators.csrf import csrf_exempt
from message.models import Message, get_thread
from advanced import db

C_TYPE = "c_type"
USER = "user"
R_ID = "remote_id"
THREAD_ID = "thread_id"
SENDER = "sender"
MESSAGE = "message"
STAR = "star"
TIME = "time"
limit = 100


def prepare_message(message):
    ref = message.thread.get_reference()
    message_new = dict()
    message_new[C_TYPE] = message.thread.c_type
    message_new[R_ID] = message.pk
    message_new[THREAD_ID] = message.thread.pk
    message_new[SENDER] = message.sender.name
    message_new[MESSAGE] = message.text
    message_new[STAR] = message.star
    message_new[TIME] = str(message.dt)
    return message_new


@csrf_exempt
def get(request):
    user = getUser(request)
    thread = db.get_where(request, THREAD_ID)
    time = db.get_where(request, TIME)
    if thread:
        thread[USER] = user
        q = Message.objects.filter(**thread)[:limit]
    elif time:
        thread[USER] = user
        q = Message.objects.filter(**thread)
    else:
        q = Message.objects.filter(sender=user)
    output = []
    for message in q:
        output.append(prepare_message(message))
    return renderJSON(request, output)


@csrf_exempt
def add(request):
    thread_str = request.POST.get(THREAD_ID, 0)
    if not thread_str:
        return renderJSON(request, {})
    sender = getUser(request)
    message = request.POST.get(MESSAGE, "")
    star = request.POST.get(STAR, 0)
    time = request.POST.get(TIME, None)
    thread = get_thread(thread_str)

    # value = dict()
    # value[THREAD_ID] = thread.pk
    # value[SENDER] = sender
    # value[MESSAGE] = message
    # value[STAR] = star
    # value[TIME] = time

    q = Message(thread=thread, sender=sender, dt=time, text=message, star=star)
    q.save()
    return renderJSON(request, prepare_message(q))


@csrf_exempt
def edit(request):
    condition = db.get_where(request, R_ID)
    q = Message.objects.get(**condition)
    star = request.POST.get(STAR, 0)
    if star:
        q.star = star
    q.save()
    return renderJSON(request, prepare_message(q))

@csrf_exempt
def delete(request):
    condition = db.get_where(request, R_ID)
    condition[USER] = getUser(request)
    q = Message.objects.get(**condition)
    q.delete()