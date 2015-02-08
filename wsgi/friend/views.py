from django.contrib.auth.decorators import login_required
from advanced.render import renderJSON
from friend.models import Friend
from advanced.user import getUser

@login_required
def getAll(request):
    result = Friend.objects.filter(user=getUser(request.user));
    return renderJSON(request, [{"id": x.pk, "name" : x.user.name, "ref" : x.user.user.username} for x in result])
