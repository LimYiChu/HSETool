from django.db import models
from django.urls import reverse
from .manager import *
# Create your models here.
class UploadExl(models.Model):

    Filename            =   models.FileField(upload_to='excelUpload')
    DateAdded            =   models.DateTimeField(auto_now_add=True)
    Username = models.CharField(max_length=255,null=True,blank=True)
    objects = models.Manager()
    def __str__(self):
        return '%s ---%s' %(self.Filename, self.Username)

class ActionItems(models.Model):
   
    StudyActionNo   =   models.CharField(max_length=100,null=True,blank=True)
    StudyName       =   models.CharField(max_length=255,null=True,blank=True)
    Facility        =   models.CharField(max_length=255,null=True,blank=True)
    ProjectPhase           =   models.CharField(max_length=255,null=True,blank=True)
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
    
    DueDate         =   models.DateField(auto_now_add=True, null=True,blank=True)
    QueSeries       =   models.IntegerField(blank=True,null=True,default=0) #try to make the queseries value default to 0 when not included in the templated uploaded.
    QueSeriesTarget =   models.IntegerField(blank=True,null=True,default=0)
    Guidewords      =  models.TextField(null=True,blank=True)
    objects = models.Manager()
    myActionItems = myActionItemManager()
    myActionItemsCount = myActionCount()
    mdlallActionItemsCount = mgrallActionCount()
    mdlQueSeries = mdlSetQueSeries()
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

class Comments (models.Model):
    Action = models.ForeignKey(ActionItems, on_delete=models.SET_NULL,related_name="comments",null=True)
    Username = models.CharField(max_length=255,null=True,blank=True)
    Reason = models.TextField(null=True,blank=True)
    DateAdded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    mdlComments = mdlCommentsManager()
    
    class Meta:
       verbose_name_plural = "Comments"

    def __str__(self): 
       return '%s ---%s' %(self.Action.StudyActionNo, self.Username) #if someone delete all Actions before Attachments, come here to fix

class Attachments (models.Model):
    Action = models.ForeignKey(ActionItems, on_delete=models.SET_NULL,null=True) #cant have related name as it throws a spanner in the works
    Username = models.CharField(max_length=255,null=True,blank=True)
    Attachment      =   models.FileField(upload_to='excelUpload',null=True,blank=True)
    DateAdded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    mdlDeleteAttachment = mgrDeleteAttachment()
    class Meta:
       verbose_name_plural = "Attachments"

    def __str__(self): 
       return '%s---%s' %(self.Action.StudyActionNo, self.Username)