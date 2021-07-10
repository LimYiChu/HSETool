from django.contrib import admin
from .models import *
# Register your models here.
class ActionItemsAdmin(admin.ModelAdmin):
    list_display =('StudyActionNo' ,'DueDate','StudyName', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)
    list_editable = ('DueDate','StudyName',)

admin.site.register(UploadExl)
admin.site.register(ActionItems, ActionItemsAdmin)
admin.site.register(Comments)

admin.site.register(Attachments)