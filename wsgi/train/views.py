from advanced.render import renderJSON
from train.models import Train
from django.views.decorators.csrf import csrf_exempt
from advanced import db


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
    fieldMap = {}
    trains = db.get(Train, request, fieldMap)
    trainsReal = [{"name": x.name, "info": "{}-{}".format(x.start, x.end), "number":x.number} for x in trains ]
    return renderJSON(request, trainsReal)

@csrf_exempt
def add(request):
    pass #TODO

@csrf_exempt
def edit(request):
    pass #TODO

@csrf_exempt
def delete(request):
    pass #TODO
