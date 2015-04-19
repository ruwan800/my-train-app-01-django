from advanced.render import renderJSON
from station.models import Station
from advanced import db
from django.views.decorators.csrf import csrf_exempt

# def findByLine(request, ref):
#     line = getObjectByName(ref)
#     stations = Station.objects.filter(line=line)
#     return renderJSON(request, [ {'name':x.name, 'line':x.line, 'code':x.code, 'number':x.number} for x in stations ])


def search(request, text):
    stations = Station.objects.filter(name__contains=text)
    print(stations[0])
    return renderJSON(request, [ {'name':x.name, 'line':x.line, 'code':x.code, 'number':x.number} for x in stations ])
    
# def view(request, ref):
#     x = getObject(ref)
#     return renderJSON(request, {'name':x.name, 'line':x.line, 'code':x.code, 'number':x.number})


def viewAll(request):
    stations = Station.objects.all().order_by('name')
    return renderJSON(request, [ {'name':x.name, 'uri':x.name.lower().replace(" ","-"), 'active': True} for x in stations ])

@csrf_exempt
def get(request):
    field_map = {}
    stations = Station.objects.all()
    station_real = [{"name": x.get_name(), "uri": x.get_uri(), "active": True} for x in stations]
    return renderJSON(request, station_real)

@csrf_exempt
def add(request):
    pass # TODO

@csrf_exempt
def edit(request):
    pass # TODO

@csrf_exempt
def delete(request):
    pass # TODO
