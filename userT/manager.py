from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
class RoutesQuerySet(models.QuerySet):
    def get_ActioneeR(self,useremail):
        return self.filter(Actionee__icontains=useremail)
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

    def get_mgrgetCompany(self):
        allRoutes =self.filter()
        Company = []
        for items in allRoutes:
            Company.append(items.Organisation)

        return list(set(Company)) #- Returns non Duplicate values
    
    def mgrgetActApp(self,DiscSub):
        return self.filter (Disipline__icontains=DiscSub[0]).filter(Subdisipline__icontains=DiscSub[1])

class ActioneeManager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_ActioneeR(useremail)

class ApproverManager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail,ApproverLevel):
        lookup = 'Approver'+str(ApproverLevel)+'__icontains'
        return self.get_queryset().get_Approver(useremail,lookup)

class mgrgetDiscSub (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getDiscSub(self):
        return self.get_queryset().get_AllDiscSub()

class mgrgetCompany (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getCompanyCount(self):
        return self.get_queryset().get_mgrgetCompany()

class mgrActioneeApprover (models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def mgr_getActApp(self,DiscSub):
        return self.get_queryset().mgrgetActApp(DiscSub)
# class Approver2Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver2(useremail)

