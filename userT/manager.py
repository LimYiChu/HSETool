from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class RoutesQuerySet(models.QuerySet):
    def get_ActioneeR(self,useremail):
        return self.filter(Actionee__iexact=useremail)
    def get_Approver(self,useremail,lookup):
        return self.filter(**{lookup: useremail})
    def get_AllDiscSub(self):
        DiscSub=[]
        listoflist =[[]]
        allRoutes = self.filter()
        
        for items in allRoutes:
            DiscSub.append(items.Disipline)
            DiscSub.append(items.Subdisipline)
         
            listoflist.append(DiscSub)
            DiscSub=[]
        
        finallistoflist = [x for x in listoflist if x] #strip of the first blank, the append into initiliased list of list creates a blank at the start
        return finallistoflist
    
    def get_AllDiscSubOrg(self):
        DiscSubOrg=[]
        listoflist =[]
        allRoutes = self.filter()
        
        for items in allRoutes:
            DiscSubOrg.append(items.Disipline)
            DiscSubOrg.append(items.Subdisipline)
            DiscSubOrg.append(items.Organisation)
            listoflist.append(DiscSubOrg)
            DiscSubOrg=[]
        
        finallistoflist = [x for x in listoflist if x] #strip of the first blank, the append into initiliased list of list creates a blank at the start
        return finallistoflist
    def get_mgrgetCompany(self):
        allRoutes =self.filter()
        Company = []
        for items in allRoutes:
            Company.append(items.Organisation)

        return list(set(Company)) #- Returns non Duplicate values

    #edward changed icontains for Disipline to iexact on 20210630
    def mgrgetActApp(self,DiscSub):
        return self.filter (Disipline__iexact=DiscSub[0]).filter(Subdisipline__icontains=DiscSub[1])
    def mgrgetApprLevel(self,CompDiscSub):
        return self.filter (Disipline__iexact=CompDiscSub[0]).filter(Subdisipline__icontains=CompDiscSub[1]).filter(Organisation__icontains=CompDiscSub[2])
    def mgrgetactioneefromtriplet(self,DiscSubOrg):
        return self.filter (Disipline__iexact=DiscSubOrg[0]).filter(Subdisipline__icontains=DiscSubOrg[1]).filter(Organisation__icontains=DiscSubOrg[2]).values('Actionee')

class UserQuerySet(models.QuerySet):
    
    def set_field(self,EMAILID, fields, value):
        
        return self.filter (email=EMAILID).update (**{fields: value})
    def get_field(self,EMAIL, fields):
                
        return self.filter (email=EMAIL).values(fields)
class ActioneeManager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_ActioneeR(useremail)

class ApproverManager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail,ApproverLevel):
        lookup = 'Approver'+str(ApproverLevel)+'__iexact'
        return self.get_queryset().get_Approver(useremail,lookup)

class mgrgetDiscSub (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getDiscSub(self):
        return self.get_queryset().get_AllDiscSub()
    def mgr_getDiscSubOrg(self):
        return self.get_queryset().get_AllDiscSubOrg()

class mgrgetCompany (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getOrgnames(self):
        return self.get_queryset().get_mgrgetCompany()

class mgrActioneeApprover (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getActApp(self,DiscSub):
        return self.get_queryset().mgrgetActApp(DiscSub)
    def mgr_getactioneefromtriplet(self,DiscSubOrg):
        return self.get_queryset().mgrgetactioneefromtriplet(DiscSubOrg)
class mmgrgetApproverLevel (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getApproverLevel(self,CompDiscSub):
        return self.get_queryset().mgrgetApprLevel(CompDiscSub)


class mgrSetGetfields(models.Manager):
    def get_queryset (self):
         return UserQuerySet(self.model, using=self._db)
    def mgrSetField(self,email, fields, value):
         #lookup = str(fields)+'__icontains' - This is how you search dynamically but since we are setting it
         return self.get_queryset().set_field(email, fields, value)
    def mgrGetField(self,email, fields):
         #lookup = str(fields)+'__icontains' - This is how you search dynamically but since we are setting it
         return self.get_queryset().get_field(email, fields)
# class Approver2Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver2(useremail)

