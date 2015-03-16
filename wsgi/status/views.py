from advanced.render import renderJSON
from status.models import Status, saveStatus
from reference.models import getReferenceObject, getObject

def checkIn(request, ref):
    msg = request.POST.get("message", None)
    saveStatus(request, ref, msg)
    return renderJSON(request, {'success':True})

def checkInsAt(request,ref):
    ref = getReferenceObject(ref)
    objs = Status.objects.filter(status=ref)
    return renderJSON(request, [str(getObject(x.user.code)) for x in objs])
