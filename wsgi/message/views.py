from advanced.render import renderJSON, renderForm
from message.models import saveMessage # , getThread
#from advanced.user import getUser
from message.forms import MessageForm
from django.views.decorators.csrf import csrf_exempt
from message.models import Message
from advanced import db
#from reference.models import getReferenceByObject

"""
def allMessages(request):
    result = Message.objects.filter(sender=getUser(request))
    threads = []
    messages = []
    for x in result:
        if x.thread not in threads:
            messages.append({'user': x.receiver.name, 'user_ref': getReferenceByObject(x.receiver), 'thread': x.thread, 'dt': str(x.dt), 'text': x.text[:100]})
            threads.append(x.thread)
    return renderJSON(request, messages)

def thread(request,ref):
    thread = getThread(request, ref)
    return renderJSON(request, [{'user': x.receiver.name, 'user_ref': getReferenceByObject(x.receiver), 'dt': str(x.dt), 'text': x.text} for x in thread])

def view(request,ref):
    x = Message.objects.get(code=ref)
    return renderJSON(request, {'user': x.receiver.name, 'user_ref': getReferenceByObject(x.receiver), 'dt': str(x.dt), 'text': x.text})
"""

@csrf_exempt
def write(request):
    if request.method == 'POST':
        msg = request.POST.get("MESSAGE", None)
        target = request.POST.get("TARGET", None)
        target_type = request.POST.get("TYPE", None)
        result = saveMessage(request, msg, target_type, target)
        return renderJSON(request, {'success':True})
        #return renderJSON(request, str(result.read()))
    else:
        return renderJSON(request, {'success':False})

def get(request):
    fieldMap = {}
    messages = db.get(Message, request, fieldMap)
    return renderJSON(request, messages)

"""
def viewed(request,ref):
    msg = Message.objects.get(code=ref)
    msg.visited = True
    msg.save()
    return renderJSON(request, {'success':True})

def received(request,ref):
    msg = Message.objects.get(code=ref)
    msg.received = True
    msg.save()
    return renderJSON(request, {'success':True})
"""