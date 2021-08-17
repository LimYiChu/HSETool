from django.db.models.fields import NullBooleanField
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from UploadExcel.forms import *
from django.contrib.auth import get_user_model
import matplotlib as plt
from .businesslogic import *
from .tableheader import *
from .excelReports import *
from .models import *
from UploadExcel.models import *
from django.views.generic import ListView, DetailView, UpdateView,TemplateView, CreateView
#test for login required
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail
from .reports import *
#from Trackem.settings import EMAIL_HOST_USER - to delete and change as per discussion with edward it uses deault EMail user in settings
from django.template.loader import render_to_string
from django.template import loader
from django.core.mail import EmailMessage
import pandas as pd
from django.utils import timezone
import os
#import mixins
from django.views.generic.detail import SingleObjectMixin
from userT.pdfgenerator import *
from django.db.models import Count

from zipfile import ZipFile
from io import StringIO, BytesIO

#Rest Framework
from rest_framework import viewsets
from .serializers import *
#from .forms import UserRegisterForm
# Create your views here.

from UploadExcel.forms import *
from userT.parameters import *
#edward scheduler
# from .scheduler import *

#from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

# edward 20210713 added json import
import json
#edward 20210722 added datetime
import datetime 
from datetime import date as dt 
from operator import itemgetter



from collections import OrderedDict
def loadsignature (request):
    
    form1 = frmMultipleFiles()
    obj = CustomUser.objects.get(id=11)
    form2 = CustomUserSignature(instance=obj)

  
    if (request.POST.get('Upload')):
        #ID= form2.instance.id
        FORM2=CustomUserSignature(request.POST)
       

        #CustomUser.mdlSetField.mgrSetField(ID,"signature",Signature)
   

        #Signature=request.POST.get('signature')
       
        #x=CustomUser.objects.get(id=form2.instance.id)
        #formuser = CustomUserSignature(request.POST, instance=x)
        #formuser.save()
    
    context = {
        'form1' : form1,
        'form2': form2

    }

    return render(request, 'userT/loadsignatures.html',context) #yhs checked small letters


class anyView(viewsets.ModelViewSet):

    queryset = ActionItems.objects.all()
    serializer_class = anySerializers

def googlecharts(request):
    
    
    lstbyDueDate    = blaggregatebydate(ActionItems.objects.all())
    #print (lstbyDueDate)

    lstplanned          = blprepareGoogleChartsfromDict(lstbyDueDate)

    print (lstplanned)
    lstactual           = blgetActualRunDown(lstplanned)
    newlist             = blformulateRundown(lstplanned,lstactual)
  
    for items in lstbyDueDate:

        x=items.get('DueDate')

    subtotal =[]
   
    for items in lstbyDueDate:
       subtotal.append(items['count']) #how to access dictionary object by
    
    content1 =  newlist
    

    content2= [['2021-01-10', 136, 136], 
                ['2021-02-10', 133, 136], 
                ['2021-04-18', 124, 136], 
                ['2021-04-29', 113, 136], 
                ['2021-05-01', 110, 136], 
                ['2021-05-08', 80, 136], 
                ['2021-06-03', 77, 133], 
                ['2021-07-09', 70, 131], 
                ['2021-07-13', 69, ], 
                ['2021-07-15', 67, ], 
                ['2021-07-16', 66, ], 
                ['2021-07-23', 63, ], 
                ['2021-07-30', 15, ], 
                ['2021-08-26', 14, ], 
                ['2021-10-10', 13, ], 
                ['2021-10-15', 10, ], 
                ['2021-10-16', 8, ], 
                ['2021-10-17', 0, ]]
    context = {
        
        'content' : content1,
        'charttitles' : "XYZ"
      

    }
    
    #return JsonResponse()
    return render(request, 'userT/googlecharts.html',context) #ok checked by yhs

    
# edward 20210713 new chart
def googlecharts88(request):
    
    
    lstbyDueDate    = blaggregatebydate(ActionItems.objects.all())
    
    lstplanned          = blprepareGoogleChartsfromDict(lstbyDueDate)
    lstactual           = blgetActualRunDown(lstplanned)
    newlist             = blformulateRundown(lstplanned,lstactual)
    
    for items in lstbyDueDate:

        x=items.get('DueDate')

    subtotal =[]
    for items in lstbyDueDate:
       subtotal.append(items['count']) #how to access dictionary object by
    
    content =  newlist
    # print(content1)
    # blstopcharttoday(content1)
    
# edward 20210723 end new graphing to stop on current day   
# content2 using hardcoded data for testing 
    # content = [    
    #                 ['2021-06-08', 68, 68], 
    #                 ['2021-06-08', 68, 68],
    #                 ['2021-07-08', 67, 68], 
    #                 # ['2021-07-09', 62, 65], 
    #                 # ['2021-07-15', 58, 58], 
    #                 # ['2021-07-16', 57, 58], 
    #                 # ['2021-07-20', 57, 58], 
    #                 # ['2021-07-24', 57, 58], 
    #                 ['2021-07-25', 54, 56], 
    #                 ['2021-07-30', 14, 20], 
    #                 # ['2021-08-26', 13, 14], 
    #                 # ['2021-10-15', 10, 12], 
    #                 # ['2021-10-16', 8, 10], 
    #                 # ['2021-10-17', 0, 5]
    #             ]
    content1 = blstopcharttoday(content)

    # strtoday = dt.today().strftime('%Y-%m-%d') #todays date as string
    # today= dt.today()#.strftime('%Y-%m-%d') #todays date as string
    # closed =(len(ActionItems.objects.filter(QueSeries=99))) #closed items
    # TotalActionItems = (len(ActionItems.objects.all())) #total items
    # actual = (TotalActionItems-closed) # use this to append the actual data
    # currentdate = [today,' ',actual]
    # empty=[]
   
    # for items in content:
    #     items[0] = datetime.datetime.strptime(items[0], '%Y-%m-%d').date() # datetime obj has problems bcs comparing down to the minute

    # if not any(today in items for items in content) :
    #     content.insert(0,currentdate)
    #     print("InsertedDate", content)
    # else :
    #     content
    # sortedcontent = sorted(content, key=itemgetter(0)) # itemgetter(0) sorts by first entry inside list of list (date in this case)
    # print(sortedcontent)
   
    # for items in sortedcontent:        
    #     items[0]=items[0].strftime('%Y-%m-%d')
    #     if items[0]> strtoday:
    #         items.pop(2)
    
    # content = sortedcontent
        


    
    context = {
        
        # 'contentplanned' :contentplanned,
        # 'contentactual' : contentactual
        'content' : content1

        
      

    }
    #return JsonResponse()
    return render(request, 'userT/googlecharts88.html',context) #ok checked by yhs
# edward 20210713 end new chart

def mainDashboard (request):
   
    #get workshops
    studies = blgetAllStudies()

    #get all routes
    dict_allRou = blgetuserRoutes(request.user.email)
    
    #Just get Actionee and Approver Routes, tied into model managers
    Actionee_R =    dict_allRou.get('Actionee_Routes')
    Approver_R =    dict_allRou.get('Approver_Routes') 

    ActionCount = blfuncActionCount(Actionee_R,0)
    totalactioneeaction=sum(ActionCount)
    
   #****chart parameters to pass in 
   
    QueOpen = [1,2,3,4,5,6,7,8,9]
    QueClosed =99  
    # **** End Chart Parameters

    #***Initilise list count
    stripCount =[]
    striplabels = []
    chartappdata=[]
    actioneefinallist =[]
    apprfinalist =[]
    labelsApprover =[]
    dataApprover =[]
    appractioncount =[]
    #****end list count

    for eachstudy in studies:
        StudyName = eachstudy.StudyName
        
        labels=[]
        
        countbyStudies, labels= blActionCountbyStudiesStream(Actionee_R,StudyName,0) 
        countbyStudiesClosed, labelsClosed= blActionCountbyStudiesStream(Actionee_R,StudyName,QueClosed)
             
        stripCount, striplabels ,  = stripAndmatch(countbyStudies,labels)
       
        if stripCount != [] : # Just to get a better view in HTML instead of rendering spaces for empty charts
            googlechartlist = blprepGoogChartsbyStudies(striplabels,stripCount,StudyName)
            actioneefinallist.append(googlechartlist)
            googlechartlist =[] 

        #complete sub routine for actionee and then go to approver
        for QueSeries, Routes in Approver_R.items():
            
            listofCountManyApprovers,labelsapp =blActionCountbyStudiesStream(Routes,StudyName,QueSeries) 
            sumoflistCount = sum(listofCountManyApprovers)
            appractioncount.append(sumoflistCount)
            if (sumoflistCount > 0):
                labelsApprover.append('Level'+str(QueSeries))
                dataApprover.append(sumoflistCount)
                
                chartappdata = blprepGoogChartsbyStudies(labelsApprover,dataApprover,StudyName)
                sumoflistCount = 0

        
        apprfinalist.append(chartappdata)
        
        totalapproveraction = sum (appractioncount)
        #empties out the data for next loop otherwise it doubles the data to append on each study
        chartappdata = []
        
        dataApprover = []
        labelsApprover =[]
        countbyStudies = []
   
    Context = {
        'totalapproveraction' : totalapproveraction,
        'totalactioneeaction' : totalactioneeaction,
        'actioneefinallist' : actioneefinallist,
        'apprfinalist' : apprfinalist,
        
            }
    return render(request, 'userT/maindashboard.html',Context) #ok checked by yhs in terms of capital letters.


def getActionDetails(request, id=None):
    Items = get_object_or_404(ActionItems,id=id)
    context = {
            "Items":Items

    }
    return render(request, "userT/detailactions.html", context) #ok checked by yhs in terms of capital letters.

#below view is for list of actions under actionee , 
# it returns a list of actions under object_list
class ActioneeList (ListView):
    template_name   =   'userT/actionlistactionee.html' #yhs changed to all small letters
    
    def get_queryset(self):
        userZemail = self.request.user.email
        ActioneeRoutes =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
        #actioneeItems = blfuncActioneeComDisSub(ActioneeRoutes,0) - To be deleted - this was limited to 3 streams
        
        ActioneeActions = blallActionsComDisSub(ActioneeRoutes,0)
        rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated']

        finalactionitems = bladdriskcolourandoptimise(ActioneeActions,rem_list)
       
                
                
        return finalactionitems
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riskmatrix'] = blgetRiskMatrixColour()
       
        return context
        # context = super().get_context_data(**kwargs)
        # # Add in a QuerySet of all the books
        # context['book_list'] = Book.objects.all()
        
        #res = next((sub for sub in riskmatrices if sub['Combined'] == "5A"),None)
       
class HistoryList (ListView):
    template_name   =   'userT/historylist.html' #ok checked by yhs in terms of capital letters.
    
    def get_queryset(self):
        #historically only get queue for all approver levels that he person is the actionee instead of everything else
        userZemail = self.request.user.email
        
        dict_allRou = blgetuserRoutes(userZemail)
    
        #Just get Actionee and Approver Routes, tied into model managers
        Actionee_R =    dict_allRou.get('Actionee_Routes')
        lstgetHistoryforUser             = blgetHistoryforUser(userZemail,Actionee_R)
        
        #the sequence just appends risk matrix colours
        rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated']
        finalactionitems = bladdriskcolourandoptimise(lstgetHistoryforUser,rem_list)
        
        return lstgetHistoryforUser

    def get_context_data(self, **kwargs):

        userZemail = self.request.user.email

        context = super().get_context_data(**kwargs)
        context['riskmatrix'] = blgetRiskMatrixColour()

        dict_allRou = blgetuserRoutes(userZemail)
        Approver_R =    dict_allRou.get('Approver_Routes')

        ApproverActions = []

        for key, value in Approver_R.items():
            #x = blfuncActioneeComDisSub(value,key)
            #starts with key 1 - it shows if your name is in approver 1
            #The key reresents que series
            allactionItems= blApproverHistoryActions(value,key)
            ApproverActions.insert(key,allactionItems)

        approverflatdict = [item for sublist in ApproverActions for item in sublist] # Just merging all approvers levels into a flatter list

        rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated']
       
        #addriskcolour to approver list
        finalappractionitems= bladdriskcolourandoptimise(approverflatdict,rem_list) 
        
        rejecteditemsid = blRejectedHistortyActionsbyId(userZemail,0,1)

        # Need to make a list to feed into bladdriskcolourandoptimise as that function is expecting a list of dictionaries
        rejecteditemsbyhistory = [blgetActionItemsbyid(rejecteditemsid)]
        newrejecteditemsbyhist                        = bladdriskcolourandoptimise(rejecteditemsbyhistory,rem_list)
        #Last part , pass back to HTML and render in tab
        #print (rejecteditemsbyhistory)
        context['rejectedhistory'] = rejecteditemsbyhistory
        context['approveractions'] = finalappractionitems
         
        return context

class ApproverList (ListView):
    template_name   =   'userT/actionlistapprover.html' #yhs changed to all small letters
    
    def get_queryset(self):
        userZemail = self.request.user.email
        ApproverActions = []
        dict_allRou = blgetuserRoutes(userZemail)
        Approver_R =    dict_allRou.get('Approver_Routes')
        
        print(Approver_R)
        for key, value in Approver_R.items():
            #x = blfuncActioneeComDisSub(value,key)
            allactionItems= blallActionsComDisSub(value,key)
            ApproverActions.insert(key,allactionItems)
            
        rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated']
        
        for items in ApproverActions:
            #have to do a loop as its adding another level compared to actionee
            finalactionitems= bladdriskcolourandoptimise(items,rem_list) #The way python works its not using this finally but editing ApproverActions directly

        return ApproverActions
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riskmatrix'] = blgetRiskMatrixColour()
        return context
class DetailActioneeItems (DetailView):
    template_name   =   'userT/actiondetailactionee.html' #yhs changed to all small letters
    #queryset = ActionItems.objects.all()

    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)


class ApproveItemsMixin(UserPassesTestMixin,UpdateView):
    #paginate_by = 20
    template_name = "userT/actionupdateapproveaction.html" #yhs changed to all small letters 
    form_class = ApproverForm
    success_url = '/ApproverList/'

    def test_func(self,**kwargs):
        
        ingroup =  self.request.user.groups.filter(name="Approver").exists()

        IdAI = self.kwargs.get("pk")
        
        emailID = self.request.user.email
        inroute = blgetvaliduserinroute(IdAI,emailID)

        #satifies 2 test before allowing to access items in Url  otherwise just redirect to main
        if  (ingroup) and (inroute):
            return True
        else :
            return False     
    def handle_no_permission(self):
        #if no permission from test_func return to main
        return HttpResponseRedirect('/main')

    def get(self, request, *args, **kwargs):
        #uses pk key to automatically get objext
        self.object = self.get_object(queryset=ActionItems.objects.all())
        return super().get(request, *args, **kwargs)

    def get_object(self,queryset=None):
       
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['pk'])
       
    def form_valid(self,form):
        
            #if form is valid just increment q series by 1 so it goes to Approver que so it goes to next queSeries
        if (self.request.POST.get('Reject')):
                #If reject que series should be 0, but need another intermediate screen for comments
                #form.instance.QueSeries = 0
            
                #Need to do below with HTTPResponseredirect because normal reverse seems to give an str error
                #reverse simply redirects to url path so can call class RejectReason below since cant really call it from fucntion call directly
                #makes sense since really django wants to work with views coming from URL paths- simply a structured way of doing stuff
            context = {
                        'StudyActionNo' : form.instance.StudyActionNo
                }
            return HttpResponseRedirect(reverse ('RejectReason', kwargs={'forkeyid': form.instance.id})) #this is key as wanted another screen on the first reject

        if (self.request.POST.get('Cancel')):
#             
           return HttpResponseRedirect('/ApproverList/')

        if (self.request.POST.get('Approve')): 
                #  need another intermediate screen for approval no comments
           

            return super().form_valid(form)
        if (self.request.POST.get('Pullback')):

            return super().form_valid(form)
        if (self.request.POST.get('Delete')): 
                #  need another intermediate screen for approval no comments
            AttachmentID = self.request.POST.get ('filepk') # hidden file that holds ID of the attachment
            ActionItemID = form.instance.id
            Status = Attachments.mdlDeleteAttachment.mgrDeleteAttachmentbyID(AttachmentID)
            
            return redirect('ActioneeFormMixin' , pk=ActionItemID)

        if (self.request.POST.get('Next')): 
            return super().form_valid(form)

    def get_context_data(self,**kwargs):
        idAI = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        discsub = blgetDiscSubOrgfromID(idAI)
        Signatories = blgetSignotories(discsub)

        #There is an error going on here or so to speak as its calling ActioneeItemsMixin as well odd error and cant narrow it down
        #edward 20210707 trying to use consolidated version blgettimestampuserdetails
        lstSignatoriesTimeStamp= blgettimestampuserdetails (idAI, Signatories) #it changes the signatories directly
        # edward added set approver target for approver 20210701 patch 2.5b
        # edward 20210703 pushing approver set queue target to main
        ApproverLevel = blgetApproverLevel(discsub)
        blsetApproverLevelTarget(idAI,ApproverLevel) #sets approver level target
        # end of edward added set approver target for approver 20210701 patch 2.5b
        object_list = self.object.attachments_set.all()

        context['object_list'] = object_list
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(idAI)
        context['Approver'] = True
        context ['Signatories'] = lstSignatoriesTimeStamp
        
        return context

    # def get_queryset(self):
    #    return self.object.attachments_set.all() #-this one gets the the attachments and puts it into Object_List

    def get_success_url(self):
        return reverse ('ApproverConfirm', kwargs={'id': self.object.id})

class ApproverConfirm(UpdateView):
    
    template_name = "userT/approverconfirmation.html" #yhs changed to all small letters
    form_class = frmApproverConfirmation
    success_url = '/ApproverList/'
    
    def form_valid(self,form):
        #edward added for showing email as deafult signature
        emailid=self.request.user.email
        strsignature = blgetfieldCustomUser(emailid,"signature")

        if (self.request.POST.get('Cancel')):
             
           return HttpResponseRedirect('/ApproverList/')

        if (self.request.POST.get('ApproveConfirm')): 
                #  need another intermediate screen for approval no comments
            
            ID =self.kwargs["id"]
            
            field = "QueSeriesTarget"
            
            ApproverLevel =  blgetFieldValue(ID,field)
            
            if (form.instance.QueSeries == (ApproverLevel-1)): 
                form.instance.QueSeries = 99 # Random far end number to show all closed
            else:
                form.instance.QueSeries += 1

                #edward added for showing email as deafult signature
            if (self.request.POST.get('signature')):
                strsignature = self.request.POST.get('signature')
                blsetfieldCustomUser(emailid,"signature",strsignature)
            else :
                blsetfieldCustomUser(emailid,"signature",str(emailid))
            #     #end

            #edward next approver sent email when approved 20210708 manage to send but trying to figure out how to send just to approver who submit and the next approver
            integerqueseries = blgetFieldValue(ID,"QueSeries") # using this to find Approver QueSeries
            discsub = blgetDiscSubOrgfromID(ID)
            Signatoryemails = blgetSignatoryemailbyque2(discsub,integerqueseries+1)
            ContentSubject  =blbuildApprovedemail(ID) # using new bl since approver email should be this has been approved instead of submitted
            success = blemailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1])  
            #edward end next approver sent email when approved 20210708  
              
            return super().form_valid(form)

    #edward added for showing email as deafult signature
    def get_context_data(self, **kwargs): 
        emailid=self.request.user.email
        sign=self.request.user.signature
       
        context = super().get_context_data(**kwargs)
        context['signature'] = blgetfieldCustomUser(emailid,"signature")
        return context

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
      
        return queryset.get(id=self.kwargs['id'])

#Guna using History Form Mixin - Need to delete below
# class HistoryFormApprover(ApproveItemsMixin):
    
#     template_name = "userT/historyformapprover.html" 
#     form_class = frmApproverConfirmation
#     success_url = '/HistoryList/'
    
#     def get_context_data(self,**kwargs):
#         id = self.object.id #its actually the id and used as foreign key
        
#         context = super().get_context_data(**kwargs)
        
#         discsuborg = blgetDiscSubOrgfromID(id)
#         ApproverLevel = blgetApproverLevel(discsuborg)
        
#         # #sets the signatory directly in getting timestamp
#         Signatories = blgetSignotories(discsuborg)
#         #edward 20210707 trying to use consolidated version blgettimestampuserdetails
#         lstSignatoriesTimeStamp= blgettimestampuserdetails (id, Signatories)
#         object_list = self.object.attachments_set.all()

#         context['object_list'] = object_list
#         context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(id)
#         context['Approver'] = False
#         context ['ApproverLevel'] = ApproverLevel
#         context ['Signatories'] = lstSignatoriesTimeStamp
       
#         return context
#     def form_valid(self,form):

#         if (self.request.POST.get('Pullback')):

#             return super().form_valid(form)
        
#         if (self.request.POST.get('Cancel')):
# #             
#            return HttpResponseRedirect('/HistoryList/')

#     def get_success_url(self):
#         return reverse ('HistoryConfirm', kwargs={'id': self.object.id })

class HistoryConfirm(UpdateView):
    
    template_name = "userT/historyconfirmpull.html" #yhs checked capital
    form_class = frmApproverConfirmation
    success_url = '/HistoryList/'
    
    def form_valid(self,form):
        if (self.request.POST.get('Cancel')):
#             
           return HttpResponseRedirect('/HistoryList/')

        if (self.request.POST.get('Pullconfirm')): 
                #  need another intermediate screen for final confirmation
            
            #ID =self.kwargs["id"]
            form.instance.QueSeries = 0 # Return back to Actionee
            

            return super().form_valid(form)

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
      
        return queryset.get(id=self.kwargs['id'])

class HistoryFormMixin(UserPassesTestMixin,UpdateView):
    template_name = "userT/historypullback.html" 
    form_class = frmApproverConfirmation
    
    def test_func(self,**kwargs):
        
        if (self.request.user.groups.filter(name="Approver").exists()) or self.request.user.groups.filter(name="Actionee").exists():
            ingroup =  True
        else :
            ingroup = False
            
        IdAI = self.kwargs.get("pk")
        emailID = self.request.user.email
        inroute = blgetvaliduserinroute(IdAI,emailID,True)

        #satifies 2 test before allowing to access items in Url  otherwise just redirect to main
        if  (ingroup) and (inroute):
            return True
        else :
            return False     
    def handle_no_permission(self):
        #if no permission from test_func return to main
        return HttpResponseRedirect('/main')

    def get_object(self,queryset=None):
       
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs,):
        #id = self.object.id  # old code just leave it as its a good example
        
        id = self.kwargs['pk'] 
        isactionee= eval(self.kwargs['actionee']) #convert string to boolean values so can use direct in HTML
       
        context = super().get_context_data(**kwargs)
        
        #print ("KWARGS",context)
        discsuborg = blgetDiscSubOrgfromID(id)
        ApproverLevel = blgetApproverLevel(discsuborg)
        
        # #sets the signatory directly in getting timestamp
        Signatories = blgetSignotories(discsuborg)
        
       
        lstSignatoriesTimeStamp= blgettimestampuserdetails (id, Signatories)
        
   
        #get location of action and have it in tray at top of the action in history view
        #Start edward
        actionlocation = []
        integerqueseries = blgetFieldValue(id,"QueSeries") #change to use bl function
        if integerqueseries != 99 and (Signatories !=[]): # looks at que series and then matches it against the list of signatories for an action, != means not equal
            lststuckAt = Signatories[integerqueseries]#uses QueSeries to indicate where action currently is
            actionlocation.append(lststuckAt[1])
        else: 
            actionlocation.append('Closed')
        #end edward

        object_list = self.object.attachments_set.all()
        context ['object_list'] = object_list
        context['actionlocation'] = actionlocation[0]
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(id)
        context['Approver'] = False
        context ['ApproverLevel'] = ApproverLevel
        context ['Signatories'] = lstSignatoriesTimeStamp
        context ['isactionee'] = isactionee
        return context

    def form_valid(self,form):

        if (self.request.POST.get('Pullback')):

            return super().form_valid(form)
        
        if (self.request.POST.get('Cancel')):
#             
           return HttpResponseRedirect('/HistoryList/')

    def get_success_url(self):
        return reverse ('HistoryConfirm', kwargs={'id': self.object.id })

#@user_passes_test(lambda u: u.groups.filter(name='Actionee').count() == 0, login_url='/main')
class ActioneeItemsMixin(UserPassesTestMixin,UpdateView):
    template_name = "userT/actionupdateapproveaction.html" #yhs changed to all small letters
    form_class = frmUpdateActioneeForm
    
    #delete 
    # def get(self, request, *args, **kwargs):
    #     #uses pk key to automatically get objext
    #     self.object = self.get_object(queryset=ActionItems.objects.all())
    #     return super().get(request, *args, **kwargs)
    def test_func(self,**kwargs):
        
        ingroup = self.request.user.groups.filter(name="Actionee").exists()
        print (ingroup)
        IdAI = self.kwargs.get("pk")
        emailID = self.request.user.email
        inroute = blgetvaliduserinroute(IdAI,emailID)

        #satifies 2 test before allowing to access items in Url  otherwise just redirect to main
        if  (ingroup) and (inroute):
            return True
        else :
            return False     
     
    def handle_no_permission(self):
        #if no permission from test_func return to main
        return HttpResponseRedirect('/main')

    def get_object(self,queryset=None):
       
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['pk'])

    def get_context_data(self,**kwargs):
        IdAI = self.kwargs.get("pk") #its actually the id and used as foreign key
        context = super().get_context_data(**kwargs)
        
        discsuborg = blgetDiscSubOrgfromID(IdAI)
        ApproverLevel = blgetApproverLevel(discsuborg)
        Signatories = blgetSignotories(discsuborg)
        blsetApproverLevelTarget(IdAI,ApproverLevel)
        #edward 20210707 trying to use consolidated version blgettimestampuserdetails
        lstSignatoriesTimeStamp= blgettimestampuserdetails (IdAI, Signatories)
        object_list = self.object.attachments_set.all()

        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(IdAI)
        context['Approver'] = False
        context ['ApproverLevel'] = ApproverLevel
        context ['Signatories'] = lstSignatoriesTimeStamp
        context ['object_list'] = object_list
        return context

    def form_valid(self,form):

        if (self.request.POST.get('Cancel')):   
           return HttpResponseRedirect('/ActioneeList/')

        if (self.request.POST.get('Next')): 
            return super().form_valid(form)

        if (self.request.POST.get('Delete')): 
                #  need another intermediate screen for approval no comments
            AttachmentID = self.request.POST.get ('filepk') # hidden file that holds ID of the attachment
            ActionItemID = form.instance.id
            Status = Attachments.mdlDeleteAttachment.mgrDeleteAttachmentbyID(AttachmentID)
            
            return redirect('ActioneeFormMixin' , pk=ActionItemID)
      
    def get_success_url(self):
        return reverse ('multiplefiles', kwargs={'forkeyid': self.object.id})

def ContactUs (request):
    return render(request, 'userT/contactus.html') #yhs changed to all small letters

class RejectReason (CreateView):
    model = Comments
    template_name = 'userT/rejectreason.html' #yhs changed to all small letters
    form_class = frmAddRejectReason
    success_url = '/ApproverList/'

    def form_valid (self,form):
        if (self.request.POST.get('Reject')):
            ID = self.kwargs['forkeyid']
            intqueseries = blgetFieldValue(ID,"QueSeries")
            
            #set using model manager since we want it back to actionee it has to be set at QueSeries=0
            blsetrejectionActionItems(ID,0)# This is key and should go into bltoset this and revision
            
            form.instance.Action_id = ID
            form.instance.Username = self.request.user.email
            rejectreason =  form.instance.Reason
           
            discsub = blgetDiscSubOrgfromID(ID)
            
            Signatoryemails = blgetSignatoryemailbyque(discsub,intqueseries)

            
            ContentSubject  =blbuildRejectionemail(ID,rejectreason)

            success = blemailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1]) #send email, the xyz is dummy data and not used
            
            return super().form_valid(form)
        if (self.request.POST.get('Cancel')):
            #cant use success url, its got assocaition with dict object, so have to use below
            
            return HttpResponseRedirect('/ApproverList/')
    def get_context_data(self, **kwargs):
        fk = self.kwargs['forkeyid']
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        return context

#-commented below to remove
# def IndividualBreakdownByUsers(request):
#     #Need to do some maths here  most of the functions have been charted out just need to remap back to individual
#     # 2 functions need to merge
#     discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
   
#     #Signatories = 
    
#     QueOpen = [0,1,2,3,4,5,6,7,8,9]
#     QueClosed = [99]
#     Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)          
   
#     context = {
        
#         'Indisets' : Indisets,
        
#     }
            
#     return render(request, 'userT/indibreakbyuser.html',context) #yhs changed to all small letters

def IndividualBreakdownByActions(request):
    
    allactions = ActionItems.objects.all()
                #blgetdetailsofeachActions(allactions)
    lstattributes = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','InitialRisk']
   
    lstofindiactions = blgetActionStuckAt(allactions, lstattributes)

    context ={
        
        'context' : lstofindiactions

    }

    return render(request, 'userT/indibreakdownbyactions.html', context)#yhs changed to all small letters

# def ContactUs (request):
#     return render(request, 'userT/ContactUs.html')

def multiplefiles (request, **kwargs):
  
    form_multi = frmMultipleFiles()
    emailid = request.user.email
    strsignature = blgetfieldCustomUser(emailid,"signature")
 
    if (request.POST.get('Upload')):
        
        ID = kwargs['forkeyid']
        #set using model manager since we want it back to actionee it has to be set at QueSeries=0
        files = request.FILES.getlist('Attachment')
        if (request.POST.get('signature')):
            strsignature = request.POST.get('signature')
            blsetfieldCustomUser(emailid,"signature",strsignature)
        else :
            blsetfieldCustomUser(emailid,"signature",str(emailid))
            
        for file in files:
            #should be doing via model manager , the problem is its justa line of code
            x = Attachments.objects.create(
                Attachment=file,
                Action_id=ID,
                Username=request.user.email
            )
        #edward 20210709 testing around here before consolidating
        newQueSeries = 1
        
        ActionItems.mdlQueSeries.mgrsetQueSeries(ID,newQueSeries)
        
        discsub = blgetDiscSubOrgfromID(ID)

        # Signatoryemails = blgetSignatoryemailbyque(discsub,newQueSeries+1)    
        Signatoryemails = blgetSignatoryemailbyque2(discsub,newQueSeries) # edward 20210709 altered this to use with new bl
        
            
        ContentSubject  =blbuildSubmittedemail(ID)
        
        success = blemailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1])
        
        
        return HttpResponseRedirect('/ActioneeList/')
            
    if (request.POST.get('Cancel')):
            #cant use success url, its got associattion with dict object, so have to use below
            return HttpResponseRedirect('/ActioneeList/')

        
    context = {
        'form_multi' : form_multi,
        'signature' : strsignature,

    }
    ID = kwargs['forkeyid']

  
    return render(request, 'userT/multiplefiles.html',context) #yhs checked small letters


def rptoverallStatus(request, **kwargs):
    #this function is too messy and needs to be cleaned up
    #Function on businees logic to get data based on Queseries, Actionee and Approver levels
    #most of the data is
    openActionsQueSeries = [0,1,2,3,4,5,6,7,8,9]
    closedActionsQueSeries = [99]
    allOpenActions= blfuncgetallAction('Y', openActionsQueSeries)
    allClosedActions = blfuncgetallAction('Y', closedActionsQueSeries)
    charts =[]
    chartChanges =[]
    #this is for overall charts
    listofOpenClosed = [allOpenActions,allClosedActions]
    labelsOpenClosed = ['Open', 'Closed']
    
    charts.append(showPie(listofOpenClosed,labelsOpenClosed,"Overall Action Status"))
    
    #this is for disc/sub-disipline
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
    
    #important to separate list , reusing list will fuck it up by adding list below to this one
    listcountbyDisSub= []
    listlablesDisc =[]
    listcountbyCompany= []
    listlabelsCompany = []

    #default view
    for itemPair in discsub:
        
        listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,openActionsQueSeries))
        listlablesDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
    
    chartChanges.append(showPie(listcountbyDisSub,listlablesDisc, "Open Actions by Disc/Sub-Disc"))

    #if generatePdf is hit, the selection is checked and graphs generated internally
    if request.method == 'POST':

        ActionStatus = request.POST.get ('ActionStatus')
        ActionsSorton = request.POST.get ('SortOn')
        ViewExcel = request.POST.get('viewExcel')
       
        if (ViewExcel):
          
            excelCompleteReport(request)
            
            
        if ActionStatus =='Open':
            chartChanges = []
            if ActionsSorton == 'Company':
                
                Company = ActionRoutes.mdlAllCompany.mgr_getOrgnames()
                
                for items in Company:
                        listcountbyCompany.append(blgetCompanyActionCount (items,openActionsQueSeries))
                            #dont need to append list as its already in the list above
               
                chartChanges.append(showPie(listcountbyCompany,Company, "Open Actions by Company"))
            if ActionsSorton == 'Discipline':
                
                discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
                listcountbyDisSub= []
                listlablesDisc =[]
                for itemPair in discsub:
        
                    listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,openActionsQueSeries))
                    listlablesDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
    
                chartChanges.append(showPie(listcountbyDisSub,listlablesDisc, "Open Actions by Disc/Sub-Disc"))
            
            if ActionsSorton == 'Workshops':
                workshops = Studies.objects.all()
                
                countbyStudies = []
                for x in workshops:

                    countbyStudies.append(blallActionCountbyStudies(x.StudyName,openActionsQueSeries))
                    countbyStudies.append(blallActionCountbyStudies(x.StudyName,closedActionsQueSeries))

                    
                    chartChanges.append(showPie(countbyStudies,labelsOpenClosed,x.StudyName))
                    #chart = showPie(listofOpenClosed,labelsOpenClosed,"Overall Studies Action Status")
                    
                    countbyStudies = []
                    #stripCount, striplabels ,  = st  ripAndmatch(countbyStudies,labels)
    
                    # For studies check if actually assigned to it or if count is 0 then just dont generate graph
                    #if stripCount != []:
            
                        #charts.append(showPie(stripCount,striplabels,StudyName))

        else: #This is for closed actions if selected
            chartChanges = []
            if ActionsSorton == 'Company':
                Company = ActionRoutes.mdlAllCompany.mgr_getOrgnames()
                
                for items in Company:
                        listcountbyCompany.append(blgetCompanyActionCount (items,closedActionsQueSeries))
                            #dont need to append list as its already in the list above
                chartChanges.append(showPie(listcountbyCompany,Company, "Closed Actions by Company"))

            if ActionsSorton == 'Discipline':
                
                discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
                listcountbyDisSub= []
                listlablesDisc =[]
                
                for itemPair in discsub:
        
                    listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,closedActionsQueSeries))
                    listlablesDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
    
                chartChanges.append(showPie(listcountbyDisSub,listlablesDisc, "Closed Actions by Disc/Sub-Disc"))
    
            if ActionsSorton == 'Workshops':
                workshops = Studies.objects.all()
                
                countbyStudies = []
                for x in workshops:

                    countbyStudies.append(blallActionCountbyStudies(x.StudyName,openActionsQueSeries))
                    countbyStudies.append(blallActionCountbyStudies(x.StudyName,closedActionsQueSeries))

                    
                    chartChanges.append(showPie(countbyStudies,labelsOpenClosed,x.StudyName))
                    #chart = showPie(listofOpenClosed,labelsOpenClosed,"Overall Studies Action Status")
                    
                    countbyStudies = []
    
    context = {
            "charts":charts,
            "chartChanges":chartChanges,
            "overall":True

    }
    return render (request, 'userT/reports.html',context ) #yhs checked

def rptdiscSlice(request, **kwargs):
    
    #Function on businees logic to get data based on Queseries, Actionee and Approver levels
    #most of the data is
    TotalCount = [0,1,2,3,4,5,6,7,8,9,99]  #yhs updated to make flexible path
    OpenAccount = [0,1,2,3,4,5,6,7,8,9]
    ApproverQList = [1,2,3,4,5,6,7,8,9]
    ActioneeQlist = [0]
    Company = ActionRoutes.mdlAllCompany.mgr_getOrgnames()
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg()

    
    listcountbyDisSub= []
    listlablebyDisSub =[]
    totalcountbyDisSub = []
    listofstringDiscSub =[]
    Title = "Open Actions by Discipline"
    label1 = "Open Actions"
    label2 = "Total Actions"
    generalxlabel = ""  #yhs removed
    
    labelActionee = "Actionee"
    labelApprover = "Approver"
    TitleActApp = "Actionee-Approver Open items"
    
    listofPairActioneeCount = []
    listofPairApproverCount = []
    discsub
    for itemPair in discsub:
        
        listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,OpenAccount))
        totalcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,TotalCount))
        listlablebyDisSub.append(str(itemPair[2]+"/"+ itemPair[0]+"/"+ itemPair[1])) # to include sub disc later -- +"/"+str(itemPair[1])
        listofstringDiscSub.append(str(itemPair[0]+"/"+ itemPair[1]))

        listofPairActioneeCount.append(blgetDiscSubActionCount ('Y',itemPair,[0]))
        listofPairApproverCount.append(blgetDiscSubActionCount ('Y',itemPair,ApproverQList))

    #cleaner to do a second loop
    
    listoflist = [[]]
    

    # for itemPair in discsub:
        
    #     routesfortheDiscpline = ActionRoutes.mdlgetActioneeAppr.mgr_getActApp(itemPair)

        
        
    #     for items in routesfortheDiscpline:
        
            
    #         listofPairActioneeCount.append(blgetDiscSubActionCount ('Y',itemPair,[0]))
    #         listofPairApproverCount.append(blgetDiscSubActionCount ('Y',itemPair,ApproverQList))
    #         listofPairNameCount.append(items.Actionee)
    #         
    #         listoflist.append(listofPairNameCount)
    #         listofPairNameCount = []
    Dispcount = len(listlablebyDisSub)
    chart = showbar(listcountbyDisSub,totalcountbyDisSub,listlablebyDisSub, label1,label2,generalxlabel,Title)
    chartChanges = showbar(listofPairActioneeCount,listofPairApproverCount,listlablebyDisSub,labelActionee,labelApprover,generalxlabel,TitleActApp )
    context = {
            "chart":chart,
            "chartChanges":chartChanges,
            "discpslice" : listofstringDiscSub,
            "Company" : Company, 
            "Dispcount": Dispcount
            }
    return render (request, 'userT/repdisc.html', context) #yhs changed all to smal lletters

def rptbyUser(request, **kwargs):
    dict_allRou = blgetuserRoutes(request.user.email)
    Actionee_R =    dict_allRou.get('Actionee_Routes')
    
    #This function just does a count using model managers , calling from businesslogic.py
    ActioneeCount = blfuncActionCount(Actionee_R,0)
    return render (request, 'userT/reports.html') #yhs checked
    
# def GeneratePDF (request):
#     filename = [] # for appending filename place before for loop
#     if (request.POST.get('GeneratePDF')):      
#         x=ActionItems.objects.all()  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
#         y= x.values()          
#         for item in y :            
#             i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file  
#             j = (i + '.pdf')  # easier to breakdown j           
#             del item["id"]      
#             data_dict=item       
#             x = 'static/multiple.pdf'             
#             out_file = 'static/media/' + j   # sending file to media folder inside static folder                                                        
#             generated_pdf = pypdftk.fill_form(
#                 pdf_path = x,
#                 datas = data_dict,
#                 out_file = out_file,                             
#             )
#             filename.append(str(generated_pdf)) #can only append str   
#             context={
#                  'filename' : filename,
#                  'table': True
#             }
                              
#         return render(request, 'userT/GeneratePDF.html', context)                    
#     return render(request, 'userT/GeneratePDF.html')

def ReportingTable(request):
    sub = Subscribe()
    if request.method == 'POST':
        #Msg=EmailMessage()
        sub = Subscribe(request.POST)
        subject = 'Test for sending email overview'
        message = 'A summary table should present here'
        recepient = str (sub ['Email'].value())
        Msg=EmailMessage(subject, message, emailSender, [recepient])
        Msg.content_subtype="html"
        Msg.attach_file('C:\\Users\\yh_si\\Desktop\\HSETool-1\\static\\multiple.pdf')
        Msg.send()
        context ={
          'form':sub
        }
        return render(request, 'userT/reportingtable.html',context) #yhs changed to small letters
    return render (request, 'userT/reportingtable.html', {'form':sub}) #yhs changed to small letters

#def EmailReminder (request):
#    return render(request, 'userT/EmailReminder.html')

def emailreminders(request):
    #sub = Subscribe()
    emaillist =[]
    #Get all Actions
    allactions = ActionItems.objects.all()
    if (request.POST.get('SendPending')):
        QueOpen = [0,1,2,3,4,5,6,7,8,9]
        QueClosed = [99]
        discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
        Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)   
        subject = f"Pending Activities for {paremailphase} Risk Assessment Workshops"
        content=f"You have Pending Actions in your Queue. Please go to {paremailurl} to attend to the actions." 
        for items in Indisets : 
            if items[3]>0:
                emaillist.append(items[0])
        blemailSendindividual(emailSender,emaillist,subject,content)
        #below is for the overdue, it is linked to button, just waiting for overdue function
    elif (request.POST.get('SendOverdue')):
          
        subject = f"Pending Activities for {paremailphase} Assessment Workshops"
        content=f"You have Overdue Actions in your Queue. Please go to {paremailurl} to attend to the actions." 
        blemailSendindividual(emailSender,emaillist,subject,content)

        return render (request, 'userT/emailreminders.html')
    return render (request, 'userT/emailreminders.html')
    
def EmailReminder(request):
    sub = Subscribe()
    if request.method == 'POST':
        
         #send email, the xyz is dummy data and not used
            
        
        sub = Subscribe(request.POST)
        recepient = str (sub ['Email'].value())
        
        dict_allRou = blgetuserRoutes(recepient)
        Actionee_R =    dict_allRou.get('Actionee_Routes')  
        ActionCount = blfuncActionCount(Actionee_R,0)
        
        totalaction=sum(ActionCount)
       
        #Msg=EmailMessage()
        sub = Subscribe(request.POST)
        subject = 'Template for Action Pending Responses'
        message = 'Clients template. Your pending responses are ' + str(totalaction) + ' actions.'
        
        Msg=EmailMessage(subject, message, emailSender, [recepient])
        Msg.content_subtype="html"
        Msg.send()
        context ={
          'form':sub
        }
        return render(request, 'userT/EmailReminder.html',context)  #edward to check this.....
    return render (request, 'userT/emailreminders.html', {'form':sub})

def EmailReminderAttachment(request):
    sub = Subscribe()
    if request.method == 'POST':
        #Msg=EmailMessage()
        sub = Subscribe(request.POST)
        subject = 'Template for sending out weekly report'
        message = 'Clients weekly report template & attachment.'
        recepient = str (sub ['Email'].value())
        Msg=EmailMessage(subject, message, emailSender, [recepient])
        Msg.content_subtype="html"
        Msg.attach_file('C:\\Users\yh_si\Desktop\HSETool-1\static\weeklyreporttemplate.pdf')
        Msg.send()
        context ={
          'form':sub
        }
        return render(request, 'userT/EmailReminder.html',context)
    return render (request, 'userT/EmailReminder.html', {'form':sub}) #edward to check this


    

def Profile (request):
    return render(request, 'userT/profile.html') #yhs changed to small letters

def repoverallexcel (request):
    #edward 20210804 excel
    
    all_actions =   ActionItems.objects.all().values()
    blank=[]

    dfalllist = blgetActionStuckAtdict(all_actions) # getting a list of everything
    # all_actionsopt = bladdriskcolourandoptiforflater(dfalllist, blank)
    dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format 
    dfallsorted = blsortdataframes(dfall,dfcompletecolumns) # sort dfall
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=AllActionDetails.xlsx' 
    in_memory = BytesIO()
    
    with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        dfallsorted.to_excel(writer, sheet_name='All Action Details',engine='xlsxwriter',header=False,startrow=1)
        workbook = writer.book #gives excelwriter access to workbook
        worksheet = writer.sheets['All Action Details'] #gives excelwriter access to worksheet
        formattedexcel = blexcelformat(workbook,worksheet,dfallsorted)

    in_memory.seek(0)    
    response.write(in_memory.read())
    #edward 20210804 excel end

    #edward 20210804 original excel commented out bcs replacing with dfexcel
    # workbook = excelCompleteReport(request) 
    # response = HttpResponse(content_type='application/ms-excel') #
    # response['Content-Disposition'] = 'attachment; filename=AllActionDetails.xlsx' 
    # workbook.save(response) # odd  way but it works - took too long to figure out as no resource on the web 
    #edward end 20210804 original excel commented out bcs replacing with dfexcel
    
    return response
    
def repPMTExcel (request):
    

    #latest first
    
    #Signatories = 
    #get individual actions
    QueOpen = [0,1,2,3,4,5,6,7,8,9]
    
    QueClosed = [99]
    YetToRespondQue =[0]
    ApprovalQue = [1,2,3,4,5,6,7,8,9]
    TotalQue = [0,1,2,3,4,5,6,7,8,9,99]
    discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
    
    #***Start Pie Chart Guna
    allOpenActions= blfuncgetallAction('Y', QueOpen)
    allClosedActions = blfuncgetallAction('Y', QueClosed)
    
    # forpie2 = [
    #       ['OpenClosed', 'Open Closed'],
    #       ['Open',     allOpenActions],
    #       ['Closed',      allClosedActions],
          
    #     ]
    forpie=[]
    #this is for overall charts
    #listofOpenClosed = [allOpenActions,allClosedActions]
    labels = ['Open', 'Closed']
    values = [allOpenActions,allClosedActions]
    
    pienameoverall = "Open/Closed Actions"
    googlechartlistoverall = blprepGoogChartsbyStudies(labels,values,pienameoverall)
    forpie.append(googlechartlistoverall)
    
    #Open action by organisation
    labelsorg = ActionRoutes.mdlAllCompany.mgr_getOrgnames()
    countorg =[] 
    pienameorg = "Open Actions by Organisation"          
    for items in labelsorg:
            countorg.append(blgetCompanyActionCount (items,QueOpen))
    googlechartlistorganisation = blprepGoogChartsbyStudies(labelsorg,countorg,pienameorg)
    forpie.append(googlechartlistorganisation)

    #Submitted actions by organisation
    pienamesubmitted = "Submitted Actions by Organisation" 
    countsubmitted =[]         
    for items in labelsorg:
            countsubmitted.append(blgetCompanyActionCount (items,ApprovalQue))
    
    googlechartlistsubmitted = blprepGoogChartsbyStudies(labelsorg,countsubmitted,pienamesubmitted)
 
    forpie.append(googlechartlistsubmitted)

    # Open Actionsfor discipline
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
    countdiscsub= []
    labelsDisc =[]
    pietitledisc = "Open Actions by Discipline"
    for itemPair in discsub:
        
        countdiscsub.append(blgetDiscSubActionCount ('Y',itemPair,QueOpen))
        labelsDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
    
    googlechartlistdiscipline = blprepGoogChartsbyStudies(labelsDisc,countdiscsub,pietitledisc)

    forpie.append(googlechartlistdiscipline) 
    #By workshops - Overall OPen actions by Studies
    labelsworkshop = Studies.objects.all()
                
    countstudies = []
    labelsstudies = []
    pietitlestudies = "Open Actions by Studies"

    for study in labelsworkshop:

        countstudies.append(blallActionCountbyStudies(study.StudyName,QueOpen))
        labelsstudies.append(study.StudyName)
    googlechartliststudies = blprepGoogChartsbyStudies(labelsstudies,countstudies,pietitlestudies)
   
    forpie.append(googlechartliststudies)


    # Open Actions by Workshop   
  
    #***End Pie Guna
    #get Individual action

    # Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)   
    # tableindiheader = ['User','Role','Organisation Route','In-Progress','Closed', 'Open Actions']

    Indisets = blgetIndiResponseCount2(discsuborg,QueOpen,QueClosed) 
    # tableindiheader = ['User','Role','Organisation Route','Yet-to-Respond','Yet-to-Approve','Closed', 'Open Actions']  
    tableindiheader = ['User','Role','Organisation Route','Pending Submission','Pending Approval','Closed', 'Open Actions'] #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
    
    #getsummaryactions
    #edited by edward 20210706 to only show yet to approve & yet to respond
    # listaggregatedindi,listaggregatedindiheader=blgroupbyaggsum(Indisets,tableindiheader,'User', ['Yet-to-Respond','Yet-to-Approve','Closed','Open Actions])
    listaggregatedindi,listaggregatedindiheader=blgroupbyaggsum(Indisets,tableindiheader,'User', ['Pending Submission','Pending Approval']) #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
    
    allactions = ActionItems.objects.all()
    
    rem_list = []

    
    # dfRiskMatrix = pd.DataFrame(list(RiskMatrix.objects.all().values()))
    #     #print (dfRiskMatrix[['Combined','RiskColour']])
        
   
        
    # for items in allactions:
    #             [items.pop(key) for key in rem_list] # Reducing the data going to html
    #             #
    #             RiskColour = dfRiskMatrix.loc[dfRiskMatrix['Combined'].isin([items.get('InitialRisk')]),'RiskColour'].tolist() #cant use .item() as its causing an error when not matching
                
    #             if RiskColour:
    #                 items['RiskColour'] = RiskColour[0]
    #             else: 
    #                 items['RiskColour'] = False
    
    


    tableallheader = ['id','StudyActionNo','StudyName', 'Disipline' ,'Recommendations', 'Response','DueDate','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
    lstofallactions = blgetActionStuckAt(allactions, tableallheader) #basically you feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
    tableallheadermodified = ['Study Action No','Study Name', 'Discipline' ,'Recommendations', 'Response','Due Date','Initial Risk']
    
    # # # edward 20210803 dataframes excel
    # all_actions =   ActionItems.objects.all().values()#'StudyActionNo','StudyName','ProjectPhase', 'Facility','Guidewords', 'Deviation', 'Cause', 'Consequence', 'Safeguard','InitialRisk','ResidualRisk', 'Disipline' ,'Recommendations','DueDate', 'Response','FutureAction')
    # rem_list2 = ['QueSeries','QueSeriesTarget','DateCreated'] #OPtimising data to be removed
    # blank=[]
    # all_actionsopt = bladdriskcolourandoptiforflater(all_actions, blank)
    # dfall1 = pd.DataFrame.from_dict(all_actionsopt) # sort dfall
    # dfall = blsortdataframes(dfall1,dfallcolumns)
    # # # edward end 20210803 dataframes excel
    
    #RejectDetails - gonna use a different way same way as actionne list
    #just using revision way to get all rejected actions
    revisiononwards = 1
    queseries = 0
    rejectedactions = ActionItems.mdlgetActionDiscSubCount.mgr_getAllRejectedItems(revisiononwards,queseries)
    rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated'] #OPtimising data to be removed
    rejectedallactionitems = bladdriskcolourandoptiforflater(rejectedactions,rem_list)
    dfrejection = pd.DataFrame.from_dict(rejectedallactionitems)


    #lstofrejectedforexcel = blgetActionStuckAt(rejectedactions, tableallheader)
    #for Disipline based view
    tabledischeader = ['Discipline', 'Yet to Respond' ,'Approval Stage', 'Closed','Open Actions','Total Actions']
    lstbyDisc= blaggregatebyDisc(discsuborg,  YetToRespondQue, ApprovalQue,QueClosed,QueOpen,TotalQue)
    

    #get rejected summary actions get Reject Table
    tablerheaderejected = ['Discipline', 'Rejected Count']
    listofrejecteditems = blgetrejectedcount(discsuborg,1) #Pass revision number => than whats required
    

    #for workshop based view
    allstudies = Studies.objects.all()
    tablestudiesheader = ['Studies', 'Yet to Respond' ,'Approval Stage','Closed','Open Actions', 'Total Actions']
   
    lstbyWorkshop = blgetbyStdudiesCount(allstudies,YetToRespondQue,ApprovalQue,QueClosed,QueOpen,TotalQue)
    
    #edward 20210708 printing here to see
    #due date based view
    tableduedateheader = ['Due Date','Actions to Close by']
    lstbyDueDate= blaggregatebydate(ActionItems.objects.all())
    
    subtotal =[]
    for items in lstbyDueDate:
       subtotal.append(items['count']) #how to access dictionary object by
    
    totalallDueDate = sum(subtotal)
    
    lstbyDueDate    = blaggregatebydate(ActionItems.objects.all())
    
    lstplanned         =  blprepareGoogleChartsfromDict(lstbyDueDate)
    lstactual      = blgetActualRunDown(lstplanned) # shows how many closed
    
    newlist = blformulateRundown(lstplanned,lstactual)
    #edward 20210727 rundown
    newliststop = blstopcharttoday(newlist)
    #edward end 20210727 rundown
    if request.method == 'POST':
                
        if (request.POST.get('allActions')):
          
            #edward 20210803 dataframes excel
            # in_memory = BytesIO()
            # workbook = dfall.to_excel(in_memory)
            #edward end 20210803 dataframes excel

            tableallheader.append("Current Actionee/Approver") #appends the last column that the list spits out #yhs changed from tableallheader to tableallheadermodified
            workbook = excelAllActions(lstofallactions,tableallheader,"All Action Items",1) #optional parameter passed to remove excel columns if required
            response = HttpResponse(content_type='application/ms-excel') #
            response['Content-Disposition'] = 'attachment; filename=byAllActions.xlsx' 
            workbook.save(response) # odd  way but it works - took too long to figure out as no resource on the web

            #edward 20210803 dataframes excel
            # in_memory.seek(0)    
            # response.write(in_memory.read())
            #edward end 20210803 dataframes excel

            return response
        elif (request.POST.get('rejectedactions')):
            
            in_memory = BytesIO()
            workbook = dfrejection.to_excel(in_memory)
            #just use memory and workbook is redundant
            response = HttpResponse(content_type='application/ms-excel') #
            response['Content-Disposition'] = 'attachment; filename=byRejectedActions.xlsx' 
            in_memory.seek(0)    
            response.write(in_memory.read())
            
            return response

        elif (request.POST.get('indisummary')):
            

            workbook = excelAllActions(listaggregatedindi,listaggregatedindiheader,"Individual Summary") 
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=byIndividualSummary.xlsx' 
            workbook.save(response) 
            return response

        elif (request.POST.get('indiActions')):
            

            workbook = excelAllActions(Indisets,tableindiheader,"Individual Actions") 
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=byIndividual.xlsx' 
            workbook.save(response) 
            return response

        elif (request.POST.get('allStudies')):
            
            workbook = excelAllActions(lstbyWorkshop,tablestudiesheader,"Workshop Actions")
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=byStudies.xlsx' 
            workbook.save(response) 
            return response
        
        elif (request.POST.get('bydiscipline')):
            
           
            workbook = excelAllActions(lstbyDisc,tabledischeader,"Discipline Actions")
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=byDiscipline.xlsx' 
            workbook.save(response) 
            return response

        elif (request.POST.get('byDueDate')):
            
            reallstDuedate = blquerysetdicttolist(lstbyDueDate) #need a list
            workbook = excelAllActions(reallstDuedate,tableduedateheader,"DueDates") 
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=byDueDates.xlsx' 
            workbook.save(response) # odd way but it works - took too long to figure out as no resource on the web
            return response    
     
    riskmatrix = blgetRiskMatrixColour()
        
    context = {
        
        'riskmatrix' : riskmatrix,
        'forpie' : forpie,
        'lstbyDueDate' : lstbyDueDate,
        'tableduedateheader' : tableduedateheader,
        'totalallDueDate' : totalallDueDate, 
        'rundowncontent': newliststop, #edward 20210727 rundown
        'lstbyDisc' : lstbyDisc,
        'lstbyWorkshop' : lstbyWorkshop,
        'Indisets' : Indisets,
        'lstofallactions' : lstofallactions,
        'tableindiheader' : tableindiheader,
        'tablestudiesheader' : tablestudiesheader,
        'tabledischeader' : tabledischeader ,
        'tableallheader' : tableallheadermodified,
        'listaggregatedindi':listaggregatedindi,
        'listaggregatedindiheader':listaggregatedindiheader,
        'listofrejectedheader': tablerheaderejected,
        'listofrejecteditems': listofrejecteditems,
        "rejectedactions": rejectedallactionitems,
    
        
    }
    return render(request, 'userT/reppmtexcel.html', context)

def DisciplineBreakdown (request):
    return render(request, 'userT/disciplinebreakdown.html')#yhs changed to small letters
 
def StickyNote(request):
    return render(request, 'userT/stickynote.html') #yhs changed to small letters


# def PDFtest(request):
#     run()
#     return HttpResponse('TEST')

#this part need to be tidied up. For time's sake i just copy from def (repPMTExcel). by YHS
def closeoutprint(request,**kwargs):
   
    ID = (kwargs["id"])
    
    obj = ActionItems.objects.filter(id=ID).values() # one for passing into PDF
    objFk =ActionItems.objects.get(id=ID) # this is for getting all attachments

    ObjAttach = objFk.attachments_set.all()  #get attcahments from foreign key
    
    
    studyActionNo =  objFk.StudyActionNo
    replacestudyActionNo= studyActionNo.replace("/","_")
    Filename = replacestudyActionNo  + ".pdf"
    #edward new tempfolder from parameters
    out_file = tempfolder + Filename
       
    data_dict=obj[0]
    
    discsub = blgetDiscSubOrgfromID(ID)
    Signatories = blgetSignotories(discsub)
    
  
    lstSignatoriesTimeStamp= blgettimestampuserdetails (ID, Signatories) #edward changed this to use new bl for signature 20210706
    signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp)
    
    newcloseouttemplate = blsetcloseouttemplate (ID)

    file = pdfgenerate(newcloseouttemplate,out_file,data_dict,signatoriesdict)
    
    in_memory = BytesIO()
    
    zip = ZipFile(in_memory,mode="w")
    
    for eachfile in ObjAttach:
        filename = os.path.basename(eachfile.Attachment.name)
        zip.write (eachfile.Attachment.path, "Attach_"+filename)
    
    closeoutname = os.path.basename(out_file) 
    zip.write (out_file, closeoutname)
    zip.close()

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=" + studyActionNo+ ".zip"

    in_memory.seek(0)    
    response.write(in_memory.read())
    
    
    #dont delete below as its a way to actualy read from memory can be used elsewhere
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #bufferfile = pdfsendtoclient ('atrtemplateautofontreadonly.pdf',data_dict)
    #edward changed file location to parameters
 
   #return FileResponse(bufferfile, as_attachment=True, filename=out_file)
    
    return response
  
def closeoutsheet(request): #new naming convention - all small letters
    QueOpen = [0,1,2,3,4,5,6,7,8,9]
    QueClosed = [99]
    YetToRespondQue =[0]
    ApprovalQue = [1,2,3,4,5,6,7,8,9]
    TotalQue = [0,1,2,3,4,5,6,7,8,9,99]
    allstudies = Studies.objects.all()

    tablestudiesheader = ['Studies', 'Yet to Respond' ,'Approval Stage','Closed','Open Actions', 'Total Actions']
   

    
    lstbyWorkshop = blgetbyStdudiesCount(allstudies,YetToRespondQue,ApprovalQue,QueClosed,QueOpen,TotalQue)

    allactions = ActionItems.objects.all()
    tableallheader = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','Response','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
    lstofallactions = blgetActionStuckAt(allactions, tableallheader) #basically you feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
    tableallheadermodified =  ['Study Action No','Study Name', 'Discipline' ,'Recommendations','Response','Initial Risk'] 
    filename = [] # for appending filename place before for loop
    
    #Guna

    lstclosed = ActionItems.objects.filter(QueSeries =99)
 
    if (request.POST.get('GeneratePDF')): 
        x=ActionItems.objects.all()  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
       
        y= x.values()          
        for item in y :            
            i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file  
            j = (i + '.pdf')  # easier to breakdown j & to append further on          
            del item["id"]      
            data_dict=item
            out_file = staticmedia + j
            pdfgenerate(atrtemplate,out_file,data_dict)#returns from pdfgenerator #edward added atrtemplate location in parameters
            filename.append(j) #can only append str, appending j shows the filename for userview instead of whole location 
            context1={
                'filename' : filename,
                'table': True,
                'lstbyWorkshop' : lstbyWorkshop,
                'lstofallactions' : lstofallactions,
            }
        return render(request, 'userT/closeoutsheet.html', context1)                    
    

    context = {
        'lstclosed' : lstclosed,
        'lstbyWorkshop' : lstbyWorkshop,
        'lstofallactions' : lstofallactions,
        'tablestudiesheader' : tablestudiesheader,
        
    }

    return render(request, 'userT/closeoutsheet.html', context)

# def closeoutsheet(request):
#     filename = [] # for appending filename place before for loop
#     if (request.POST.get('GeneratePDF')): 
#         x=ActionItems.objects.filter(StudyName='HAZID')  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
#         y= x.values()          
#         for item in y :            
#             i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file  
#             j = (i + '.pdf')  # easier to breakdown j           
#             del item["id"]      
#             data_dict=item
#             out_file = 'static/media/' + j
#             pdfgenerate('atrtemplateautofontreadonly.pdf',out_file,data_dict)
#             filename.append(out_file) #can only append str   
#             context={
#                 'filename' : filename,
#                 'table': True
#             }
#             #return HttpResponse('TEST')
#         #     return render(request, 'userT/closeoutsheet.html', context)
#         # return render(request, 'userT/closeoutsheet.html')
#         return render(request, 'userT/closeoutsheet.html', context)                    
#     return render(request, 'userT/closeoutsheet.html')
        

# for  making view all actions clickable & obtain the id using update view


class pmtrepviewall(UpdateView): 
    template_name = "userT/reppmtviewall.html" #the html is missing object_list
    form_class = ApproverForm

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['id'])

    def get_context_data(self,**kwargs):
        idAI = self.kwargs.get("id")
        context = super().get_context_data(**kwargs)
        discsub = blgetDiscSubOrgfromID(idAI)
        Signatories = blgetSignotories(discsub)

        
        #There is an error going on here or so to speak as its calling ActioneeItemsMixin as well odd error and cant narrow it down
        #edward 20210707 trying to use consolidated version blgettimestampuserdetails
        lstSignatoriesTimeStamp= blgettimestampuserdetails (idAI, Signatories) #it changes the signatories directly
        object_list = self.object.attachments_set.all() #-this one gets the the attachments and puts it into Object_List, edward added attachments
        rejectcomments = self.object.comments_set.all() #edward added new way of getting rejectcomments 
        #edward added attachments
        context['object_list'] = object_list #attachments are foreign key
        # context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(idAI) #edward-> its another way of getting ForeignKey elements using filters
        context['Rejectcomments'] = rejectcomments
        context ['Signatories'] = lstSignatoriesTimeStamp
        
        return context
 

#yhs testing to print individual pdf on actionee page
def indiprint(request,**kwargs):
    ID = (kwargs["id"])
    obj = ActionItems.objects.filter(id=ID).values() # one for passing into PDF
    objFk =ActionItems.objects.get(id=ID) # this is for getting all attachments
    ObjAttach = objFk.attachments_set.all()  #get attcahments from foreign key
    studyActionNo =  objFk.StudyActionNo
    replacestudyActionNo= studyActionNo.replace("/","_")
    Filename = replacestudyActionNo  + ".pdf"
    #edward new tempfolder from parameters
    out_file = tempfolder + Filename
       
    data_dict=obj[0]
 
   
    #There is an error going on here or so to speak as its calling ActioneeItemsMixin as well odd error and cant narrow it down
        
    #dont delete below as its a way to actualy read from memory
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #bufferfile = pdfsendtoclient ('atrtemplateautofontreadonly.pdf',data_dict)

    newcloseouttemplate = blsetcloseouttemplate (ID)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=" + studyActionNo+ ".pdf"
    #edward changed file location to parameters
    file = pdfsendtoclient(newcloseouttemplate, data_dict)
    response.write(file.read())
    return response
   
   #return FileResponse(bufferfile, as_attachment=True, filename=out_file)

#yhs added
def delegatedadmin (request):
    return render(request, 'userT/delegatedadmin.html')#yhs changed to small letters
#edward scheduler
# def scheduler (request):
#     Command()
#     return HttpResponse('TEST')
