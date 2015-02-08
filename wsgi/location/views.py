from advanced.render import renderJSON
from location.models import Location
from datetime import datetime
from advanced.user import getUser

def add(request,x,y,time):
    try:
        time = datetime.strptime(time,"%H:%M:%S").time()
        Q1 = Location(user=getUser(request.user),x=x,y=y,time=time)
        Q1.save()
        return renderJSON(request,True)
    except Exception as inst:
        print(inst)
        return renderJSON(request,False)

def all(request):
    if request.user.is_staff:
        Q1 = Location.objects.all()
        return renderJSON(request,[{'user':k.user.username,'x':k.x,'y':k.y,'time':str(k.time)} for k in Q1])
    else:
        return renderJSON(request,False)