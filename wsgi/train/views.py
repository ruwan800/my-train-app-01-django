from advanced.render import renderJSON
from train.models import Train
from reference.models import getObject


def search(request, text):
    trains = Train.objects.filter(name__contains=text)
    return renderJSON(request, [str(x) for x in trains])

def view(request, ref):
    return renderJSON(request, str(getObject(ref)))

def getAll(request):
    result = Train.objects.all();
    return renderJSON(request, [{"name":x.name, "info": "{} : {} - {}".format(x.start_time, x.start.name, x.end.name),"number":x.number} for x in result])

