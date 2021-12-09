from django.db.models.fields import NullBooleanField
from django.http import response
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from numpy import empty
from .forms import *
from UploadExcel.forms import *
from django.contrib.auth import get_user_model
import matplotlib as plt
from .businesslogic import *
from .businesslogicQ import *
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
from rest_framework import generics
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
#edward 20210924
from django.forms.models import model_to_dict
from django.db.models import F
#edward 20211027 bulk pdf fix for large file dl
from django.http import StreamingHttpResponse
#edward 20211122 stitch pdf
import xlwings as xw
#20211202 edward commented out this import because there is a problem with img2pdf library on linux
# import img2pdf
# from PIL import Image
#edward 20211207 
from datetime import datetime as dtime
from django.utils import timezone


def base3 (request):
    """This function is to view base3.html while editing the html"""
    
    return render(request,'userT/base3.html')

def sidebar (request):
    
  return render(request, 'userT/basesidebar.html')

class actionlist(generics.ListCreateAPIView):
    pass


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
    
    content1 = [['By Studies', '///Open Actions by Organisation:::'], ['RWP', 13], 
                ['HESS', 20], ['SFSB', 2], ['MMHE', 28]]

    context = {

         'content' : content1,
    #     'charttitles' : "XYZ"


     }
    context['XYZ'] = json.dumps([{

                    "data" : [[{
                                "Feature1" : "Open Action by organisation",
                                "Feature2" : "No: Open"},
                                {
                                "Feature1" : "MMHE","Feature2" : 28
                                },{
                                "Feature1" : "SFSB","Feature2" : 2
                                },{
                                    "Feature1" : "HESS","Feature2": 20
                                },
                                {
                                    "Feature1" : "RWP","Feature2": 20
                                }],[
                                    {
                                "Feature1" : "Open/Closed Actions", "Feature2" : "Open Closed"},
                                {
                                "Feature1" : "Open",
                                "Feature2" : 192
                                },

                                {
                                "Feature1" : "Closed",
                                "Feature2" : 12
                                },
                                ]
                            ]
                }])
    
    data=  [[['By Studies', '///Open/Closed Actions:::'], ['Open', 220], ['Closed', 12]], 
            [['By Studies', '///Open Actions by Organisation:::'], ['HESS', 20], ['MMHE', 28], ['RWP', 13], ['SFSB', 2]],
            [['By Studies', '///Submitted Actions by Organisation:::'], ['HESS', 12], ['MMHE', 16], ['RWP', 6], ['SFSB', 0]],
            [['By Studies', '///Open Actions by Discipline:::'], ['HUC', 19], ['Operations', 7], ['Drilling', 7], ['EHS', 1], ['EHS', 1], ['Safety', 9], ['Marine', 6], ['Electrical', 71], ['Commissioning', 3], ['Mechanical', 2], ['MARINE', 6], ['EHS', 0]],
            [['By Studies', '///Open Actions by Studies:::'], ['MRU Barge Campaign Post Shutdown - Phase3', 34], ['HAZID', 19], ['HAZOP', 2], ['CRA-DPDSV/PRECOMM', 0], ['Environmental Impact Identification (ENVID)', 0], ['Hazard Identification (HAZID) Study', 0], ['Hazard and Operability (HAZOP) Study', 0], ['SAFOP Report', 75], ['NMB Phase 4A Concept Definition - HAZID Report', 28], ['NMB Phase 4A Concept Definition', 34]]]

    featuresfields = ["Feature1", "Feature2"]
    data2=[]
    data3 =[]
    #for items in data:
        # for xyz in items:
        #     data1 = dict(zip(featuresfields,xyz))
        #     data2.append(data1)

        # data2= [dict(zip(featuresfields,pies)) for pies in items]
        
        # data3.append(data2)
        # data2=[]
    data3 = blmakelistforjson(data,featuresfields)
    
    context['XYZ'] = json.dumps([{"data":data3}])
 
       
    return render(request, 'userT/googlecharts.html',context) 

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

    content1 = blstopcharttoday(content)

    context = {

        'content' : content1

    }

    return render(request, 'userT/googlecharts88.html',context) #ok checked by yhs
# edward 20210713 end new chart

def mainDashboard (request):
    """ My Dashboard view. Rewrite Nov 21. The starting point  or at main uses this view
    1. Get all studies first. not using phases at this stage at this is more for an individual dashboard 
    2. Get routes and separate them to actionee or approver routes
    """
    usersemail=request.user.email
    ActioneeActions = []
    queActionee = 0
    Actionee_R = []
    Approver_R = []
    totalactioneeaction = 0
    studies = blgetAllStudies()
    #get all routes based on email and then get seprate actione and approver routes 
    dict_allrou = blgetuserRoutes(usersemail)
    Actionee_R =    dict_allrou.get('Actionee_Routes')
    Approver_R =    dict_allrou.get('Approver_Routes')
    
    reducedfileds= ['id','StudyActionNo','Disipline' ,'QueSeries', 'DueDate','InitialRisk']
    #ActioneeActions = blallActionsComDisSub(Actionee_R,0)
    ActioneeActions = blallactionscomdissubQ(Actionee_R,queActionee,reducedfileds)
    totalactioneeaction = blfuncActionCountQ(Actionee_R,YetToRespondQue)
    totalactionssubmitted = blfuncActionCountQ(Actionee_R,ApprovalQue)
    
    rejecteditemsid = blRejectedHistortyActionsbyId(usersemail,queActionee,1)
    countrejected = bldropduplicateandcount(rejecteditemsid)
   
    submittedsummary = {'totalactionssubmitted':totalactionssubmitted,'countrejected':countrejected }

    rem_list = []   
    ActioneeActionsrisk = bladdriskelements(list(ActioneeActions))
    riskrankingsummary =  blaggregateby(ActioneeActionsrisk,"RiskRanking")
    duedateaggregated = blaggregateby(ActioneeActionsrisk,"DueDate")
    duedatesummary = blduedateecountrelative(duedateaggregated)

    
    
    


    #***Initilise empty list to hold values
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
        stripCount, striplabels ,  = stripAndmatch(countbyStudies,labels)

        # Just to get a better view in HTML instead of rendering spaces for empty charts
        if stripCount != [] : 
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
        #empties out the data for next loop otherwise it doubles the data to append on each study
        chartappdata = []

        dataApprover = []
        labelsApprover =[]
        countbyStudies = []

        
    # #20211207 edward current holding time & days holding
    strdays = bltotalholdtime(ActioneeActions,Approver_R,reducedfileds,queActionee)
    oneweekcount,twoweekcount = blexceedholdtime(ActioneeActions,Approver_R,queActionee,reducedfileds)
    #     #20211207 edward current holding time & days holding ends here
    
    totalapproveraction = sum (appractioncount)
   
    approverjsonlist = blremoveemptylist(apprfinalist)
    
    Context = {
        'oneweekcount':oneweekcount,
        'twoweekcount':twoweekcount,
        'strdays':strdays,
        'totalapproveraction' : totalapproveraction,
        'totalactioneeaction' : totalactioneeaction,
        #'actioneefinallist' : actioneefinallist, #substituted with json data below
        #'apprfinalist' : apprfinalist, #substituted with json data below
        "pieactioneenew" : json.dumps([{"data":actioneefinallist}]),
        "pieapprovernew" : json.dumps([{"data":approverjsonlist}]),
        "riskrankingsummary":riskrankingsummary,
        "duedatesummary":duedatesummary,
        "submittedsummary": submittedsummary
            }
    
    return render(request, 'userT/maindashboard.html',Context) 




class ActioneeList (ListView):
    """This class is for Your Actions/Actionee list, basically uses email to get all actions within actionee routes 
    And then assigns a colour on it. Returns the queryset and context into object_list(default django)"""

    template_name   =   'userT/actionlistactionee.html'

    def get_queryset(self):

        userZemail = self.request.user.email
        queactionee = 0
        ActioneeRoutes =[]
        ActioneeActions =[]
        ActioneeRoutes =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
        reducedfileds= ['id','StudyActionNo','StudyName__StudyName','Disipline' ,'Subdisipline','Cause','Recommendations',
        'QueSeries', 'DueDate','InitialRisk']
        ActioneeActions = blallactionscomdissubQ(ActioneeRoutes,queactionee,reducedfileds)
        finalactionitems = bladdriskelements(list(ActioneeActions))
        return ActioneeActions

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['riskmatrix'] = blgetRiskMatrixColour()

        return context

class HistoryList (ListView):
    """Populates what you have done under History under Your Actions"""
    template_name   =   'userT/historylist.html' 

    def get_queryset(self):
        #historically only get queue for all approver levels that he person is the actionee instead of everything else
        userZemail = self.request.user.email

        dict_allRou = blgetuserRoutes(userZemail)

        #Just get Actionee and Approver Routes, tied into model managers
        Actionee_R =    dict_allRou.get('Actionee_Routes')
        lstgetHistoryforUser             = blgetHistoryforUser(userZemail,Actionee_R)

        #the sequence just appends risk matrix colours
        #rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated']
        finalactionitems = bladdriskcolourandoptimise(lstgetHistoryforUser)

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

        #rem_list = ['Consequence','FutureAction','Deviation','QueSeries','QueSeriesTarget','DateCreated']

        #addriskcolour to approver list
        finalappractionitems= bladdriskcolourandoptimise(approverflatdict)

        rejecteditemsid = blRejectedHistortyActionsbyId(userZemail,0,1)
       
        # Need to make a list to feed into bladdriskcolourandoptimise as that function is expecting a list of dictionaries
        rejecteditemsbyhistory = [blgetActionItemsbyid(rejecteditemsid)]
        newrejecteditemsbyhist                        = bladdriskcolourandoptimise(rejecteditemsbyhistory)
        context['rejectedhistory'] = rejecteditemsbyhistory
        context['approveractions'] = finalappractionitems

        return context

class ApproverList (ListView):
    
    """This is the view under Your actions and when you click Approver Actions. It gives all 
    approver actions across multiple que series. Get routes that maps against que series and then use """
    template_name   =   'userT/actionlistapprover.html'

    def get_queryset(self):

        userZemail = self.request.user.email
        ApproverActions = []
        ApproverActionsX = []
        dict_allRou = blgetuserRoutes(userZemail)
        #gets approver routes by que series and slots QuerySet for routes according to key dict Approver Routes
        Approver_R =    dict_allRou.get('Approver_Routes')
        reducedfileds= ['id','StudyActionNo','StudyName__StudyName','Disipline' ,'Subdisipline','Cause','Recommendations',
        'QueSeries', 'DueDate','InitialRisk']
        for key, value in Approver_R.items():

            # allactionItems= blallActionsComDisSub(value,key)
            # ApproverActions.insert(key,allactionItems)
            
            allactionItems= blallactionscomdissubQ(value,key,reducedfileds)    
            finalactionitems = bladdriskelements(list(allactionItems))
            ApproverActions.insert (key,allactionItems)
        
       
        # for items in ApproverActions:
        #     #have to do a loop as its adding another level compared to actionee
        #     #rem_list removed from equation as now its getting only relevant data
        #     finalactionitems= bladdriskelements(items,[]) #The way python works its not using this finally but editing ApproverActions directly
        
        

        return ApproverActions
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #change the codes to just make it read the count and say if there is a table uploaded
        #Nov 21, need to apply to rest as well
        #context['riskmatrix'] = blgetRiskMatrixColour()
        context['riskmatrix'] = blgetriskmatrixtable()

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
            #if delete function required for approver to copy from actioneemixin
            pass

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
            Signatoryemails = blgetSignatoryemailbyque(discsub,integerqueseries+1)
            ContentSubject  = blbuildSubmittedemail(ID,"Approver")#change the function call to try and have code standardised #blbuildApprovedemail(ID) # using new bl since approver email should be this has been approved instead of submitted
           
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
            AttachmentID = self.request.POST.get ('Delete') 
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

            Signatoryemails = blgetSignatoryemailbyquereject(discsub,intqueseries)
            ContentSubject  =blbuildSubmittedemail(ID,"Reject",rejectreason)
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
        Signatoryemails = blgetSignatoryemailbyque(discsub,newQueSeries) # edward 20210709 altered this to use with new bl


        ContentSubject  =blbuildSubmittedemail(ID,"Actionee")

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


def repoverallexcel (request):
    #edward 20210929 excel
    """Provides the Download Complete Excel Feature in PMT Reporting"""
    #have to try passing in all values of fk instead of specifying just one 
    all_actions =   ActionItems.objects.all().values()
    all_actionwithfk = blannotatefktomodel(all_actions)
    
    dfalllist = blgetActionStuckAtdict(all_actionwithfk) # getting a list of everything
    # all_actionsopt = bladdriskelements(dfalllist, blank)
    dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
    dfallsorted = blsortdataframes(dfall,dfcompletecolumns) # sort dfall

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=AllActionDetails.xlsx'
    in_memory = BytesIO()

    with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        dfallsorted.to_excel(writer, sheet_name='All Action Details',engine='xlsxwriter',header=False,startrow=1)
        workbook = writer.book #gives excelwriter access to workbook
        worksheet = writer.sheets['All Action Details'] #gives excelwriter access to worksheet
        formattedexcel = blexcelformat(dfallsorted,workbook,worksheet)
        
    in_memory.seek(0)
    response.write(in_memory.read())
    #edward 20210929 excel end

    return response

    
def repPMTExcel (request,phase=""):
    """This is the original function called when user selects PMT Reporting from menu
    It dumps all actions into this function """
    
    #added for phases - Get all phases from Phases table for Html
    listofPhases= Phases.mdlSetGetField.mgrGetAllActionsAndFields()
    #20211202 edward previous discsuborg was looping through the AR table, changed to temporarily use dfdiscsuborgphase which uses DF to sort actions by phase
    discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() 
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
    
    organisationnames = ActionRoutes.mdlAllCompany.mgr_getOrgnames()

    #20211201 edward this one replaces discsuborg
    dfdiscsuborgphase = bldfdiscsuborgphase(phase)

    #1st Pie Overall Actions Open/Closed
    forpie=[]
    PhaseOpenActions= blallphasegetAction(QueOpen,phase)
    PhaseClosedActions = blallphasegetAction(QueClosed,phase)
    labelpie =['Open', 'Closed']
    titlepie = "Open/Closed Actions"
    googlechartlistoverphase= blprepGoogChartsbyStudies(labelpie,[PhaseOpenActions,PhaseClosedActions],titlepie )
    forpie.append(googlechartlistoverphase)
    
    #2nd Pie Open action by organisation
    countorg =[] 
    titleorg = "Open Actions by Organisation"          
    for items in organisationnames:
            countorg.append(blgetCompanyActionCountPhase (items,QueOpen,phase))
    googlechartlistorganisation = blprepGoogChartsbyStudies(organisationnames,countorg,titleorg)
    forpie.append(googlechartlistorganisation)

   #3rd Pie Submitted actions by organisation
    titlesubmitted = "Submitted Actions by Organisation" 
    countsubmitted =[]         
    for items in organisationnames:
            countsubmitted.append(blgetCompanyActionCountPhase (items,ApprovalQue,phase))
    googlechartlistsubmitted = blprepGoogChartsbyStudies(organisationnames,countsubmitted,titlesubmitted)
    forpie.append(googlechartlistsubmitted)

    #4th Pie Open Actions for discipline
    countdiscsub= []
    labelsDisc =[]
    titledisc = "Open Actions by Discipline"
    
    for itemPair in discsub:
        countdiscsub.append(blgetDiscSubActionCountPhase (itemPair,QueOpen,phase))
        labelsDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
    googlechartlistdiscipline = blprepGoogChartsbyStudies(labelsDisc,countdiscsub,titledisc)
    forpie.append(googlechartlistdiscipline) 

    #5th Pie  Overall Open actions by Studies
    labelsworkshop = Studies.objects.all()        
    countstudies = []
    labelsstudies = []
    titlestudies = "Open Actions by Studies"

    for study in labelsworkshop:
        countstudies.append(blallActionCountbyStudiesPhaseQ(study.StudyName,QueOpen,phase))
        labelsstudies.append(study.StudyName)
    googlechartliststudies = blprepGoogChartsbyStudies(labelsstudies,countstudies,titlestudies)
    forpie.append(googlechartliststudies)
    #***End Pie Guna

    #20211201 edward remove discsuborg here because using discsuborg in bl
    Indisets = blgetIndiResponseCount2(dfdiscsuborgphase,QueOpen,QueClosed,phase) 
    
                
    # tableindiheader = ['User','Role','Organisation Route','Yet-to-Respond','Yet-to-Approve','Closed', 'Open Actions']
    tableindiheader = ['User','Role','Organisation Route','Pending Submission','Pending Approval','Closed', 'Open Actions'] #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
    
    
    #edited by edward 20210706 to only show yet to approve & yet to respond
   
    listaggregatedindi,listaggregatedindiheader=blgroupbyaggsum(Indisets,tableindiheader,'User', ['Pending Submission','Pending Approval']) #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
    tableallheader = ['id','StudyActionNo','StudyName', 'ProjectPhase','Disipline' ,'Recommendations', 'Response','DueDate','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
    tableallheadermodified = ['Study Action No','Study Name', 'Project Phase','Discipline' ,'Recommendations', 'Response','Due Date','Initial Risk']
    
    #All actions and actions by Phases
    justenoughattributes =  ['id','StudyActionNo','Disipline' ,'Recommendations', 'QueSeries', 'Response','DueDate','InitialRisk']

    phasesactions =  blphasegetActionreducedfieldsQ(justenoughattributes,phase)
    
    #this annotate function needs to first because it doesnt like addtional items added to query set
    dictofallactions    = blannotatefktomodel(phasesactions)
    #this sequence is important otherwise doesnt work
    phaseswithrisk = bladdriskelements(dictofallactions)
    dictofallactions    = blgetdictActionStuckAt(phaseswithrisk)
    
    #edward 20211001 pd allactions
    all_actions =   ActionItems.objects.all().values()
    all_actionsannotate = blannotatefktomodel(all_actions)
    blank=[]
    all_actionsopt = bladdriskelements(all_actionsannotate)
    dfall1 = pd.DataFrame.from_dict(all_actionsopt) # sort dfall
    dfall = blsortdataframes(dfall1,dfallcolumns)
    #edward 20211001 pd rejected excel 
   
    revisiongte = 1
    queseriesrejected = 0
   

    #Rejected details using Q Object
    rejectedactions = blphasegetrejectedactionsQ (revisiongte,queseriesrejected,justenoughattributes,phase)
    rejecteddictofallactions    = blannotatefktomodel(rejectedactions)
    #this sequence is important otherwise doesnt work
    rejectedallactionitems = bladdriskelements(rejecteddictofallactions)
    dfrejection = pd.DataFrame.from_dict(rejectedallactionitems)
    
    #for Disipline based view
    #20211201 edward 
    tabledischeader = ['Discipline', 'Yet to Respond' ,'Approval Stage', 'Closed','Open Actions','Total Actions']
    lstbyDisc= blaggregatebyDisc(dfdiscsuborgphase,  YetToRespondQue, ApprovalQue,QueClosed,QueOpen,TotalQue)


    #get rejected summary actions get Reject Table
    tablerheaderejected = ['Discipline', 'Rejected Count']
    listofrejecteditems = blgetrejectedcount(dfdiscsuborgphase,1) #Pass revision number => than whats required

    #20211203 edward
    studiesattributes =['StudyName','ProjectPhase']
    phasestudies =  blphasegetStudyreducedfieldsQ(studiesattributes,phase)
    #20211206 edward 
    allstudies = Studies.objects.all()
    
    tablestudiesheader = ['Studies', 'Yet to Respond' ,'Approval Stage','Closed','Open Actions', 'Total Actions']

    lstbyWorkshop = blgetbyStdudiesCountphase(phasestudies,YetToRespondQue,ApprovalQue,QueClosed,QueOpen,TotalQue)
    
    
    #Changed to Q function and Phases
    tableduedateheader = ['Due Date','Actions to Close by']
    fieldsrequired = ['id','StudyActionNo', 'DueDate','QueSeries']
    actionitemsbyphase = blphasegetActionreducedfieldsQ(fieldsrequired,phase)
    lstbyDueDate= blaggregatebydate(blphasegetActionreducedfieldsQ(fieldsrequired,phase))
   
    #20211021 edward rundown by phase 
    closed=99
    closeditems = actionitemsbyphase.filter(QueSeries=closed)
    totalactions = (len(actionitemsbyphase))
    closedactions = (len(closeditems))
    
    subtotal =[]
    for items in lstbyDueDate:
       subtotal.append(items['count']) #how to access dictionary object by

    totalallDueDate = sum(subtotal)
    
    lstplanned         =  blprepareGoogleChartsfromDict(lstbyDueDate)
    lstactual      = blgetActualRunDown(lstplanned,closeditems) # shows how many closed pass in here 
    
    newlist = blformulateRundown(lstplanned,lstactual)
    #edward 20210727 rundown, 20211021 edward updated
    newliststop = blstopcharttoday(newlist,totalactions,closedactions)
    #edward end 20210727 rundown, 20211021 edward updated
    #20211021 edward rundown by phase 

    if request.method == 'POST':

        if (request.POST.get('allActions')):

            in_memory = BytesIO()


            response = HttpResponse(content_type='application/ms-excel') #
            response['Content-Disposition'] = 'attachment; filename=byAllActions.xlsx'
            #workbook.save(response) # odd  way but it works - took too long to figure out as no resource on the web
        
            with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
                dfall.to_excel(writer, sheet_name='All Actions',engine='xlsxwriter',header=None,startrow=1)
                workbook = writer.book #gives excelwriter access to workbook
                worksheet = writer.sheets['All Actions'] #gives excelwriter access to worksheet
                formattedexcel = blexcelformat(dfall,workbook,worksheet)

            in_memory.seek(0)
            response.write(in_memory.read())
            #edward end 20210928 dataframes excel

            return response
        elif (request.POST.get('rejectedactions')):

            in_memory = BytesIO()
            drejectedsorted = blsortdataframes(dfrejection,dfrejectedcolumns)

            with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
                drejectedsorted.to_excel(writer, sheet_name='Rejected Actions',engine='xlsxwriter',header=False,startrow=1)
                workbook = writer.book #gives excelwriter access to workbook
                worksheet = writer.sheets['Rejected Actions'] #gives excelwriter access to worksheet
                formattedexcel = blexcelformat(drejectedsorted,workbook,worksheet)
       
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
     
    
    #This needs to be worked on more as there are other problems now if risk matrix is not loaded
    #riskmatrix = blgetRiskMatrixAvailable()
    context = {
        
        'riskmatrix' : True,
        #'forpie' : forpie, #commented out Guna
        'lstbyDueDate' : lstbyDueDate,
        'tableduedateheader' : tableduedateheader,
        'totalallDueDate' : totalallDueDate, 
        #'rundowncontent': newliststop, #edward 20210727 rundown#commented out Guna
        'lstbyDisc' : lstbyDisc,
        'lstbyWorkshop' : lstbyWorkshop,
        'Indisets' : Indisets,
        #'lstofallactions' : lstofallactions,
        "dictofallactions" : dictofallactions,
        'tableindiheader' : tableindiheader,
        'tablestudiesheader' : tablestudiesheader,
        'tabledischeader' : tabledischeader ,
        'tableallheader' : tableallheadermodified,
        'listaggregatedindi':listaggregatedindi,
        'listaggregatedindiheader':listaggregatedindiheader,
        'listofrejectedheader': tablerheaderejected,
        'listofrejecteditems': listofrejecteditems,
        "rejectedactions": rejectedallactionitems,
        "listofPhases": listofPhases,
        "phase": phase,
        "piechartsjson" : json.dumps([{"data":forpie}])
    }
    #moving tojson 26/09/2021 - Guna. Moving to json enables cleaner javascript and data passing between python and html and javascript
    
    # #1st approach lace the dictionary wih features
    #featuresfields = ["Feature1", "Feature2"]
    #data3 = blmakelistforjson(forpie,featuresfields)
    # context["piechartsjson"]= json.dumps([{"data":data3}])
    
    #Test for lineshart
    #dataforrundown = blmakelistforjson(newliststop,featuresfields)
    #2nd approach should have done it like this in the first place simple stratight. Leaving the above to see how to lace and extract
    context["rundownchartsjson"] = json.dumps([{"data":newliststop}]) #one line, going to leave the above approach so that it could be used elsewhere
    #end Json changes

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

    actiondetails = ActionItems.objects.get(id=ID)
    datafrommodels= model_to_dict(actiondetails) #20210927 changed from using obj[0] to this method of converting to dictionary
    
    ObjAttach = actiondetails.attachments_set.all()  #get attcahments from foreign key

    studyActionNo =  actiondetails.StudyActionNo #move to bl
    replacestudyActionNo= studyActionNo.replace("/","_")
    Filename = replacestudyActionNo  + ".pdf"
    out_file = tempfolder + Filename #edward new tempfolder from parameters
    data_dict = datafrommodels

    discsub = blgetDiscSubOrgfromID(ID)
    Signatories = blgetSignotories(discsub)

    lstSignatoriesTimeStamp= blgettimestampuserdetails (ID, Signatories) #edward changed this to use new bl for signature 20210706

    signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp)

    #20210923 edward fk to data_dict
    studyname = str(actiondetails.StudyName)
    projectphase = str(actiondetails.ProjectPhase)
    foreignkeydict = {'StudyName':studyname,'ProjectPhase':projectphase}

    # updateddata_dict = bladdfktodict(data_dict,ID)
    updateddata_dict = bladdfktodict(data_dict,foreignkeydict)
    newcloseouttemplate = blsetcloseouttemplate (ID)

    file = pdfgenerate(newcloseouttemplate,out_file,updateddata_dict,signatoriesdict)

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

#edward 20211027 bulk pdf fix for large file dl
def mergedcloseoutprint(request):
    "Sends bulkpdf files with attachments in their repective folders in a zipped file to Client"

    response = FileResponse(open(bulkpdfzip,'rb'))
    response['Content-Disposition'] = 'attachment; filename= Bulk Closeout Sheets.zip'
    
    return response

#edward 20211027 bulk pdf fix for large file dl - original func
def mergedcloseoutprintoriginal(request): 
    
    #edward 20210915 bulkpdf parameters
    # bulkpdfdir = "static/media/temp/bulkpdf/"
    bulkpdfzipfoldername = tempfolder + ("bulkpdffiles" +".zip")
    # bulkpdfcreatezipfilename = "static/media/temp/" + "bulkpdffiles" #can be just slash

    objactionitems = ActionItems.objects.filter(QueSeries = 99).values() # to be altered when move to bl
    objactionitemsfk = blannotatefktomodel(objactionitems)
    returnzipfile = blbulkdownload(objactionitemsfk,bulkpdfdir,bulkpdfcreatezipfilename) #to remove bulkpdfmakebulkpdfdir

    in_memory = BytesIO()
    zip = ZipFile(in_memory,mode="w")
    finalname = os.path.basename(bulkpdfzipfoldername)
    zip.write (returnzipfile,finalname)
    zip.close()

    response = HttpResponse(content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename= Bulk Closeout Sheets.zip'
    in_memory.seek(0)
    response.write(in_memory.read())

    return response
#edward 20211027 bulk pdf fix for large file dl - original func



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

def indiprint(request,**kwargs):
    """This function prints individual Action Items into the """
    ID = (kwargs["id"])
    obj = ActionItems.objects.filter(id=ID).values().annotate(StudyName=F('StudyName__StudyName')).annotate(ProjectPhase = F('ProjectPhase__ProjectPhase')) # one for passing into PDF
    
    objFk =ActionItems.objects.get(id=ID) # this is for getting all attachments
    ObjAttach = objFk.attachments_set.all()  #get attcahments from foreign key
    studyActionNo =  objFk.StudyActionNo
    replacestudyActionNo= studyActionNo.replace("/","_")
    Filename = replacestudyActionNo  + ".pdf"
    #edward new tempfolder from parameters
    out_file = tempfolder + Filename

    data_dict=obj[0]

    #dont delete below as its a way to actualy read from memory
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #bufferfile = pdfsendtoclient ('atrtemplateautofontreadonly.pdf',data_dict)

    newcloseouttemplate = blsetcloseouttemplate (ID)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=" + studyActionNo+ ".pdf"
    #edward changed file location to parameters
    #20210923 edward study & phase fk
   # updateddata_dict = blgetfkdict(data_dict, ID)
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

#edward 20211122 stitch pdf 
def stitchpdf(request):

    " Sends stitched pdf to Client "

    response = FileResponse(open(stitchedpdf,'rb'))
    response['Content-Disposition'] = 'attachment; filename= Final Report.pdf'
    
    return response
