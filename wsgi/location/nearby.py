from advanced import db
from advanced.render import renderJSON
from location.models import Location
from datetime import datetime
from advanced.user import getUser
from django.views.decorators.csrf import csrf_exempt

X = "x"
Y = "y"
NAME = "name"
TYPE = "type"
INFO = "info"
URI = "uri"


def add(request, x, y,time):
    try:
        time = datetime.strptime(time,"%H:%M:%S").time()
        q1 = Location(user=getUser(request.user),x=x,y=y,time=time)
        q1.save()
        return renderJSON(request,True)
    except Exception as inst:
        print(inst)
        return renderJSON(request,False)

@csrf_exempt
def get(request):
    x = db.get_where(request, X)
    y = db.get_where(request, Y)
    q1 = Location.objects.all()
    # TODO fill with correct values
    return renderJSON(request, [{X: x, Y: y, NAME: k.user.username, TYPE: k.x, INFO: k.y, URI: str(k.time)} for k in q1])

