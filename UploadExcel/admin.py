from django.contrib import admin
from .models import *
# Register your models here.
class ActionItemsAdmin(admin.ModelAdmin):
    list_display =('StudyActionNo' ,'StudyName', 'QueSeries','ProjectPhase', 'Cause', 'Consequence', 'Organisation', 'Disipline','DateCreated')
admin.site.register(UploadExl)
admin.site.register(ActionItems, ActionItemsAdmin)
admin.site.register(Comments)

admin.site.register(Attachments)