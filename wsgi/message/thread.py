from advanced import db
from message.models import Thread
from advanced.render import renderJSON
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get(request):
    fieldMap = {}
    threads = db.get(Thread, request, fieldMap)
    return renderJSON(request, threads)

@csrf_exempt
def add(request):
    pass #TODO

@csrf_exempt
def edit(request):
    pass #TODO

@csrf_exempt
def delete(request):
    pass #TODO