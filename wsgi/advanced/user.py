from userinfo.models import UserInfo
from reference.models import getReference as GR, getReferenceObject as GRO

def getReference(request):
    ref_id = UserInfo.objects.get(user=request.user).id
    return GR(UserInfo, ref_id)

def getReferenceObject(request):
    return GRO(getReference(request))

def getUser(request):
    return UserInfo.objects.get(user=request.user)


def getUserName(request):
    Q1 = UserInfo.objects.get(user=request.user)
    return Q1.name