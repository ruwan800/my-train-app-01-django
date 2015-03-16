from django.contrib import admin
from schedule.models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('train', 'station', 'arrival', 'departure')

admin.site.register(Schedule, ScheduleAdmin)
