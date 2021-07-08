from django.contrib import admin
from .models import *
from django.contrib.admin.forms import AuthenticationForm

# Register your models here.
class ActionItemsAdmin(admin.ModelAdmin):
    list_display =('StudyActionNo' ,'DueDate','StudyName', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)
    list_editable = ('DueDate',)



class delegatedadmin(admin.AdminSite):
    
    site_header = 'Delegated Admin'
    list_display =('StudyActionNo' ,'DueDate','StudyName', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)
    list_editable = ('DueDate',)

    login_form = AuthenticationForm
    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.is_active

class delegatedActionItemsAdmin(admin.ModelAdmin):
    
    list_display =('StudyActionNo' ,'DueDate','StudyName', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)
    list_editable = ('DueDate',)

    

    def has_add_permission(self, request):
        return True

delegatedadmin_site=delegatedadmin(name='DelegatedAdmin')

delegatedadmin_site.register(ActionItems,delegatedActionItemsAdmin)

admin.site.register(UploadExl)
admin.site.register(ActionItems, ActionItemsAdmin)
admin.site.register(Comments)

admin.site.register(Attachments)