from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myrailway.views.home', name='home'),
    # url(r'^myrailway/', include('myrailway.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #homepage
    url(r'^$', 'home.views.home', name='home'),
    url(r'^test$', 'home.views.test', name='home'),
    
    #document
    url(r'^doc/', include('documentation.urls')),
    
    #change
    url(r'^s/change/edit/(?P<ref>[a-z0-9]{32})$', 'change.views.edit'),
    url(r'^s/change/drop/(?P<ref>[a-z0-9]{32})$', 'change.views.drop'),
    
    #comment
    url(r'^s/comments/all$', 'comment.views.allComments'),
    url(r'^s/comments/view/(?P<ref>[a-z0-9]{32})$', 'comment.views.view'),
    url(r'^s/comments/write$', 'comment.views.write'),
    
    #favourites
    url(r'^s/favourites/(?P<model>[a-z0-9_-]*)$', 'favourite.views.favourites'),
    url(r'^s/favourites/mark/(?P<ref>[a-z0-9]{32})$', 'favourite.views.mark'),
    url(r'^s/favourites/unmark/(?P<ref>[a-z0-9]{32})$', 'favourite.views.unmark'),
    
    #friend
    url(r'^s/friends/all$', 'friend.views.getAll'),
    
    
    #location
    url(r'^s/location/(?P<x>[0-9.]*)/(?P<y>[0-9.]*)/(?P<time>[0-9:]*)$', 'location.views.add'),
    url(r'^s/location/all$', 'location.views.all'),
    
    #messages
    #url(r'^s/messages/all$', 'message.views.allMessages'),
    #url(r'^s/messages/thread/(?P<ref>[a-z0-9]{32})$', 'message.views.thread'),
    #url(r'^s/messages/view/(?P<ref>[a-z0-9]{32})$', 'message.views.view'),
    url(r'^s/messages/write$', 'message.views.write'),
    
    #notification
    url(r'^s/notifications/all$', 'notification.views.allNotifications'),
    url(r'^s/notifications/new$', 'notification.views.newNotifications'),
    url(r'^s/notifications/view/(?P<ref>[a-z0-9]{32})$', 'notification.views.viewNotification'),
    url(r'^s/notifications/viewed/(?P<ref>[a-z0-9]{32})$', 'notification.views.setAsViewed'),

    #progress
    #url(r'^s/update$', 'update.views.update'),
    #url(r'^s/update/progress$', 'update.views.progress'),
    #url(r'^s/update/test', 'update.views.test'),

    
    #reference
    url(r'^s/reference/view/(?P<ref>[a-z0-9]{32})$', 'reference.views.view'),
    url(r'^s/reference/data/(?P<ref>[a-z0-9]{32})$', 'reference.views.getData'),
    url(r'^s/reference/structure/(?P<ref>[a-z0-9]{32})$', 'reference.views.getStructure'),
    
    #schedule
    url(r'^s/schedule/from/(?P<begin>[a-z0-9-]*)/to/(?P<end>[a-z0-9-]*)$', 'schedule.views.find'),
    url(r'^s/schedule/info/(?P<ref1>[a-z0-9-]*)/(?P<ref2>[a-z0-9-]*)$', 'schedule.views.info'),
    
    #station
    url(r'^s/stations/by-line/(?P<ref>[a-z0-9]{32})$', 'station.views.findByLine'),
    url(r'^s/stations/search/(?P<text>\w{3,20})$', 'station.views.search'),
    url(r'^s/stations/view/(?P<ref>[a-z0-9]{32})$', 'station.views.view'),
    url(r'^s/stations/all$', 'station.views.viewAll'),
    
    #status
    url(r'^s/status/new/(?P<ref>[a-z0-9]{32})$', 'status.views.checkIn'),    
    url(r'^s/status/find/(?P<ref>[a-z0-9]{32})$', 'status.views.checkInsAt'),
    
    #subscribe
    url(r'^s/subscribe/subscribed$', 'subscribe.views.subscribed'),
    url(r'^s/subscribe/suggestions$', 'subscribe.views.suggestions'),
    url(r'^s/subscribe/add/(?P<ref>[a-z0-9]{32})$', 'subscribe.views.add'),
    url(r'^s/subscribe/remove/(?P<ref>[a-z0-9]{32})$', 'subscribe.views.remove'),
    
    #train
    url(r'^s/trains/search/(?P<text>\w{3,20})$', 'train.views.search'),
    url(r'^s/trains/view/(?P<ref>[a-z0-9]{32})$', 'train.views.view'),
    url(r'^s/trains/view/(?P<ref>[a-z0-9]{32})$', 'train.views.view'),
    url(r'^s/trains/all$', 'train.views.getAll'),

    #login
    url(r'^s/user/login/(?P<username>[a-z0-9]*)/(?P<password>[a-z0-9]*)$', 'userinfo.views.login',name="Login"),
    url(r'^s/user/logout/$', 'userinfo.views.logout',name="Logout"),
    url(r'^s/user/isi/$', 'userinfo.views.islogged',name="is logged in?"),
    url(r'^s/user/register$', 'userinfo.views.register',name="Register"),
    url(r'^s/user/gcm_id/(?P<regid>[a-zA-Z0-9_-]*)$', 'userinfo.views.setRegistrationID'),
    
    #user
    url(r'^s/user/profile/(?P<ref>([a-z0-9]{32}|self))$', 'userinfo.views.profile'),
    url(r'^s/user/profile/(?P<ref>([a-z0-9]{32}|self))$', 'userinfo.views.friends'),
    url(r'^s/user/profile/(?P<ref>([a-z0-9]{32}|self))$', 'userinfo.views.activity'),
    url(r'^s/user/settings$', 'userinfo.views.settings'),
    url(r'^s/user/update/(?P<field>[a-z0-9_]{3,20})/(?P<value>[a-zA-Z0-9_]*)$', 'userinfo.views.update'),
    
    #update
)
