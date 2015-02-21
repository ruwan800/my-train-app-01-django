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

def get(request):
        Q1 = Location.objects.all()
        #TODO fill with correct values
        return renderJSON(request,[{'name':k.user.username,'type':k.x,'info':k.y,'uri':str(k.time)} for k in Q1])