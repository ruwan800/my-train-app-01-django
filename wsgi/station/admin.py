from django.contrib import admin
from django.conf.urls import patterns
from django.core import urlresolvers
from station.models import Station, Line, LinePath

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'line', 'code', 'number','pos')
admin.site.register(Station, StationAdmin)

class LineAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'begin', 'end', 'name', 'code')
admin.site.register(Line, LineAdmin)

class LPAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'in_use', 'priority')
admin.site.register(LinePath, LPAdmin)


def accept_changes(modeladmin, request, queryset):
    queryset.update(status='p')
accept_changes.short_description = "Apply suggested changes."

class TempStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'line', 'code')
    actions = [accept_changes]

    #change the default behavior of change view.
    change_form_template = 'admin/submit_row.html'
    def change_view(self, request, object_id):
        return super(TempStationAdmin, self).change_view(request, object_id)

    #new view toget params manually and save in station table
    def update_change(self, request):
        #TODO get params manually and save in station table
        return super(TempStationAdmin, self).changelist_view(request)

    #append new view to existing admin urls
    def get_urls(self):
        urls = super(TempStationAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^update_change/$', self.update_change)
        )
        return my_urls + urls

