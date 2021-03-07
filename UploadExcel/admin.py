from django.contrib import admin
from .models import *
# Register your models here.
class ActionItemsAdmin(admin.ModelAdmin):
    list_display =('StudyActionNo' ,'StudyName', 'lsQueSeries','ProjectPhase', 'Cause', 'Consequence', 'Organisation', 'Disipline')
admin.site.register(UploadExl)
admin.site.register(ActionItems, ActionItemsAdmin)

