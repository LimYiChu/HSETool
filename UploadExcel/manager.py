from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
class QuerySet(models.QuerySet):
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_myActions(self,userorganisation,userdisipline,usersubdisipline,que): 
        return self.filter(Organisation__iexact=userorganisation).filter(Disipline__iexact=userdisipline).filter(
                Subdisipline__iexact=usersubdisipline).filter(QueSeries__iexact=que).values()

    #edward 20210729 changing icontains to iexact for Disc,SubDisc
    def get_myActionsCount(self,userorganisation,userdisipline,usersubdisipline,que): #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
        return self.filter(Organisation__iexact=userorganisation).filter(Disipline__iexact=userdisipline).filter(Subdisipline__iexact=usersubdisipline).filter(QueSeries__iexact=que).count ()
    #edward 20210729 changing icontains to iexact for Disc,SubDisc
    def get_myActionsCountbyStudies(self,studies, organisation,disipline,subdisipline,que):
        return self.filter(StudyName__iexact=studies).filter(Organisation__iexact=organisation).filter(Disipline__iexact=disipline).filter(
            
                            Subdisipline__iexact=subdisipline).filter(QueSeries__iexact=que).count ()
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_allActionsCountbyStudies(self,studies, que):
        return self.filter(StudyName__iexact=studies).filter(QueSeries__iexact=que).count ()
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_allActionsCountbyDisc(self,Disc, que):
        return self.filter(Disipline__iexact=Disc).filter(QueSeries__iexact=que).count ()

    def set_field(self,ID, fields, value):
        
        
        return self.filter (id=ID).update (**{fields: value})
    
    def get_field(self,ID, fields):
                
        return self.filter (id=ID).values(fields)
        #field = eval('obj.'+fields)
        #return field

    def get_allActionsCount(self,workshop,que):
        return self.filter (QueSeries__iexact=que).count ()
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_DiscSubActionsCount(self,workshop,DiscSub,que):
        return self.filter (Disipline__iexact=DiscSub[0]).filter(Subdisipline__iexact=DiscSub[1]).filter (QueSeries__iexact=que).count ()
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_DiscSubOrgActionsCount(self,workshop,DiscSub,que): #get discipline, sub-disc, get the filter
        return self.filter (Disipline__iexact=DiscSub[0]).filter(Subdisipline__iexact=DiscSub[1]).filter (Organisation__iexact=DiscSub[2]).filter (
            QueSeries__iexact=que).count ()
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_DiscSubOrgRejectedActionsCount(self,DiscSub,Revvalue): #get discipline, sub-disc, get the filter
        return self.filter (Disipline__iexact=DiscSub[0]).filter(Subdisipline__iexact=DiscSub[1]).filter (
                        Organisation__iexact=DiscSub[2]).filter (Revision__gte=Revvalue).count ()
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_DiscSubOrgRejectedActions(self,DiscSub,Revvalue): #get discipline, sub-disc, get the filter
        return self.filter (Disipline__iexact=DiscSub[0]).filter(Subdisipline__iexact=DiscSub[1]).filter (
                        Organisation__iexact=DiscSub[2]).filter (Revision__gte=Revvalue).values()
    def get_AllRejectedActions(self,Revvalue,queseriesrejected): #get discipline, sub-disc, get the filter
        return self.filter (Revision__gte=Revvalue).filter(QueSeries=queseriesrejected).values() # if que series moves from 0 it has been resubmitted and not considered rejected

    def get_mgrComments(self,fkey):
        return self.filter(Action__pk=fkey)
    #edward 20210729 changing icontains to iexact for Org,Disc,SubDisc
    def get_mgrCompanyCount(self,Company,que):
        return self.filter (Organisation__iexact=Company).filter (QueSeries__iexact=que).count()
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
    def mgr_myItemsCountbyStudies(self,studies, organisation,disipline,subdisipline,que):
        return self.get_queryset().get_myActionsCountbyStudies(studies, organisation,disipline,subdisipline,que)
    def mgr_allItemsCountbyStudies(self,studies,que):
        return self.get_queryset().get_allActionsCountbyStudies(studies,que)
    def mgr_allItemsCountbyDisc(self,Disc,que):
        return self.get_queryset().get_allActionsCountbyDisc(Disc,que)

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
    def mgr_getDiscSubOrgItemsCount(self,workshop,DiscSub,que): 
        return self.get_queryset().get_DiscSubOrgActionsCount(workshop,DiscSub,que)
    def mgr_getDiscSubOrgRejectedItemsCount(self,DiscSub,Revision):
        return self.get_queryset().get_DiscSubOrgRejectedActionsCount(DiscSub,Revision)
    def mgr_getDiscSubOrgRejectedItems(self,DiscSub,Revision):
        return self.get_queryset().get_DiscSubOrgRejectedActions(DiscSub,Revision)
    def mgr_getAllRejectedItems(self,Revision,queseries):
        return self.get_queryset(). get_AllRejectedActions(Revision,queseries)   

class mgrgetActionCompanyCount(models.Manager):
    def get_queryset (self):
        return QuerySet(self.model, using=self._db)
    def mgr_getCompanyCount(self,Company,que):
        return self.get_queryset().get_mgrCompanyCount(Company,que)

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
class mdlGetSetQueRevision(models.Manager):
    
    def mgrsetQueSeries(self,ID, Que):
        obj = get_object_or_404(self.model, id=ID)
        obj.QueSeries = Que
        obj.save(update_fields=["QueSeries"],using=self.db)

    def mgrincrementRevision(self,ID):
        obj = get_object_or_404(self.model, id=ID)
        obj.Revision += 1
        obj.save(update_fields=["Revision"],using=self.db)

class mgrSetfields(models.Manager):
    def get_queryset (self):
         return QuerySet(self.model, using=self._db)
    def mgrSetField(self,ID, fields, value):
         #lookup = str(fields)+'__icontains' - This is how you search dynamically but since we are setting it
         return self.get_queryset().set_field(ID, fields, value)

class mgrgetfields(models.Manager):
    def get_queryset (self):
         return QuerySet(self.model, using=self._db)
    def mgrGetField(self,ID, fields):
         #lookup = str(fields)+'__icontains' - This is how you search dynamically but since we are setting it
         return self.get_queryset().get_field(ID, fields)

class mgrDeleteAttachment(models.Manager):

    def mgrDeleteAttachmentbyID(self,ID):
        obj = get_object_or_404(self.model, id=ID)
        obj.delete()
        return True
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