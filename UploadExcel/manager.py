from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
class QuerySet(models.QuerySet):
    def get_myActions(self,userorganisation,userdisipline,usersubdisipline,que):
        return self.filter(Organisation__icontains=userorganisation).filter(Disipline__icontains=userdisipline).filter(Subdisipline__icontains=usersubdisipline).filter(QueSeries__iexact=que)
    def get_myActionsCount(self,userorganisation,userdisipline,usersubdisipline,que):
        return self.filter(Organisation__icontains=userorganisation).filter(Disipline__icontains=userdisipline).filter(Subdisipline__icontains=usersubdisipline).filter(QueSeries__iexact=que).count ()
    def get_allActionsCount(self,workshop,que):
        return self.filter (QueSeries__iexact=que).count ()
    def get_DiscSubActionsCount(self,workshop,DiscSub,que):
        return self.filter (Disipline__icontains=DiscSub[0]).filter(Subdisipline__icontains=DiscSub[1]).filter (QueSeries__iexact=que).count ()
    def get_mgrComments(self,fkey):
        return self.filter(Action__pk=fkey)
    
    # def get_Approver1(self,userorganisation,userdisipline,usersubdisipline):
    #     return self.filter(Organisation__icontains=userorganisation).filter(Disipline__icontains=userdisipline).filter(Subdisipline__icontains=usersubdisipline)
    # def get_Approver2(self,useremail):
    #     return self.filter(Approver2__icontains=useremail)
    # def get_Approver3(self,useremail):
    #     return self.filter(Approver3__icontains=useremail)
    # def get_Approver4(self,useremail):
    #     return self.filter(Approver4__icontains=useremail)
    # def get_Approver5(self,useremail):
    #     return self.filter(Approver5__icontains=useremail)

class myActionItemManager(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def get_myItemsbyCompDisSub(self,userorganisation,userdisipline,usersubdisipline,que):
        return self.get_queryset().get_myActions(userorganisation,userdisipline,usersubdisipline,que)

class myActionCount(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def get_myItemsCount(self,userorganisation,userdisipline,usersubdisipline,que):
        return self.get_queryset().get_myActionsCount(userorganisation,userdisipline,usersubdisipline,que)

class mgrallActionCount(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def mgr_getallItemsCount(self,workshop,que):
        return self.get_queryset().get_allActionsCount(workshop,que)

class mgrgetActionDiscSubCount(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def mgr_getDiscSubItemsCount(self,workshop,DiscSub,que):
        return self.get_queryset().get_DiscSubActionsCount(workshop,DiscSub,que)


class Approver1Manager(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def get_myItemsbyCompDisSub(self,userorganisation,userdisipline,usersubdisipline):
        return self.get_queryset().get_Approver1(userorganisation,userdisipline,usersubdisipline)


class mdlCommentsManager(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def mgrCommentsbyFK(self,Fkey):
        return self.get_queryset().get_mgrComments(Fkey)

#for setting queseries, really needs improvement because we can set any attibute for it
class mdlSetQueSeries(models.Manager):
    
    def mgrsetQueSeries(self,ID, Que):
        obj = get_object_or_404(self.model, id=ID)
        obj.QueSeries = Que
        obj.save(update_fields=["QueSeries"],using=self.db)

# class Approver2Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver2(useremail)

# class Approver3Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver3(useremail)

# class Approver4Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver4(useremail)

# class Approver5Manager(models.Manager):
#     def get_queryset (self):
#         return RoutesQuerySet(self.model, using=self._db)
#     def get_myroutes(self,useremail):
#         return self.get_queryset().get_Approver5(useremail)