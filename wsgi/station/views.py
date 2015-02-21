from advanced.render import renderJSON
from station.models import Station
from advanced import db

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

def get(request):
    fieldMap = {}
    stations = db.get(Station, request, fieldMap)
    return renderJSON(request, stations)

def add(request):
    pass #TODO

def edit(request):
    pass #TODO

def delete(request):
    pass #TODO
