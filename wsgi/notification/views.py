from advanced.render import renderJSON
from notification.models import getNotificationReferenceList, getObject,\
    ViewedNotification, Notification
from advanced.user import getReference, getUser

def allNotifications(request):
    notifications = getNotificationReferenceList(getReference(request))
    return renderJSON(request, notifications)

def newNotifications(request):
    notifications = getNotificationReferenceList(getReference(request))
    viewed = ViewedNotification.objects.filter(user = getUser(request))
    new = [x for x in notifications if x not in viewed]
    return renderJSON(request, new)

def viewNotification(request, ref):
    notification = getObject(ref)
    return renderJSON(request, str(notification))


def setAsViewed(request, ref):
    Q0 = ViewedNotification.objects.filter(user = getUser(request), reference__code = ref)
    if not len(Q0):
        notification = Notification.objects.get(code = ref)
        Q = ViewedNotification(user = getUser(request), reference = notification)
        Q.save()
    return renderJSON(request, {'success': True})