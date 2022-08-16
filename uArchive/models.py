from django.db import models

# Create your models here.

class PhasesArch (models.Model):
    ProjectPhase = models.CharField(max_length=200, null=True)
    Scheduled = models.CharField(max_length=200, null=True)
    DescriptionX  = models.CharField(max_length=1000, null=True)
    DefaultX = models.BooleanField(default=False)
    objects = models.Manager()
   

    class Meta:
       verbose_name_plural = "Phases" 

    def __str__(self): 
       return '%s' %(self.ProjectPhase)

class StudiesArch (models.Model):
    StudyName = models.CharField(max_length=200, null=True)
    ProjectPhase_backup = models.CharField(max_length=200, null=True,blank=True)
    AttendanceList  = models.CharField(max_length=200, null=True,blank=True)
    DateConducted = models.DateField(auto_now_add=True,null=True,blank=True)
    Form = models.CharField(max_length=100, null=True,blank=True)
    ProjectPhase =   models.ForeignKey(PhasesArch, on_delete=models.SET_NULL,null=True,blank=True)
    Sendemail = models.BooleanField(default=True)

class ActionItemsArch(models.Model):
   
    StudyActionNo   =   models.CharField(max_length=100,null=True,blank=True)
    StudyName_backup      =   models.CharField(max_length=255,null=True,blank=True)
    StudyName       =   models.ForeignKey(StudiesArch, on_delete=models.SET_NULL,null=True,blank=True) 
    Facility       =   models.CharField(max_length=255,null=True,blank=True)
    ProjectPhase_backup         =   models.CharField(max_length=255,null=True,blank=True)
    ProjectPhase =   models.ForeignKey(PhasesArch, on_delete=models.SET_NULL,null=True,blank=True)
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
    NodeNo = models.IntegerField(blank=True,null=True,default=0)
    NodeDescription = models.TextField(null=True,blank=True)
    PreventiveSafeguard = models.TextField(null=True,blank=True) 
    MitigativeSafeguard = models.TextField(null=True,blank=True)

    Signatory = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['QueSeries', 'Organisation','Disipline','Subdisipline'])]


class AttachmentsArch (models.Model):
    Action = models.ForeignKey(ActionItemsArch, on_delete=models.SET_NULL,null=True) #cant have related name as it throws a spanner in the works, edward-anything that has foreignkey here comes up in tables with _id, 
    Username = models.CharField(max_length=255,null=True,blank=True)
    Attachment      =   models.FileField(upload_to='attachments',null=True,blank=True,max_length=500)
    DateAdded = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
   
    class Meta:
       verbose_name_plural = "Attachments"

    def __str__(self): 
       return '%s---%s' %(self.Action.StudyActionNo, self.Username)