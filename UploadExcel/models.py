from urllib import request
from django.db import models
from django.urls import reverse
from django.utils.tree import Node
from .manager import *
from simple_history.models import HistoricalRecords
from datetime import datetime
from userT.models import *
# Create your models here.
class UploadExl(models.Model):

    Filename            =   models.FileField(upload_to='excelUpload',max_length=500)
    DateAdded            =   models.DateTimeField(auto_now_add=True)
    Username = models.CharField(max_length=255,null=True,blank=True)
    objects = models.Manager()
    def __str__(self):
        return '%s ---%s' %(self.Filename, self.Username)

class ActionItems(models.Model):
   
    StudyActionNo   =   models.CharField(max_length=100,null=True,blank=True)
    # StudyName_backup       =   models.CharField(max_length=255,null=True,blank=True)
    # StudyName       =   models.ForeignKey(Studies, on_delete=models.SET_NULL,null=True,blank=True) 
    StudyName_backup      =   models.CharField(max_length=255,null=True,blank=True)
    StudyName       =   models.ForeignKey(Studies, on_delete=models.SET_NULL,null=True,blank=True) 
    Facility       =   models.CharField(max_length=255,null=True,blank=True)
   

    # ProjectPhase_backup         =   models.CharField(max_length=255,null=True,blank=True)
    # ProjectPhase       =   models.ForeignKey(Phases, on_delete=models.SET_NULL,null=True,blank=True)
    ProjectPhase_backup         =   models.CharField(max_length=255,null=True,blank=True)
    ProjectPhase =   models.ForeignKey(Phases, on_delete=models.SET_NULL,null=True,blank=True)

    Cause           =   models.TextField(null=True,blank=True)
    Safeguard           = models.TextField(null=True,blank=True)
    Consequence     =   models.TextField(null=True,blank=True)
    Recommendations  =   models.TextField(null=True,blank=True)
    InitialRisk     =   models.CharField(max_length=10,null=True,blank=True)
    ResidualRisk    =   models.CharField(max_length=10,null=True,blank=True)
    Response        =   models.TextField(null=True,blank=True)
    
    Organisation    =   models.CharField(max_length=100,null=True,blank=True)
    Disipline       = models.CharField(max_length=100,null=True,blank=True)
    Subdisipline    = models.CharField(max_length=100,null=True,blank=True)
    FutureAction    =   models.TextField(null=True,blank=True)
    
    DueDate         =   models.DateField(null=True,blank=True)
    QueSeries       =   models.IntegerField(blank=True,null=True,default=0) #try to make the queseries value default to 0 when not included in the templated uploaded.
    QueSeriesTarget =   models.IntegerField(blank=True,null=True,default=0)
    Guidewords      =  models.TextField(null=True,blank=True)
    Deviation       =  models.TextField(null=True,blank=True)
    Revision        =   models.IntegerField(blank=True,null=True,default=0)
    DateCreated     =  models.DateField(auto_now_add=True, null=True,blank=True)

    #20211223 edward Hazid fields
    NodeNo = models.IntegerField(blank=True,null=True,default=0)
    NodeDescription = models.TextField(null=True,blank=True)
    PreventiveSafeguard = models.TextField(null=True,blank=True)
    MitigativeSafeguard = models.TextField(null=True,blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['QueSeries', 'Organisation','Disipline','Subdisipline'])]

    history = HistoricalRecords()
    objects = models.Manager()
    myActionItems = myActionItemManager()
    myActionItemsCount = myActionCount()

   
    mdlallActionItemsCount = mgrallActionCount()
    mdlQueSeries = mdlGetSetQueRevision()
    mdlSetField = mgrSetfields()
    mdlgetField = mgrgetfields()
    mdlgetActionDiscSubCount = mgrgetActionDiscSubCount()
    mdlgetActionCompanyCount = mgrgetActionCompanyCount()
    
    #Approver1RoItems = Approver1ItemManager()
    #Approver2RoItems = Approver2ItemManager()
 

    def get_absolute_url(self):
        return reverse("DetailsForm", kwargs={"id": self.id})
        
    def __str__(self): 
        return self.StudyActionNo  


    def save(self, *args, **kwargs):

        # useremail = HistoricalRecords.thread.request.user
        # objuser  = CustomUser.objects.get (email = useremail)   
        userurl = HistoricalRecords.thread.request.path
        urllowercase = userurl.casefold()
        if "admin/uploadexcel/" in urllowercase:
            self.skip_history_when_saving = True
            super(ActionItems, self).save(*args, **kwargs)

        else:
            super(ActionItems, self).save(*args, **kwargs)


class Comments (models.Model):
    Action = models.ForeignKey(ActionItems, on_delete=models.SET_NULL,null=True) #edward-> removed related name 
    Username = models.CharField(max_length=255,null=True,blank=True)
    Reason = models.TextField(null=True,blank=True)
    Attachment      =   models.FileField(upload_to='comments',null=True,blank=True,max_length=500)
    DateAdded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    mdlComments = mdlCommentsManager()
    
    class Meta:
       verbose_name_plural = "Comments"

    def __str__(self): 
       return '%s ---%s' %(self.Action.StudyActionNo, self.Username) #if someone delete all Actions before Attachments, come here to fix

class Attachments (models.Model):
    Action = models.ForeignKey(ActionItems, on_delete=models.SET_NULL,null=True) #cant have related name as it throws a spanner in the works, edward-anything that has foreignkey here comes up in tables with _id, 
    Username = models.CharField(max_length=255,null=True,blank=True)
    Attachment      =   models.FileField(upload_to='attachments',null=True,blank=True,max_length=500)
    DateAdded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    mdlDeleteAttachment = mgrDeleteAttachment()
    class Meta:
       verbose_name_plural = "Attachments"

    def __str__(self): 
       return '%s---%s' %(self.Action.StudyActionNo, self.Username)