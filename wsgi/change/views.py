from change.models import suggestForm, DropList, suggestFormAccept
from advanced.render import renderForm, renderJSON
from advanced.user import getUser
from reference.models import getReferenceObject

def edit(request,ref):
    if request.method == 'POST':
        suggestFormAccept(request, ref, request.POST)
        return renderJSON(request, {'success':True})
    else:
        form = suggestForm(ref)
    return renderForm(request, ref, form)

def drop(request,ref):
    item = DropList(target=getReferenceObject(ref), user=getUser(request))
    item.save()
    return renderJSON(request, {'success':True})