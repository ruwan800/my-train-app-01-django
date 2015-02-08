from django.contrib import admin
from process.models import Process, Stage, Progress

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'last_run')
admin.site.register(Process, ProcessAdmin)

class StageAdmin(admin.ModelAdmin):
    list_display = ('id', 'process', 'index', 'stage_message','stage_function_module', 'stage_function_file', 'stage_function_name')
admin.site.register(Stage, StageAdmin)

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'process', 'stage', 'progress', 'complete', 'break_stage', 'break_point')
admin.site.register(Progress, ProgressAdmin)