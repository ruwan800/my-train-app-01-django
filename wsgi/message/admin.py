from django.contrib import admin
from message.models import Message, PublicMessage, TrainMessage,\
    StationMessage, Thread

class MessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'thread', 'sender', 'dt','text', 'star')
admin.site.register(Message, MessageAdmin)

class ThreadAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'ctype', 'ref')
admin.site.register(Thread, ThreadAdmin)
