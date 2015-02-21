from advanced import db
from message.models import Thread
from advanced.render import renderJSON

def get(request):
    fieldMap = {}
    threads = db.get(Thread, request, fieldMap)
    return renderJSON(request, threads)

def add(request):
    pass #TODO

def edit(request):
    pass #TODO

def delete(request):
    pass #TODO