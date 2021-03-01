from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
class RoutesQuerySet(models.QuerySet):
    def get_ActioneeR(self,useremail):
        return self.filter(Actionee__icontains=useremail)
    def get_Approver1(self,useremail):
        return self.filter(Approver1__icontains=useremail)
    def get_Approver2(self,useremail):
        return self.filter(Approver2__icontains=useremail)
    def get_Approver3(self,useremail):
        return self.filter(Approver3__icontains=useremail)
    def get_Approver4(self,useremail):
        return self.filter(Approver4__icontains=useremail)
    def get_Approver5(self,useremail):
        return self.filter(Approver5__icontains=useremail)
class ActioneeManager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_ActioneeR(useremail)

class Approver1Manager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_Approver1(useremail)

class Approver2Manager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_Approver2(useremail)

class Approver3Manager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_Approver3(useremail)

class Approver4Manager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_Approver4(useremail)

class Approver5Manager(models.Manager):
    def get_queryset (self):
        return RoutesQuerySet(self.model, using=self._db)
    def get_myroutes(self,useremail):
        return self.get_queryset().get_Approver5(useremail)