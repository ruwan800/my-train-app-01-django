from django.contrib import admin
from location.models import Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'gps', 'x', 'y')
admin.site.register(Location, LocationAdmin)
