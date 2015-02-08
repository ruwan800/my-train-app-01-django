from django.contrib import admin
from message.models import UserMessage, PublicMessage, TrainMessage,\
    StationMessage

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'receiver', 'dt','text', 'received', 'visited')
admin.site.register(UserMessage, UserMessageAdmin)

class StationMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'receiver', 'dt', 'text', 'likes', 'dislikes', 'flags')
admin.site.register(StationMessage, StationMessageAdmin)

class TrainMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'receiver', 'dt', 'text', 'likes', 'dislikes', 'flags')
admin.site.register(TrainMessage, TrainMessageAdmin)

class PublicMessageAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'sender', 'dt', 'text', 'likes', 'dislikes', 'flags')
admin.site.register(PublicMessage, PublicMessageAdmin)