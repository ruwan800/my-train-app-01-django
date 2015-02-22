from advanced.render import renderJSON
from subscribe.models import Subscribe
from advanced.user import getUser
from advanced import db
from django.views.decorators.csrf import csrf_exempt

# def subscribed(request):
#     subscriptions = Subscribe.objects.filter(user=getUser(request.user), manual=True)
#     return renderJSON(request, [str(getObject(x.subscription.code)) for x in subscriptions])
# 
# def suggestions(request):
#     subscriptions = Subscribe.objects.filter(user=getUser(request.user), manual=False)
#     return renderJSON(request, [str(getObject(x.subscription.code)) for x in subscriptions])
# 
# def add(request, ref):
#     ref = getReferenceObject(ref)
#     Q = Subscribe(user=getUser(request), subscription=ref, manual=True)
#     Q.save()
#     return renderJSON(request, {'success':True})
# 
# def remove(request, ref):
#     ref = getReferenceObject(ref)
#     Q = Subscribe.objects.get(subscription=ref)
#     Q.delete()
#     return renderJSON(request, {'success':True})

@csrf_exempt
def get(request):
    fieldMap = {}
    contacts = db.get(Subscribe, request, fieldMap)
    return renderJSON(request, contacts)

@csrf_exempt
def add(request):
    pass #TODO

@csrf_exempt
def edit(request):
    pass #TODO

@csrf_exempt
def delete(request):
    pass #TODO
