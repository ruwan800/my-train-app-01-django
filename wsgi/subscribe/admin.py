from django.contrib import admin
from subscribe.models import Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'thread', 'dt', 'manual')
admin.site.register(Subscribe, SubscribeAdmin)
