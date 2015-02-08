from django.contrib import admin
from train.models import Train, PrimaryTrain

class TrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'start', 'end', 'start_time', 'end_time','up', 'type', 'classes', 'frequency', 'facilities')
admin.site.register(Train, TrainAdmin)

class PrimaryTrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'start', 'end', 'start_time', 'end_time','up', 'type', 'classes', 'frequency', 'facilities')
admin.site.register(PrimaryTrain, PrimaryTrainAdmin)
