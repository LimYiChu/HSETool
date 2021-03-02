from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
class QuerySet(models.QuerySet):
    def get_myActions(self,userorganisation,userdisipline,usersubdisipline):
        return self.filter(Organisation__icontains=userorganisation).filter(Disipline__icontains=userdisipline).filter(Subdisipline__icontains=usersubdisipline)
    def get_myActionsCount(self,userorganisation,userdisipline,usersubdisipline):
        return self.filter(Organisation__icontains=userorganisation).filter(Disipline__icontains=userdisipline).filter(Subdisipline__icontains=usersubdisipline).count ()
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
    def get_myItemsbyCompDisSub(self,userorganisation,userdisipline,usersubdisipline):
        return self.get_queryset().get_myActions(userorganisation,userdisipline,usersubdisipline)

class myActionCount(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def get_myItemsCount(self,userorganisation,userdisipline,usersubdisipline):
        return self.get_queryset().get_myActionsCount(userorganisation,userdisipline,usersubdisipline)


class Approver1Manager(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def get_myItemsbyCompDisSub(self,userorganisation,userdisipline,usersubdisipline):
        return self.get_queryset().get_Approver1(userorganisation,userdisipline,usersubdisipline)

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