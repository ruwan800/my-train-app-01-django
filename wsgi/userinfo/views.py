from advanced.render import renderJSON
from friend.models import Friend
from userinfo.models import UserInfo
from advanced.error import getTrace

from django.contrib.auth import authenticate, login as login2
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def profile(request,ref):
    if ref == 'self':
        user = request.user
    else:
        raise Exception("ref:P:P:P")####
        #user = getObject(ref)
    return renderJSON(request, user)

def friends(request,ref):
    if ref == 'self':
        user = request.user
    else:
        raise Exception("ref:P:P:P")####
        #user = getObject(ref)
    friends = Friend.objects.filter(user=user)
    return renderJSON(request, friends)
    
def activity(request, ref):
    if ref == 'self':
        user = request.user
    else:
        raise Exception("ref:P:P:P")####
        #user = getObject(ref)
    return renderJSON(request, user)

def settings(request):
    user = request.user
    return renderJSON(request, user)

def update(request, field, value):
    user = UserInfo.objects.get(user=request.user)
    user.__dict__[field] = value
    user.save()
    return renderJSON(request, {'success':True})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get("USER", None)
        email = request.POST.get("EMAIL", None)
        password = request.POST.get("KEY", None)
        user = User.objects.create_user(email, None, password)
        user.save()        
        user = authenticate(username=email, password=password)
        Q = UserInfo(user=user, name=username, key=password, status_is_public=True)
        Q.save()
        login2(request, user)
        if user.is_active:
            print("User is valid, active and authenticated")
            return renderJSON(request, {'success':True, 'error':""})
        else:
            message = "The password is valid, but the account has been disabled!"
            return renderJSON(request, {'success':False, 'message':message})

def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login2(request, user)
        if user.is_active:
            print("User is valid, active and authenticated")
            return renderJSON(request, {'success':True, 'error':""})
        else:
            message = "The password is valid, but the account has been disabled!"
            return renderJSON(request, {'success':False, 'message':message})
    else:
        # the authentication system was unable to verify the username and password
        message = "The username and password were incorrect."
        return renderJSON(request, {'success':False, 'message':message})

def islogged(request):
    print(request.user)####
    if request.user.is_authenticated():
        return renderJSON(request, {'success':True})
    else:
        return renderJSON(request, {'success':False})

def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    # remember language choice saved to session
    language = request.session.get('django_language')

    request.session.flush()

    if language is not None:
        request.session['django_language'] = language

    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    return renderJSON(request, {'success':False, 'error':"dummy message"})
        
def setRegistrationID(request, regid):
    try:
        Q = UserInfo.objects.get(user=request.user)
        Q.key = regid
        Q.save()
        return renderJSON(request, {'success':True})
    except:
        return renderJSON(request, {'success':False, 'error':getTrace()})