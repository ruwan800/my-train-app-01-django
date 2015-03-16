from django.contrib import admin
from userinfo.models import UserInfo

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'user', 'key', 'status_is_public')
admin.site.register(UserInfo, UserAdmin)
