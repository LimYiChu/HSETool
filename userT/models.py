from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.db.models import Q
from .manager import *
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .manager import *
#user= settings.AUTH_USER_MODEL

from django.contrib.auth.models import ( 
    AbstractBaseUser, BaseUserManager
     )
# Create your models here.(
class UserManager(BaseUserManager):
    def create_user(self, email,password,**extra_fields):
        if not email:
            raise ValueError("users must have an email account")
        # normalUser   = self.model (
        #             email= self.normalize_email(email),
        #             fullname = fullname,
        #             disipline = disipline,

        # )
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

        # normalUser.set_password(password)
        # normalUser.save(using=self._db)
        # return normalUser
    
    def create_superuser(self, email,password, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        Superuser=self.create_user(
                email,
                password=password,
                **extra_fields
        )
        #Superuser.fullname  =   fullname
        #Superuser.disipline =   disipline
        #Superuser.set_password (password)
        Superuser.admin  = True
        Superuser.staff  = True
        Superuser.is_superuser  =   True
        Superuser.save(using=self._db)
        return Superuser

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email       =   models.EmailField(max_length=254, unique=True)
    fullname   =   models.CharField(max_length=254, blank=True,null=True)
    disipline   =   models.CharField(max_length=254, blank=True, null=True)
    subdisipline    =  models.CharField(max_length=254, blank=True, null=True) 
    organisation   =   models.CharField(max_length=254, blank=True, null=True)
    designation     =    models.CharField(max_length=254, blank=True, null=True)
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

    # def has_perm(self, perm, obj=None):
    # #     "Does the user have a specific permission?"
    # #     # Simplest possible answer: Yes, always
    #     #return self.is_admin
    #     return True

    # def has_module_perms(self, app_label):
    # #     #"Does the user have permissions to view the app `app_label`?"
    # #     # Simplest possible answer: Yes, always
    #     return True
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