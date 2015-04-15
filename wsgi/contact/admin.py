from django.contrib import admin
from contact.models import Contact


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'thread', 'dt', 'manual')
admin.site.register(Contact, SubscribeAdmin)
