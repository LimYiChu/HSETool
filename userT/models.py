from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.db.models import Q
from .manager import *
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .manager import *
from UploadExcel.manager import *
#user= settings.AUTH_USER_MODEL
from UploadExcel.models import *
from simple_history.models import HistoricalRecords

from django.contrib.auth.models import ( 
    AbstractBaseUser, BaseUserManager
     )
# Create your models here.(
class UserManager(BaseUserManager):
    def create_user(self, email,password,**extra_fields):
        if not email:
            raise ValueError("users must have an email account")
       
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

         # normalUser   = self.model (
        #             email= self.normalize_email(email),
        #             fullname = fullname,
        #             disipline = disipline,

        # )
        
        # normalUser.set_password(password)
        # normalUser.save(using=self._db)
        # return normalUser
    
    def create_superuser(self, email,password, **extra_fields):
        
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        superuser = self.create_user(
                email,
                password=password,
                **extra_fields
        )
        return superuser
        #Superuser.fullname  =   fullname
        #Superuser.disipline =   disipline
        #Superuser.set_password (password)
        # Superuser.admin  = True
        # Superuser.staff  = True
        # Superuser.is_superuser  =   True
        # Superuser.save(using=self._db)
       

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email       =   models.EmailField(max_length=254, unique=True)
    fullname   =   models.CharField(max_length=254, blank=True,null=True)
    disipline   =   models.CharField(max_length=254, blank=True, null=True)
    subdisipline    =  models.CharField(max_length=254, blank=True, null=True) 
    organisation   =   models.CharField(max_length=254, blank=True, null=True)
    designation     =    models.CharField(max_length=254, blank=True, null=True)
    licensing     =    models.CharField(max_length=254, blank=True, null=True)
    signature = models.CharField(max_length=100, blank=True, null=True)
    expiration     =  models.DateTimeField(null=True) 
    is_active = models.BooleanField(default=True) #according to django contrib doc, is_active returned here
    admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(blank=True,null=True,default=True)
    staff = models.BooleanField(default=True)
    
    objects =   UserManager()
    mdlSetGetField = mgrSetGetfields()
    USERNAME_FIELD =   'email'
    REQUIRED_FIELDS =   []

    #objects = CustomUserManager()

    def __str__(self):
        return self.email

    #Dont delete its an example of what not to do
    # def has_perm(self, perm, obj=None):
    # #     "Does the user have a specific permission?"
    # #     # Simplest possible answer: Yes, always
    #     #return self.is_admin
    #     return True

    # def has_module_perms(self, app_label):
    # #     #"Does the user have permissions to view the app `app_label`?"
    # #     # Simplest possible answer: Yes, always
    #     retn True
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         #self.type = self.default_type
    #         self.type.append(self.default_type)
    #     return super().save(*args, **kwargs)

    

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname
    @property
    def is_staff(self):
        return self.staff

    def is_admin(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.admin

    #def is_active(self): #after referring to django contrib docs, this does not work
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
    #    return self.active

    #To delete Below so that user
    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     #"Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True
#changed active to is_active
class Phases (models.Model):
    ProjectPhase = models.CharField(max_length=200, null=True)
    Scheduled = models.CharField(max_length=200, null=True)
    Description  = models.CharField(max_length=1000, null=True)
    Default = models.BooleanField(default=False)
    objects = models.Manager()
    mdlSetGetField = mgrGeneralGetSetfields()
   

    class Meta:
       verbose_name_plural = "Phases" 

    def __str__(self): 
       return '%s' %(self.ProjectPhase)

class Studies (models.Model):
    StudyName = models.CharField(max_length=200, null=True)
    ProjectPhase_backup = models.CharField(max_length=200, null=True,blank=True)
    AttendanceList  = models.CharField(max_length=200, null=True,blank=True)
    DateConducted = models.DateField(auto_now_add=True,null=True,blank=True)
    Form = models.CharField(max_length=100, null=True,blank=True)
    ProjectPhase =   models.ForeignKey(Phases, on_delete=models.SET_NULL,null=True,blank=True)
    Sendemail = models.BooleanField(default=True)
    
    class Meta:
       verbose_name_plural = "Studies" #this if not done gives a view of Studiess in admin panel
    
    objects = models.Manager()
    mdlallStudies = mgrallActionCount()

    def __str__(self): 
       return '%s -- %s' %(self.StudyName, self.ProjectPhase)

class Parameters (models.Model):
    Versioning = models.CharField(max_length=200, null=True)
    Emailactionee = models.CharField(max_length=200, null=True,blank=True)
    Emailapprover = models.CharField(max_length=200, null=True,blank=True)
    Emailfrequency = models.CharField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Parameters" #this if not done gives a view of Studiess in admin panel
    
    objects = models.Manager()
   
    def __str__(self): 
       return '%s' %(self.Versioning)

class RiskMatrix (models.Model):
    Consequence = models.CharField(max_length=20, null=True,blank=True)
    ConsequenceCategory = models.CharField(max_length=100, null=True,blank=True)
    Likelihood = models.CharField(max_length=20, null=True,blank=True)
    LikelihoodCategory = models.CharField(max_length=100, null=True,blank=True)
    Combined  = models.CharField(max_length=100, null=True,blank=True)
    Ranking = models.CharField(max_length=100, null=True,blank=True)
    RiskColour = models.CharField(max_length=100, null=True,blank=True)
    
   
    objects = models.Manager()
    class Meta:
       verbose_name_plural = "RiskMatrix" #this if not done gives a view of ss

    def __str__(self): 
       return '%s ---%s' %(self.Combined, self.Ranking)

class ActionRoutes(models.Model):
    

    Organisation    = models.CharField(max_length=100, null=True)
    Disipline       = models.CharField(max_length=100, null=True)
    Subdisipline    = models.CharField(max_length=100, null=True)
    Studies         = models.ForeignKey(Studies, on_delete=models.SET_NULL,related_name="comments",null=True,blank=True)
    Actionee        =   models.CharField(max_length=100, null=True)
    Approver1        =  models.CharField(max_length=100, null=True, blank=True)
    Approver2       =   models.CharField(max_length=100, null=True,blank=True)
    Approver3       =   models.CharField(max_length=100, null=True,blank=True)
    Approver4       =   models.CharField(max_length=100, null=True, blank=True)
    Approver5       =   models.CharField(max_length=100, null=True,blank=True)
    Approver6       =   models.CharField(max_length=100, null=True,blank=True)
    Approver7       =   models.CharField(max_length=100, null=True,blank=True)
    Approver8       =   models.CharField(max_length=100, null=True,blank=True)
    ProjectPhase =   models.ForeignKey(Phases, on_delete=models.SET_NULL,null=True,blank=True)
    
    history = HistoricalRecords()
    objects = models.Manager()
    ActioneeRo = ActioneeManager()
    ApproverRo = ApproverManager()
    mdlAllDiscSub  = mgrgetDiscSub()
    mdlAllCompany = mgrgetCompany()
    mdlgetActioneeAppr = mgrActioneeApprover()
    mdlgetApproverLevel = mmgrgetApproverLevel()
    class Meta:
       verbose_name_plural = "ActionRoutes" #this if not done gives a view of Studiess

    def __str__(self): 
       return '%s--%s--%s' %(self.Organisation, self.Disipline, self.Subdisipline)

class Menus (models.Model) :

    Urlhref = models.CharField(max_length=200, null=True,blank=True)
    Icon = models.CharField(max_length=200, null=True,blank=True)
    Namemenu = models.CharField(max_length=200, null=True,blank=True)
    Parentid = models.IntegerField(null=True,blank=True)
    Permissioning = models.CharField(max_length=200, null=True,blank=True)
    Classelement = models.JSONField(max_length=200, null=True,blank=True)
    Hierarchy = models.IntegerField(null=True,blank=True)
   
    def __str__(self): 
        return '%s--%s--%s' %(self.Urlhref, self.Namemenu, self.Parentid)
    class Meta:
       verbose_name_plural = "Menus"

