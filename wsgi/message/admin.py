from django.contrib import admin
from message.models import Message, PublicMessage, TrainMessage,\
    StationMessage

class MessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'thread', 'sender', 'dt','text', 'star')
admin.site.register(Message, MessageAdmin)

class StationMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'receiver', 'dt', 'text', 'likes', 'dislikes', 'flags')
admin.site.register(StationMessage, StationMessageAdmin)

class TrainMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'receiver', 'dt', 'text', 'likes', 'dislikes', 'flags')
admin.site.register(TrainMessage, TrainMessageAdmin)

class PublicMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'dt', 'text', 'likes', 'dislikes', 'flags')
admin.site.register(PublicMessage, PublicMessageAdmin)