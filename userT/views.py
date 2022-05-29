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
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail
from .reports import *
from django.template.loader import render_to_string
from django.template import loader
from django.core.mail import EmailMessage
import pandas as pd
from django.utils import timezone
import os
from django.views.generic.detail import SingleObjectMixin
from userT.pdfgenerator import *
from django.db.models import Count
from zipfile import ZipFile
from io import StringIO, BytesIO
#Rest Framework
from rest_framework import viewsets
from .serializers import *
from rest_framework import generics
from UploadExcel.forms import *
from userT.parameters import *
from django.contrib.auth.mixins import UserPassesTestMixin
import json
import datetime
from datetime import date as dt
from operator import itemgetter
from collections import OrderedDict
from collections import Counter 
from django.forms.models import model_to_dict
from django.db.models import F
from django.http import StreamingHttpResponse
from datetime import datetime as dtime
from django.utils import timezone
from UploadExcel.formstudies import *
from time import time

def dynamicindisummX (request) :

    usersemail=request.user.email
    glist =[]
    xyzroutes = list(ActionRoutes.ActioneeRo.get_myroutes(usersemail).values_list("Disipline","Subdisipline"))

    xyzrouteslist = [print(list(x)) for x in xyzroutes]

    for items in xyzroutes:

        glist.append(list(items))

    return render (request, 'userT/YY.html')

def datatables (request): 
  return render(request, 'userT/datatables.html')   


def base3 (request):
    """
    This function is to view base3.html while editing the html
    """
    return render(request,'userT/base3.html')


def sidebar (request):
  return render(request, 'userT/basesidebar.html')


class actionlist(generics.ListCreateAPIView):
    pass


class anyView(viewsets.ModelViewSet):
    queryset = ActionItems.objects.all()
    serializer_class = anySerializers


def googlecharts88(request):
    lstbyDueDate    = blaggregatebydate(ActionItems.objects.all())
    lstplanned          = blprepareGoogleChartsfromDict(lstbyDueDate)
    lstactual           = blgetActualRunDown(lstplanned)
    newlist             = blformulateRundown(lstplanned,lstactual)

    for items in lstbyDueDate:
        x=items.get('DueDate')

    subtotal =[]
    for items in lstbyDueDate:
       subtotal.append(items['count']) 

    content =  newlist
    content1 = blstopcharttoday(content)
    context = {
        'content' : content1
    }
    return render(request, 'userT/googlecharts88.html',context) 


def mainDashboard (request):
    """ 
    My Dashboard view. Rewrite Nov 21. The starting point  or at main uses this view
    1. Get all studies first. not using phases at this stage at this is more for an individual dashboard 
    2. Get routes and separate them to actionee or approver routes
    """
    usersemail=request.user.email
    ActioneeActions = []
    ApproverActions = []
    Actionee_R = []
    Approver_R = []
    totalactioneeaction = 0
    studies = blgetAllStudies()
    menus = blgetmenus ()
    #get all routes based on email and then get seprate actione and approver routes 
    #dict_allrou = blgetuserRoutes(usersemail)
    dict_allrou = blgetuseroutesnew(usersemail)
    newdefswitch = True
    Actionee_R =    dict_allrou.get('Actionee_Routes')
    Approver_R =    dict_allrou.get('Approver_Routes')


    reducedfields= ['id','StudyActionNo','Disipline' ,'QueSeries', 'DueDate','InitialRisk']
    riskrankingsummary , ActioneeActionsrisk, ApproverActionsrisk = blgetriskrankingsummary(Actionee_R, Approver_R, reducedfields,newdefswitch)
    duedateaggregated = blaggregateby(ActioneeActionsrisk,"DueDate")
    duedatesummary = blduedateecountrelative(duedateaggregated)
    totalactioneeaction = blfuncActionCountQ(Actionee_R,YetToRespondQue,newdefswitch)
    totalactionssubmitted = blfuncActionCountQ(Actionee_R,ApprovalQue,newdefswitch)


    totalactionsapproved = blfuncActionCountQ(Actionee_R,QueClosed,newdefswitch)
    rejectedactionscount = blActioneerejectedcountQ(Actionee_R,newdefswitch) #3rd box in nicedashboard
    submittedsummary = {'totalactionssubmitted':totalactionssubmitted,'countrejected':rejectedactionscount, 'totalactionsapproved' :totalactionsapproved }

    #strdays = bltotalholdtime(Approver_R,reducedfields,newdefswitch)
   
    strdays = bltotalholdtimeActAppr(ApproverActionsrisk,ActioneeActionsrisk)
    countlistbyweek = blexceedholdtime(Approver_R,reducedfields,newdefswitch) # YY change this   

    stripCount =[]
    striplabels = []
    chartappdata=[]
    actioneefinallist =[]
    apprfinalist =[]
    labelsApprover =[]
    dataApprover =[]
    appractioncount =[]

    for eachstudy in studies:
        StudyName = eachstudy.StudyName
        labels=[]
        countbyStudies, labels= blActionCountbyStudiesStream(Actionee_R,StudyName,0,newdefswitch)
        stripCount, striplabels ,  = stripAndmatch(countbyStudies,labels)

        # Just to get a better view in HTML instead of rendering spaces for empty charts
        if stripCount != [] : 
            googlechartlist = blprepGoogChartsbyStudies(striplabels,stripCount,StudyName)
            actioneefinallist.append(googlechartlist)
            googlechartlist =[]

        #complete sub routine for actionee and then go to approver
        #approver routes has already been prefiltered according to queseries, so this loop just does the checking again based on studies
        #20_04_22 Changed to q series , tod elete commented items
        for QueSeries, Routes in Approver_R.items():
           
            #listofCountManyApprovers,labelsapp =blActionCountbyStudiesStream(Routes,StudyName,QueSeries,newdefswitch)
            listofCountManyApprovers = blActionCountbyStudiesStreamQ(Routes,StudyName,QueSeries,newdefswitch)
            #sumoflistCount = sum(listofCountManyApprovers)
            appractioncount.append(listofCountManyApprovers)
            if (listofCountManyApprovers > 0):
                labelsApprover.append('Level'+str(QueSeries))
                dataApprover.append(listofCountManyApprovers)
                
                chartappdata = blprepGoogChartsbyStudies(labelsApprover,dataApprover,StudyName)
                listofCountManyApprovers = 0
            
        apprfinalist.append(chartappdata)
        #reinitialize the list
        chartappdata = []
        dataApprover = []
        labelsApprover =[]
        countbyStudies = []

    totalapproveraction = sum (appractioncount)
    approverjsonlist = blremoveemptylist(apprfinalist)
    
    parameters = blgetparameters ()
    Versioning =  str(parameters.Versioning)


    Context = {
        'Versioning' : Versioning,
        'oneweekcount':countlistbyweek[0],
        'twoweekcount':countlistbyweek[1],
        'strdays':strdays,
        'totalapproveraction' : totalapproveraction,
        'totalactioneeaction' : totalactioneeaction,
        "pieactioneenew" : json.dumps([{"data":actioneefinallist}]),
        "pieapprovernew" : json.dumps([{"data":approverjsonlist}]),
        "riskrankingsummary":riskrankingsummary,
        "duedatesummary":duedatesummary,
        "submittedsummary": submittedsummary
            }
    return render(request, 'userT/maindashboard.html',Context) 


class ActioneeList (ListView):
    """
    This class is for Your Actions/Actionee list, basically uses email to get all actions within actionee routes 
    And then assigns a colour on it. Returns the queryset and context into object_list(default django)
    """

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
    """
    Populates what you have done under History under Your Actions
    """
    template_name   =   'userT/historylist.html' 

    def get_queryset(self):
        #historically only get queue for all approver levels that he person is the actionee instead of everything else
        userZemail = self.request.user.email
        dict_allRou = blgetuserRoutes(userZemail)

        #get Actionee and Approver Routes, tied into model managers
        Actionee_R =    dict_allRou.get('Actionee_Routes')
        lstgetHistoryforUser             = blgetHistoryforUser(userZemail,Actionee_R)

        #the sequence just appends risk matrix colours
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
            #starts with key 1 - it shows if your name is in approver 1
            #The key reresents que series
            allactionItems= blApproverHistoryActions(value,key)
            ApproverActions.insert(key,allactionItems)

        approverflatdict = [item for sublist in ApproverActions for item in sublist] # Just merging all approvers levels into a flatter list

        #addriskcolour to approver list
        finalappractionitems = bladdriskcolourandoptimise(approverflatdict)
        rejecteditemsid = blRejectedHistortyActionsbyId(userZemail,0,1)
        rejecteditemsbyhistory = [blgetActionItemsbyid(rejecteditemsid)] # Creating a list to feed into bladdriskcolourandoptimise as that function is expecting a list of dictionaries
        newrejecteditemsbyhist = bladdriskcolourandoptimise(rejecteditemsbyhistory)
        context['rejectedhistory'] = rejecteditemsbyhistory
        context['approveractions'] = finalappractionitems
        return context


class ApproverList (ListView):
    """
    This is the view under Your actions and when you click Approver Actions. It gives all 
    approver actions across multiple que series. Get routes that maps against que series and then use 
    """
    template_name   =   'userT/actionlistapprover.html'

    def get_queryset(self):
        userZemail = self.request.user.email
        ApproverActions = []
        ApproverActionsX = []
        dict_allRou = blgetuserRoutes(userZemail)
        #gets approver routes by que series and slots QuerySet for routes according to key dict Approver Routes
        Approver_R =    dict_allRou.get('Approver_Routes')
        reducedfileds= ['id','StudyActionNo','StudyName__StudyName','Disipline' ,'Subdisipline','Cause','Recommendations',
        'QueSeries', 'DueDate','Response','InitialRisk']

        for key, value in Approver_R.items():
            allactionItems= blallactionscomdissubQ(value,key,reducedfileds)    
            finalactionitems = bladdriskelements(list(allactionItems))
            ApproverActions.insert (key,allactionItems)
        return ApproverActions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riskmatrix'] = blgetriskmatrixtable()
        return context


class DetailActioneeItems (DetailView):
    template_name   =   'userT/actiondetailactionee.html' #yhs changed to all small letters

    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)


class ApproveItemsMixin(UserPassesTestMixin,UpdateView):
    """
    This function shows the Approver view (with non editable fields) for each individual Action
    """
    template_name = "userT/actionupdateapproveaction.html" 
    form_class = frmoriginalbaseapprover
    success_url = '/ApproverList/'

    def get_form_class(self,**kwargs):
        form_classnew = (blgetFieldValue(self.kwargs.get("pk"),"StudyName__Form"))
        if form_classnew:
            form_classapprover = f"{form_classnew}approver"  
            from UploadExcel import formstudies
            form_class= getattr(formstudies, form_classapprover,None)
        else:
            form_class = self.form_class
        return form_class

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
        if (self.request.POST.get('Reject')):
                #If reject que series should be 0, but need another intermediate screen for comments
            context = {
                        'StudyActionNo' : form.instance.StudyActionNo
                }
            return HttpResponseRedirect(reverse ('RejectReason', kwargs={'forkeyid': form.instance.id})) #this is key as wanted another screen on the first reject

        if (self.request.POST.get('Cancel')):
            return HttpResponseRedirect('/ApproverList/')

        if (self.request.POST.get('Approve')):
            return super().form_valid(form)

        if (self.request.POST.get('Pullback')):
            return super().form_valid(form)
        
        if (self.request.POST.get('Delete')):
            #if delete function required for approver to copy from actioneemixin IMPORTANT
            pass

        if (self.request.POST.get('Next')):
            return super().form_valid(form)

    def get_context_data(self,**kwargs):
        idAI = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        discsub = blgetDiscSubOrgfromID(idAI)
        Signatories = blgetSignotories(discsub)
        lstSignatoriesTimeStamp= blgettimestampuserdetails (idAI, Signatories) #it changes the Signatories directly
       
        currentQueSeries = blgetFieldValue(idAI,'QueSeries')
        blgettimehistorytables(idAI,lstSignatoriesTimeStamp,currentQueSeries)
        ApproverLevel = blgetApproverLevel(discsub) #add approver level target in case it doesnt get set at the start
        blsetApproverLevelTarget(idAI,ApproverLevel)
        object_list = self.object.attachments_set.all()

        context['object_list'] = object_list
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(idAI)
        context['Approver'] = True
        context ['Signatories'] = lstSignatoriesTimeStamp
        return context

    def get_success_url(self):
        return reverse ('ApproverConfirm', kwargs={'id': self.object.id})


class ApproverConfirm(UpdateView):
    """
    This function is for the Approver Confirmation Page
    """
    template_name = "userT/approverconfirmation.html" #yhs changed to all small letters
    form_class = frmApproverConfirmation
    success_url = '/ApproverList/'

    def form_valid(self,form):
        emailid=self.request.user.email
        strsignature = blgetfieldCustomUser(emailid,"signature") #IMPORTANT

        if (self.request.POST.get('Cancel')):
            
            ID =self.kwargs["id"]
            bldeletehistorytablesignatory(ID)
            return HttpResponseRedirect('/ApproverList/')

        if (self.request.POST.get('ApproveConfirm')):
            ID =self.kwargs["id"]
            field = "QueSeriesTarget"
            ApproverLevel =  blgetFieldValue(ID,field)
            if (form.instance.QueSeries == (ApproverLevel-1)):
                form.instance.QueSeries = 99 # Random far end number to show all closed
            else:
                form.instance.QueSeries += 1

            if (self.request.POST.get('signature')):
                strsignature = self.request.POST.get('signature')
                blsetfieldCustomUser(emailid,"signature",strsignature)
            else :
                blsetfieldCustomUser(emailid,"signature",str(emailid))

            integerqueseries = blgetFieldValue(ID,"QueSeries")
            discsub = blgetDiscSubOrgfromID(ID)
            Signatoryemails = blgetSignatoryemailbyque(discsub,integerqueseries+1)
            ContentSubject  = blbuildSubmittedemail(ID,"Approver")
            success = blemailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1])
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Showing email as default signature
        """
        emailid=self.request.user.email
        sign=self.request.user.signature
        context = super().get_context_data(**kwargs)
        context['signature'] = blgetfieldCustomUser(emailid,"signature")
        return context

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['id'])


class HistoryConfirm(UpdateView):
    """
    This function is for the Actionee's History Confirm Pullback View 
    """
    template_name = "userT/historyconfirmpull.html" 
    form_class = frmApproverConfirmation
    success_url = '/HistoryList/'

    def form_valid(self,form):
        if (self.request.POST.get('Cancel')):
           return HttpResponseRedirect('/HistoryList/')

        if (self.request.POST.get('Pullconfirm')):
            form.instance.QueSeries = 0 # Return back to Actionee
            return super().form_valid(form)

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['id'])


class HistoryFormMixin(UserPassesTestMixin,UpdateView):
    """
    This function gets the History Item for Your Actions View
    """
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
        #id = self.object.id  # old code just leave it as its a good example IMPORTANT
        id = self.kwargs['pk']
        isactionee= eval(self.kwargs['actionee']) #convert string to boolean values so can use direct in HTML
        context = super().get_context_data(**kwargs)
        discsuborg = blgetDiscSubOrgfromID(id)
        ApproverLevel = blgetApproverLevel(discsuborg)
        Signatories = blgetSignotories(discsuborg)
        lstSignatoriesTimeStamp= blgettimestampuserdetails (id, Signatories)

        actionlocation = []
        integerqueseries = blgetFieldValue(id,"QueSeries")
        if integerqueseries != 99 and (Signatories !=[]): # looks at que series and then matches it against the list of signatories for an action
            lststuckAt = Signatories[integerqueseries] # uses QueSeries to indicate where action currently is
            actionlocation.append(lststuckAt[1])
        else:
            actionlocation.append('Closed')

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
           return HttpResponseRedirect('/HistoryList/')

    def get_success_url(self):
        return reverse ('HistoryConfirm', kwargs={'id': self.object.id })


class ActioneeItemsMixin(UserPassesTestMixin,UpdateView): #@user_passes_test(lambda u: u.groups.filter(name='Actionee').count() == 0, login_url='/main') IMPORTANT
    template_name = "userT/actionupdateapproveaction.html"
    form_class = frmoriginalbase
  
    def get_form_class(self,**kwargs):
        form_classnew = (blgetFieldValue(self.kwargs.get("pk"),"StudyName__Form"))

        if form_classnew:
            from UploadExcel import formstudies
            form_class= getattr(formstudies, form_classnew,None)
        else:
            form_class = self.form_class
        return form_class
    
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
        return HttpResponseRedirect('/main')  #if no permission from test_func return to main

    def get_object(self,queryset=None):

        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['pk'])
        
    def get_context_data(self,**kwargs):
        IdAI = self.kwargs.get("pk") #its actually the id and used as foreign key
        context = super().get_context_data(**kwargs)
        emailID = self.request.user.email

        discsuborg = blgetDiscSubOrgfromID(IdAI)
        ApproverLevel = blgetApproverLevel(discsuborg)
        Signatories = blgetSignotories(discsuborg)
        multipleSignatories = blmultisignareplace(Signatories,emailID,"Actionee") # Replaces the multiple signatory with an individual
        blsetApproverLevelTarget(IdAI,ApproverLevel)
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
    """
    This function is for the Contact Us Page
    """
    return render(request, 'userT/contactus.html') 


class RejectReason (CreateView):
    """
    This function allows the Approver to fill in their Rejection Reason when Rejecting an Action
    """
    model = Comments
    template_name = 'userT/rejectreason.html' 
    form_class = frmAddRejectReason
    success_url = '/ApproverList/'

    def form_valid (self,form):
        if (self.request.POST.get('Reject')):
            ID = self.kwargs['forkeyid']
            intqueseries = blgetFieldValue(ID,"QueSeries")

            #set using model manager since we want it back to actionee it has to be set at QueSeries=0
            blsetrejectionActionItems(ID,0)# This is key and should go into bltoset this and revision IMPORTANT

            form.instance.Action_id = ID
            form.instance.Username = self.request.user.email
            rejectreason =  form.instance.Reason
            discsub = blgetDiscSubOrgfromID(ID)
            Signatoryemails = blgetSignatoryemailbyquereject(discsub,intqueseries,ID)
            
            ContentSubject  =blbuildSubmittedemail(ID,"Reject",rejectreason)
            success = blemailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1]) #send email, the xyz is dummy data and not used
            return super().form_valid(form)

        if (self.request.POST.get('Cancel')):
            return HttpResponseRedirect('/ApproverList/') #cant use success url, its got assocaition with dict object

    def get_context_data(self, **kwargs):
        fk = self.kwargs['forkeyid']
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        return context


def IndividualBreakdownByActions(request):
    allactions = ActionItems.objects.all()
    lstattributes = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','InitialRisk']
    lstofindiactions = blgetActionStuckAt(allactions, lstattributes)

    context ={
        'context' : lstofindiactions
    }
    return render(request, 'userT/indibreakdownbyactions.html', context)


def multiplefiles (request, **kwargs):
    """
    This function enables the User to upload the attachments into the system
    """
    form_multi = frmMultipleFiles()
    emailid = request.user.email
    strsignature = blgetfieldCustomUser(emailid,"signature") #IMPORTANT

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
            x = Attachments.objects.create(
                Attachment=file,
                Action_id=ID,
                Username=request.user.email
            )
        newQueSeries = 1

        ActionItems.mdlQueSeries.mgrsetQueSeries(ID,newQueSeries)
        discsub = blgetDiscSubOrgfromID(ID)
        Signatoryemails = blgetSignatoryemailbyque(discsub,newQueSeries) 
        ContentSubject  =blbuildSubmittedemail(ID,"Actionee")
        success = blemailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1])
        return HttpResponseRedirect('/ActioneeList/')

    if (request.POST.get('Cancel')):
            return HttpResponseRedirect('/ActioneeList/') #cant use success url, its got associattion with dict object

    context = {
        'form_multi' : form_multi,
        'signature' : strsignature,
    }
    ID = kwargs['forkeyid']
    return render(request, 'userT/multiplefiles.html',context) #yhs checked small letters


def rptoverallStatus(request, **kwargs):
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
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()

    #separate list , reusing list will screw it up by adding list below to this one
    listcountbyDisSub= []
    listlablesDisc =[]
    listcountbyCompany= []
    listlabelsCompany = []

    for itemPair in discsub:
        listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,openActionsQueSeries))
        listlablesDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))

    chartChanges.append(showPie(listcountbyDisSub,listlablesDisc, "Open Actions by Disc/Sub-Disc"))

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
                        listcountbyCompany.append(blgetCompanyActionCount (items,openActionsQueSeries)) #dont need to append list as its already in the list above                            
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
                    countbyStudies = []

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
                    countbyStudies = []

    context = {
            "charts":charts,
            "chartChanges":chartChanges,
            "overall":True

    }
    return render (request, 'userT/reports.html',context ) #yhs checked

def rptdiscSlice(request, **kwargs):
    TotalCount = [0,1,2,3,4,5,6,7,8,9,99]  
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
    generalxlabel = "" 
    labelActionee = "Actionee"
    labelApprover = "Approver"
    TitleActApp = "Actionee-Approver Open items"
    listofPairActioneeCount = []
    listofPairApproverCount = []
    discsub #IMPORTANT

    for itemPair in discsub:
        listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,OpenAccount))
        totalcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,TotalCount))
        listlablebyDisSub.append(str(itemPair[2]+"/"+ itemPair[0]+"/"+ itemPair[1])) # to include sub disc later -- +"/"+str(itemPair[1])
        listofstringDiscSub.append(str(itemPair[0]+"/"+ itemPair[1]))
        listofPairActioneeCount.append(blgetDiscSubActionCount ('Y',itemPair,[0]))
        listofPairApproverCount.append(blgetDiscSubActionCount ('Y',itemPair,ApproverQList))

    listoflist = [[]]
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
    return render (request, 'userT/repdisc.html', context) 


def rptbyUser(request, **kwargs):
    dict_allRou = blgetuserRoutes(request.user.email)
    Actionee_R =    dict_allRou.get('Actionee_Routes')
    ActioneeCount = blfuncActionCount(Actionee_R,0)
    return render (request, 'userT/reports.html') #yhs checked


def repoverallexcel (request):
    """
    Provides the Download Complete Excel Feature in PMT Reporting
    """
    all_actions =   ActionItems.objects.all().values()
    all_actionwithfk = blannotatefktomodel(all_actions)
    dfalllist = blgetdictActionStuckAt(all_actionwithfk) 
    # dfalllocation = blexcelgetactioneeandlocation (dfalllist)   
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
    return response

    
def repPMTExcel (request,phase=""):
    """
    This is the original function called when user selects PMT Reporting from menu
    The dataframes excel outputs are also written in this function.
    """
    listofPhases= Phases.mdlSetGetField.mgrGetAllActionsAndFields()
    discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() 
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
  
    organisationnames = ActionRoutes.mdlAllCompany.mgr_getOrgnames()

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
    #End Pie

    Indisets = blgetIndiResponseCount2(dfdiscsuborgphase,QueOpen,QueClosed,phase) 
    tableindiheader = ['User','Role','Organisation Route','Pending Submission','Pending Approval','Closed', 'Open Actions'] 
    
    listaggregatedindi,listaggregatedindiheader=blgroupbyaggsum(Indisets,tableindiheader,'User', ['Pending Submission','Pending Approval']) #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
    tableallheader = ['id','StudyActionNo','StudyName', 'ProjectPhase','Disipline' ,'Recommendations', 'Response','DueDate','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
    tableallheadermodified = ['Study Action No','Study Name', 'Project Phase','Discipline' ,'Recommendations', 'Response','Due Date','Initial Risk']
    
    #All actions and actions by Phases
    justenoughattributes =  ['id','StudyActionNo','Disipline' ,'Recommendations', 'QueSeries', 'Response','DueDate','InitialRisk']
    phasesactions =  blphasegetActionreducedfieldsQ(justenoughattributes,phase)
    
    dictofallactions    = blannotatefktomodel(phasesactions) #Annotate first because it doesnt like addtional items added to query set
    #this sequence is important otherwise doesnt work
    phaseswithrisk = bladdriskelements(dictofallactions)
    dictofallactions    = blgetdictActionStuckAt(phaseswithrisk)
    
    #pandas excel
    all_actions =   ActionItems.objects.all().values()
    all_actionsannotate = blannotatefktomodel(all_actions)
    blank=[]
    all_actionsopt = bladdriskelements(all_actionsannotate)
    dfall1 = pd.DataFrame.from_dict(all_actionsopt) # sort dfall
    dfall = blsortdataframes(dfall1,dfallcolumns)

    revisiongte = 1
    queseriesrejected = 0
   
    #Rejected details using Q Object
    rejectedactions = blphasegetrejectedactionsQ (revisiongte,queseriesrejected,justenoughattributes,phase)
    rejecteddictofallactions    = blannotatefktomodel(rejectedactions)
    #this sequence is important otherwise doesnt work
    rejectedallactionitems = bladdriskelements(rejecteddictofallactions)
    dfrejection = pd.DataFrame.from_dict(rejectedallactionitems)
    
    #for Disipline based view
    tabledischeader = ['Discipline', 'Yet to Respond' ,'Approval Stage', 'Closed','Open Actions','Total Actions']
    lstbyDisc= blaggregatebyDisc(dfdiscsuborgphase,  YetToRespondQue, ApprovalQue,QueClosed,QueOpen,TotalQue)

    #get rejected summary actions get Reject Table
    tablerheaderejected = ['Discipline', 'Rejected Count']
    listofrejecteditems = blgetrejectedcount(dfdiscsuborgphase,1) #Pass revision number => than whats required

    blankrejectlist = []
    for items in dfdiscsuborgphase:
        testrejectactions = blnewgetrejecteditemsQ(items,1,phase,reducedfields=['Disipline','Subdisipline','Organisation','Revision'])
        blankrejectlist.append(testrejectactions)

    blanklist=[]
    for items in dfdiscsuborgphase:
        testing = blnewgetrejecteditemsQcount(items,1,phase)
        blanklist.append(testing)
    totalrejecteditems = sum(blanklist)

    studiesattributes =['StudyName','ProjectPhase']
    phasestudies =  blphasegetStudyreducedfieldsQ(studiesattributes,phase)
    
    # allstudies = Studies.objects.all() #IMPORTANT

    tablestudiesheader = ['Studies', 'Yet to Respond' ,'Approval Stage','Closed','Open Actions', 'Total Actions']
    lstbyWorkshop = blgetbyStdudiesCountphase(phasestudies,YetToRespondQue,ApprovalQue,QueClosed,QueOpen,TotalQue)

    #Changed to Q function and Phases
    tableduedateheader = ['Due Date','Actions to Close by']
    fieldsrequired = ['id','StudyActionNo', 'DueDate','QueSeries']
    actionitemsbyphase = blphasegetActionreducedfieldsQ(fieldsrequired,phase)
    lstbyDueDate= blaggregatebydate(blphasegetActionreducedfieldsQ(fieldsrequired,phase))
   
    # rundown by phase IMPORTANT
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
    newliststop = blstopcharttoday(newlist,totalactions,closedactions)

    if request.method == 'POST':

        if (request.POST.get('allActions')):
            in_memory = BytesIO()
            response = HttpResponse(content_type='application/ms-excel') #
            response['Content-Disposition'] = 'attachment; filename=byAllActions.xlsx'
        
            with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
                dfall.to_excel(writer, sheet_name='All Actions',engine='xlsxwriter',header=None,startrow=1)
                workbook = writer.book #gives excelwriter access to workbook
                worksheet = writer.sheets['All Actions'] #gives excelwriter access to worksheet
                formattedexcel = blexcelformat(dfall,workbook,worksheet)
                
            in_memory.seek(0)
            response.write(in_memory.read())
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
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type 
            response['Content-Disposition'] = 'attachment; filename=byIndividualSummary.xlsx'
            workbook.save(response)
            return response

        elif (request.POST.get('indiActions')):
            workbook = excelAllActions(Indisets,tableindiheader,"Individual Actions")
            response = HttpResponse(content_type='application/ms-excel') 
            response['Content-Disposition'] = 'attachment; filename=byIndividual.xlsx'
            workbook.save(response)
            return response

        elif (request.POST.get('allStudies')):
            workbook = excelAllActions(lstbyWorkshop,tablestudiesheader,"Workshop Actions")
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=byStudies.xlsx'
            workbook.save(response)
            return response

        elif (request.POST.get('bydiscipline')):
            workbook = excelAllActions(lstbyDisc,tabledischeader,"Discipline Actions")
            response = HttpResponse(content_type='application/ms-excel') 
            response['Content-Disposition'] = 'attachment; filename=byDiscipline.xlsx'
            workbook.save(response)
            return response

        elif (request.POST.get('byDueDate')):
            reallstDuedate = blquerysetdicttolist(lstbyDueDate) 
            workbook = excelAllActions(reallstDuedate,tableduedateheader,"DueDates")
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=byDueDates.xlsx'
            workbook.save(response) # odd way but it works - took too long to figure out as no resource on the web
            return response    
     
    context = {
        'riskmatrix' : True,
        'lstbyDueDate' : lstbyDueDate,
        'tableduedateheader' : tableduedateheader,
        'totalallDueDate' : totalallDueDate, 
        'lstbyDisc' : lstbyDisc,
        'lstbyWorkshop' : lstbyWorkshop,
        'Indisets' : Indisets,
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
        "piechartsjson" : json.dumps([{"data":forpie}]),
    }

    context["rundownchartsjson"] = json.dumps([{"data":newliststop}]) #one line, going to leave the above approach so that it could be used elsewhere

    return render(request, 'userT/reppmtexcel.html', context)


def DisciplineBreakdown (request):
    return render(request, 'userT/disciplinebreakdown.html')#yhs changed to small letters


def StickyNote(request):
    return render(request, 'userT/stickynote.html') #yhs changed to small letters


def closeoutprint(request,**kwargs):
    """
    This function prints the individual closed reports to PDFs
    """
    ID = (kwargs["id"])
    actiondetails = ActionItems.objects.get(id=ID)
    datafrommodels= model_to_dict(actiondetails) 

    ObjAttach = actiondetails.attachments_set.all()  #get attcahments from foreign key
    studyActionNo =  actiondetails.StudyActionNo 
    replacestudyActionNo= studyActionNo.replace("/","_")
    Filename = replacestudyActionNo  + ".pdf"
    out_file = tempfolder + Filename 
    data_dict = datafrommodels

    discsub = blgetDiscSubOrgfromID(ID)
    Signatories = blgetSignotories(discsub)
    lstSignatoriesTimeStamp= blgettimestampuserdetails (ID, Signatories) #edward changed this to use new bl for signature 20210706

    currentQueSeries = blgetFieldValue(ID,'QueSeries')
    blgettimehistorytables(ID,lstSignatoriesTimeStamp,currentQueSeries)
    signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp)
    
    studyname = str(actiondetails.StudyName)
    projectphase = str(actiondetails.ProjectPhase)
    foreignkeydict = {'StudyName':studyname,'ProjectPhase':projectphase}
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

    return response


def mergedcloseoutprint(request):
    """
    Sends bulkpdf files with attachments in their repective folders in a zipped file to Client
    """
    response = FileResponse(open(bulkpdfzip,'rb'))
    response['Content-Disposition'] = 'attachment; filename= Bulk Closeout Sheets.zip'
    return response


def mergedcloseoutprintoriginal(request): 
    bulkpdfzipfoldername = tempfolder + ("bulkpdffiles" +".zip")
    objactionitems = ActionItems.objects.filter(QueSeries = 99).values() 
    objactionitemsfk = blannotatefktomodel(objactionitems)
    returnzipfile = blbulkdownload(objactionitemsfk,bulkpdfdir,bulkpdfcreatezipfilename) 

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


def closeoutsheet(request): 
    """
    This function builds the closeoutsheet for Closed Actions
    """
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
    lstofallactions = blgetActionStuckAt(allactions, tableallheader) #feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
    tableallheadermodified =  ['Study Action No','Study Name', 'Discipline' ,'Recommendations','Response','Initial Risk']
    filename = [] # for appending filename place before for loop

    lstclosed = ActionItems.objects.filter(QueSeries =99)
    
    if (request.POST.get('GeneratePDF')):
        x=ActionItems.objects.all()  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')

        y= x.values()
        for item in y :
            i = item["StudyActionNo"] 
            j = (i + '.pdf')  #specify +1 for each file so it does not overwrite one file
            del item["id"]
            data_dict=item
            out_file = staticmedia + j
            pdfgenerate(atrtemplate,out_file,data_dict)#returns from pdfgenerator 
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
    """
    This function shows individual Actions views in PMT Reporting section
    """
    template_name = "userT/reppmtviewall.html" #the html is missing object_list
    form_class = frmoriginalbaseapprover

    def get_form_class(self,**kwargs):
        form_classnew = (blgetFieldValue(self.kwargs.get("id"),"StudyName__Form")) 
        if form_classnew:
            form_classapprover = f"{form_classnew}approver"
            from UploadExcel import formstudies
            form_class= getattr(formstudies, form_classapprover,None) 
        else:
            form_class = self.form_class
        return form_class

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
        return queryset.get(id=self.kwargs['id'])

    def get_context_data(self,**kwargs):
        idAI = self.kwargs.get("id")
        context = super().get_context_data(**kwargs)
        discsub = blgetDiscSubOrgfromID(idAI)
        Signatories = blgetSignotories(discsub)
        
        lstSignatoriesTimeStamp= blgettimestampuserdetails (idAI, Signatories)
        currentQueSeries = blgetFieldValue(idAI,'QueSeries')
        blgettimehistorytables(idAI,lstSignatoriesTimeStamp,currentQueSeries)
        object_list = self.object.attachments_set.all() 
        rejectcomments = self.object.comments_set.all() 

        context['object_list'] = object_list 
        context['Rejectcomments'] = rejectcomments
        context ['Signatories'] = lstSignatoriesTimeStamp

        return context


def indiprint(request,**kwargs):
    """
    This function prints individual Action Items into the 
    """
    ID = (kwargs["id"])
    obj = ActionItems.objects.filter(id=ID).values().annotate(StudyName=F('StudyName__StudyName')).annotate(ProjectPhase = F('ProjectPhase__ProjectPhase')) # one for passing into PDF
    objFk =ActionItems.objects.get(id=ID) # this is for getting all attachments
    ObjAttach = objFk.attachments_set.all()  #get attcahments from foreign key
    studyActionNo =  objFk.StudyActionNo
    replacestudyActionNo= studyActionNo.replace("/","_")
    Filename = replacestudyActionNo  + ".pdf"
    out_file = tempfolder + Filename
    data_dict=obj[0]

    newcloseouttemplate = blsetcloseouttemplate (ID)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=" + studyActionNo+ ".pdf"

    file = pdfsendtoclient(newcloseouttemplate, data_dict)
    response.write(file.read())
    return response


def delegatedadmin (request):
    """
    This function returns the view for delegatedadmin
    """
    return render(request, 'userT/delegatedadmin.html')#yhs changed to small letters


def stitchpdf(request):
    """
    Sends stitched pdf to Client 
    """
    response = FileResponse(open(stitchedpdf,'rb'))
    response['Content-Disposition'] = 'attachment; filename= Final Report.pdf'
    return response
