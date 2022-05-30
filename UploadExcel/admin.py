from django.contrib import admin

from userT.models import Studies
from .models import *
from django.contrib.admin.forms import AuthenticationForm
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
class ActionItemsAdmin(admin.ModelAdmin):
    list_display =('StudyActionNo' ,'DueDate','StudyName','ProjectPhase', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)
    list_editable = ('DueDate','StudyName','ProjectPhase')
    search_fields =('StudyActionNo' , 'DueDate', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)


class delegatedadmin(admin.AdminSite):
    
    site_header = 'Delegated Admin'
   
    login_form = AuthenticationForm
    # The below just gives 
    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.is_active

class delegatedActionItemsAdmin(admin.ModelAdmin):
    
    list_display =('StudyActionNo' ,'DueDate','StudyName', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',)
    list_editable = ('DueDate',)

    allfields = [f.name for f in ActionItems._meta.get_fields()]

    
    del allfields[0:2] #the first few items are foreign keys under meta function so gotta delete it
    #readonly_fields=['StudyActionNo','StudyName', 'Recommendations', 'Response','Organisation', 'Disipline','Subdisipline','DateCreated','QueSeries',]
    readonly_fields = allfields
   

    # def has_add_permission(self, request):
    #     return True

    # def has_change_permission(self, request,obj=None) :
        
    #     # if obj:
    #     #     if obj.DueDate == "A":
    #     #          return request.user.has_perm('DeptA')
    #     #     elif obj.dept == "B":
    #     #          return request.user.has_perm('DeptB')
        
    #     return False
        #super().has_change_permission(request, obj=obj)

class delegatedStudiesAdmin(admin.ModelAdmin):

    list_display =('StudyName' ,'ProjectPhase','AttendanceList', )
    #list_display_links = ('StudyName',)
    #list_editable = ('StudyName',)

    readonly_fields = ('ProjectPhase','AttendanceList')

delegatedadmin_site=delegatedadmin(name='Delegated Admin')
#Since need to modify the view on action items have to do another admin.ModelAdmin to get a more appropriate views
#This model.admon overrides functions etc on it
delegatedadmin_site.register(ActionItems,delegatedActionItemsAdmin) 
delegatedadmin_site.register(Studies,delegatedStudiesAdmin)

admin.site.register(UploadExl)
admin.site.register(ActionItems, ActionItemsAdmin)
admin.site.register(Comments)

admin.site.register(Attachments)
