from django.db import models
from django.urls import reverse
from .manager import *
# Create your models here.
class UploadExl(models.Model):

    filename            =   models.FileField(upload_to='excelUpload')
    uploaded            =   models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"filename: {self.id}"

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
    QueSeries       =   models.IntegerField(default=0,blank=True) #try to make the queseries value default to 0 when not included in the templated uploaded.
    objects = models.Manager()
    myActionItems = myActionItemManager()
    myActionItemsCount = myActionCount()
    mdlQueSeries = mdlSetQueSeries()
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
       return '%s ---%s' %(self.Action.StudyActionNo, self.Username)

class Attachments (models.Model):
    Action = models.ForeignKey(ActionItems, on_delete=models.SET_NULL,null=True) #cant have related name as it throws a spanner in the works
    Username = models.CharField(max_length=255,null=True,blank=True)
    Attachment      =   models.FileField(upload_to='excelUpload',null=True,blank=True)
    DateAdded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    class Meta:
       verbose_name_plural = "Attachments"

    def __str__(self): 
       return '%s---%s' %(self.Action.StudyActionNo, self.Username)