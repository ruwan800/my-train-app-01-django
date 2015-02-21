from advanced.render import renderJSON
from train.models import Train


def search(request, text):
    trains = Train.objects.filter(name__contains=text)
    return renderJSON(request, [str(x) for x in trains])

# def view(request, ref):
#     return renderJSON(request, str(getObject(ref)))

def getAll(request):
    result = Train.objects.all();
    return renderJSON(request, [{"name":x.name, "info": "{} : {} - {}".format(x.start_time, x.start.name, x.end.name),"number":x.number} for x in result])

def get(request):
    stations = Train.objects.all().order_by('name')
    return renderJSON(request, [ {'name':x.name, 'uri':x.name.lower().replace(" ","-"), 'active': True} for x in stations ])

def add(request):
    pass #TODO

def edit(request):
    pass #TODO

def delete(request):
    pass #TODO
