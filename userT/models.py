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
        )
        normalUser.fullname = fullname
        normalUser.disipline = disipline
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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects =   UserManager()
    USERNAME_FIELD =   'email'
    REQUIRED_FIELDS =   ['fullname','disipline']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class ActionRoutes(models.Model):
    

    Organisation    = models.CharField(max_length=100, null=True)
    Disipline       = models.CharField(max_length=100, null=True)
    Subdisipline    = models.CharField(max_length=100, null=True)
    Actionee        =   models.CharField(max_length=100, null=True)
    Approver1        =  models.CharField(max_length=100, null=True)
    Approver2       =   models.CharField(max_length=100, null=True)
    Approver3       =   models.CharField(max_length=100, null=True)
    Approver4       =   models.CharField(max_length=100, null=True)
    Approver5       =   models.CharField(max_length=100, null=True)

    ActioneeRo = ActioneeManager()
    ApproverRo = ApproverManager()
    # Approver2Ro = Approver2Manager()
    
   # Actionee        = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL, related_name='Actionee')
    #Approver1       = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL, related_name='Approver1')
    #Approver2       = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL, related_name='Approver2')
    #Approver3       = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL, related_name='Approver3')
    #Approver4       = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL, related_name='Approver4')
    #Approver5       = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL, related_name='Approver5')


