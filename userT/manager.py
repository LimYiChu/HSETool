from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
class RoutesQuerySet(models.QuerySet):
    def get_ActioneeR(self,useremail):
        return self.filter(Actionee__icontains=useremail)
    def get_Approver(self,useremail,lookup):
        return self.filter(**{lookup: useremail})
    
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

# class Approver2Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver2(useremail)

