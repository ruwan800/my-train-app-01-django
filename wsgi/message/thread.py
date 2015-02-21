from advanced import db
from message.models import Thread
from advanced.render import renderJSON

def get(request):
    fieldMap = {}
    threads = db.get(Thread, request, fieldMap)
    return renderJSON(request, threads)