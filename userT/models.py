from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from .manager import *
from django.conf import settings
#user= settings.AUTH_USER_MODEL

from django.contrib.auth.models import ( 
    AbstractBaseUser, BaseUserManager
     )
# Create your models here.(
class UserManager(BaseUserManager):
    def create_user(self, email,fullname,disipline,password=None):
        if not email:
            raise ValueError("users must have an email account")
        normalUser   = self.model (
                    email= self.normalize_email(email),
                    fullname = fullname,
                    disipline = disipline,

        )
        
        normalUser.set_password(password)
        normalUser.save(using=self._db)
        return normalUser
    
    def create_superuser(self, email,fullname,disipline,password=None):
        Superuser=self.create_user(
                email,
                fullname,
                disipline,
                password=password,
        )
        #Superuser.fullname  =   fullname
        #Superuser.disipline =   disipline
        #Superuser.set_password (password)
        Superuser.is_admin  = True
        #Superuser.is_staff  =   True
        Superuser.save(using=self._db)
        return Superuser

class CustomUser(AbstractBaseUser):
    email       =   models.EmailField(max_length=254, unique=True)
    fullname   =   models.CharField(max_length=254, null=True)
    disipline   =   models.CharField(max_length=254, blank=True, null=True)
    subdisipline    =  models.CharField(max_length=254, blank=True, null=True) 
    organisation   =   models.CharField(max_length=254, blank=True, null=True)
    designation     =    models.CharField(max_length=254, blank=True, null=True)
    expiration     =  models.DateTimeField(null=True) 
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=True)
    objects =   UserManager()
    USERNAME_FIELD =   'email'
    REQUIRED_FIELDS =   ['fullname','disipline']

    def __str__(self):
        return self.email

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

    def is_active(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.active

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Studies (models.Model):
    StudyName = models.CharField(max_length=200, null=True)
    ProjectPhase = models.CharField(max_length=200, null=True)
    AttendanceList  = models.CharField(max_length=1000, null=True)
    DateConducted = models.DateField(auto_now_add=True,null=True)
    objects = models.Manager()
    class Meta:
       verbose_name_plural = "Studies" #this if not done gives a view of Studiess

    def __str__(self): 
       return '%s ---%s' %(self.StudyName, self.ProjectPhase)

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