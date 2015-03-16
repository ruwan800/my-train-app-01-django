from userinfo.models import UserInfo

# def getReference(request):
#     ref_id = UserInfo.objects.get(user=request.user).id
#     return GR(UserInfo, ref_id)
# 
# def getReferenceObject(request):
#     return GRO(getReference(request))

def getUser(request):
    if not request.user.username:
        raise "No valid user available."
    return UserInfo.objects.get(user__username=request.user.username)


def getUserName(request):
    Q1 = UserInfo.objects.get(user=request.user)
    return Q1.name