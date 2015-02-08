from advanced.render import renderJSON
from reference.models import ReferenceModel
from favourite.models import Favourite, getFavaurite

def favourites(request,model):
    model = ReferenceModel.objects.get(uri=model)
    return renderJSON(request, getFavaurite(request, model))

def mark(request, ref):
    Q = Favourite.objects.get(code=ref)
    Q.favourite=True
    Q.save()
    return renderJSON(request, {'success':True})

def unmark(request, ref):
    Q = Favourite.objects.get(code=ref)
    Q.favourite=False
    Q.save()
    return renderJSON(request, {'success':True})
