from django.db import models
from django.urls import reverse
from .manager import *
# Create your models here.
class UploadExl(models.Model):

    filename    = models.FileField(upload_to='excelUpload')
    uploaded    = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"filename: {self.id}"

class ActionItems(models.Model):
   
    StudyActionNo   =   models.CharField(max_length=100,null=True)
    StudyName       =   models.CharField(max_length=255,null=True)
    Facility        =   models.CharField(max_length=255,null=True)
    ProjectPhase           =   models.CharField(max_length=255,null=True)
    Cause           =   models.TextField(null=True)
    SafeG           = models.TextField(null=True)
    Consequence     =   models.TextField(null=True)
    Recomendations  =   models.TextField(null=True)
    InitialRisk     =   models.CharField(max_length=10,null=True)
    ResidualRisk    =   models.CharField(max_length=10,null=True)
    Response        =   models.TextField(null=True)
    Attachment      =   models.TextField(null=True)
    Organisation    =   models.CharField(max_length=100,null=True)
    Disipline       = models.CharField(max_length=100,null=True)
    Subdisipline    = models.CharField(max_length=100,null=True)
    FutureAction    =   models.TextField(null=True)
    DueDate         =   models.DateField(auto_now_add=True, null=True)
    QueSeries       =   models.IntegerField(null=True)
    
    myActionItems = myActionItemManager()
    myActionItemsCount = myActionCount()
    #Approver1RoItems = Approver1ItemManager()
    #Approver2RoItems = Approver2ItemManager()
 

    def get_absolute_url(self):
        return reverse("getActionsDetails", kwargs={"id": self.id})