from advanced.render import renderJSON
from train.models import Train
from django.views.decorators.csrf import csrf_exempt


def search(request, text):
    trains = Train.objects.filter(name__contains=text)
    return renderJSON(request, [str(x) for x in trains])

# def view(request, ref):
#     return renderJSON(request, str(getObject(ref)))

def getAll(request):
    result = Train.objects.all();
    return renderJSON(request, [{"name":x.name, "info": "{} : {} - {}".format(x.start_time, x.start.name, x.end.name),"number":x.number} for x in result])

@csrf_exempt
def get(request):
    stations = Train.objects.all().order_by('name')
    return renderJSON(request, [ {'name':x.name, 'uri':x.name.lower().replace(" ","-"), 'active': True} for x in stations ])

@csrf_exempt
def add(request):
    pass #TODO

@csrf_exempt
def edit(request):
    pass #TODO

@csrf_exempt
def delete(request):
    pass #TODO
