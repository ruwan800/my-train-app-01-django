from django.contrib import admin
from update.models import Update, Insert, Conflict, Delete

class UpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewed', 'time', 'trace', 'cat1', 'cat2', 'value', 'old', 'new')
admin.site.register(Update, UpdateAdmin)

class ConflictAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewed', 'resolved', 'time', 'trace', 'cat', 'value')
admin.site.register(Conflict, ConflictAdmin)

class InsertAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewed', 'time', 'trace', 'cat', 'value')
admin.site.register(Insert, InsertAdmin)

class DeleteAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewed', 'time', 'trace', 'cat', 'value')
admin.site.register(Delete, DeleteAdmin)