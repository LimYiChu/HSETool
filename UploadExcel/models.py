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
    Recomendations  =   models.TextField(null=True,blank=True)
    InitialRisk     =   models.CharField(max_length=10,null=True,blank=True)
    ResidualRisk    =   models.CharField(max_length=10,null=True,blank=True)
    Response        =   models.TextField(null=True,blank=True)
    Attachment      =   models.TextField(null=True,blank=True)
    Organisation    =   models.CharField(max_length=100,null=True,blank=True)
    Disipline       = models.CharField(max_length=100,null=True,blank=True)
    Subdisipline    = models.CharField(max_length=100,null=True,blank=True)
    FutureAction    =   models.TextField(null=True,blank=True)
    DueDate         =   models.DateField(auto_now_add=True, null=True,blank=True)
    QueSeries       =   models.IntegerField(null=True,blank=True)
    objects = models.Manager()
    myActionItems = myActionItemManager()
    myActionItemsCount = myActionCount()
    #Approver1RoItems = Approver1ItemManager()
    #Approver2RoItems = Approver2ItemManager()
 

    def get_absolute_url(self):
        return reverse("getActionsDetails", kwargs={"id": self.id})

    def __str__(self): 
        return self.StudyActionNo   
