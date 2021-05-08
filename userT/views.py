from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from UploadExcel.forms import *
from django.contrib.auth import get_user_model
import matplotlib as plt
from .businesslogic import *
from .email import *
from .excelReports import *
from .models import *
from UploadExcel.models import *
from django.views.generic import ListView, DetailView, UpdateView,TemplateView, CreateView
#test for login required
from django.contrib.auth.decorators import login_required
from django.conf import settings
import pypdftk
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
from userT.pdfgenerator import pdfgenerate
#from .forms import UserRegisterForm
# Create your views here.

from UploadExcel.forms import *
emailSender ="support@prism-ehstools.awsapps.com"

def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
            #usernames =   form.cleaned_data.get('username')
           # messages.success(request, 'account has been created')
        if form.is_valid():
            form.save()
            return render(request, 'userT/home.html')
    else:
       #form =  UserRegisterForm()
       #form = UserCreationForm()
        return render(request, 'userT/register.html', {'form': form})

def mainDashboard (request):
    
    
    #for chart.js Html only
    labelsActionee = []
    dataActionee = []

    labelsApprover = []
    dataApprover = []
    #This contain the entire Approver list for all levels
    Approver = []

    #get workshops
    studies = blgetAllStudies()

    #get all routes
    context_allRou = getuserRoutes(request,request.user.email)
    
    #Just get Actionee and Approver Routes, tied into model managers
    Actionee_R =    context_allRou.get('Actionee_Routes')
    Approver_R =    context_allRou.get('Approver_Routes') #this is a dictionary item {1,[list of routes]}

   
    charts=[]
    apprcharts =[]
    stripCount =[]
    striplabels = []
    QueOpen = [1,2,3,4,5,6,7,8,9]
    QueClosed =99  #something wrong this fucntion wrote it early but needs a bit more to accept list
    #loop through each workshop and get counts
    #This function just does a count using model managers , calling from businesslogic.py
    
    #Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)
    #blgetDiscSubOrgfromID(idAI)
    for eachstudy in studies:
        StudyName = eachstudy.StudyName
        
        labels=[]
        labelsapp =[]

        labelsclosed =[]
        #countbyStudies = blActionCountbyStudies(Actionee_R,StudyName,0) - old way limited by three streams 
        
        countbyStudies, labels= blActionCountbyStudiesStream(Actionee_R,StudyName,0) # unlimited actionee
        countbyStudiesClosed, labelsClosed= blActionCountbyStudiesStream(Actionee_R,StudyName,QueClosed)
             
        stripCount, striplabels ,  = stripAndmatch(countbyStudies,labels)

        stripCountClosed, striplabelsClosed ,  = stripAndmatch(countbyStudiesClosed,labelsClosed)
        # For studies check if actually assigned to it or if count is 0 then just dont generate graph
        if stripCount != []:
            
            charts.append(showPie(stripCount,striplabels,StudyName))
        
            charts.append(showPie(stripCountClosed,striplabelsClosed,StudyName +" -- Closed Actions"))
        #the key starts at 1 which is good thing and hence just pass to get count from queseries
        for key, value in Approver_R.items():
            for items in value:
                labelsapp.append(items.Disipline)
        
        
        
        for QueSeries, Routes in Approver_R.items():
            
           
            #listofCount= blActionCountbyStudies(Routes,StudyName,QueSeries)
            listofCountManyApprovers,labelsapp =blActionCountbyStudiesStream(Routes,StudyName,QueSeries) #improved version multiple approvers
           

            sumoflistCount = sum(listofCountManyApprovers)
            if (sumoflistCount > 0):
                labelsApprover.append('Level'+str(QueSeries))
                dataApprover.append(sumoflistCount)
        
        #dont want a blank pie to be appended on with no data since it loops through studies
        if dataApprover != []:
            apprcharts.append(showPie(dataApprover,labelsApprover,StudyName))
            
        
        dataApprover = []
        labelsApprover =[]
        stripedCount =[]
        stripedlabels =[]
        countbyStudies = []
 
       
    #get count for all approver levels just by looping through the key
    #Not very accurate but im summing approver level actions together
    # key is already rationalised in getuserRoutes
    for key, value in Approver_R.items():
        x= blfuncActionCount(value,key)
        Approver.insert(key,x)
        labelsApprover.append('Level'+str(key))
        dataApprover.append(sum(x))
    
    #apprchart=showPie(dataApprover,labelsApprover,"Approver Charts")

    
    #Context just returns to HTML so that we can use it in the HTML page
    Context = {
        'charts' : charts,
        'apprcharts' : apprcharts,
        
        #'Approver_Count'       : Approver,
        'labelsActionee' : labelsActionee,
        'dataActionee' : dataActionee,
        'labelsApprover' : labelsApprover,
        'dataApprover' : dataApprover,
            }
    return render(request, 'userT/mainDashboard.html',Context)


def getActionDetails(request, id=None):
    Items = get_object_or_404(ActionItems,id=id)
    context = {
            "Items":Items

    }
    return render(request, "userT/detailactions.html", context)

def getuserRoutes(request,useremail):
    ApproverLevel = 8
    userZemail = useremail
    Approver_Routes = {}

    #Actionee routes is straight forward
    Actionee_Routes   =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
    
    #Optimised to get all approver levels; readjust the key to 1 instead of 0
    for ApproverLevel in range(1 , ApproverLevel+1):
       Approver_Routes [ApproverLevel]  =  ActionRoutes.ApproverRo.get_myroutes(userZemail,ApproverLevel)
    #context just another form of return
    contextRoutes = {
       'Actionee_Routes' : Actionee_Routes,
       'Approver_Routes': Approver_Routes,
    }
    
    return contextRoutes

#below view is for list of actions under actionee , 
# it returns a list of actions under object_list
class ActioneeList (ListView):
    template_name   =   'userT/actionListActionee.html'
    
    def get_queryset(self):
        userZemail = self.request.user.email
        ActioneeRoutes =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
        #actioneeItems = blfuncActioneeComDisSub(ActioneeRoutes,0) - To be deleted - this was limited to 3 streams
        ActioneeActions = blallActionsComDisSub(ActioneeRoutes,0)

        
        return ActioneeActions

class HistoryList (ListView):
    template_name   =   'userT/historylist.html'
    
    def get_queryset(self):
        #historically only get queue for all approver levels that he person is the actionee instead of everything else
        userZemail = self.request.user.email
        ActioneeRoutes =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)

        lstgetHistoryforUser             = blgetHistoryforUser(userZemail,ActioneeRoutes)
        
        return lstgetHistoryforUser    
    
class ApproverList (ListView):
    template_name   =   'userT/actionListApprover.html'
    
    def get_queryset(self):
        userZemail = self.request.user.email
        ApproverActions = []
        context_allRou = getuserRoutes(self.request,userZemail)
        Approver_R =    context_allRou.get('Approver_Routes')
        
        for key, value in Approver_R.items():
            #x = blfuncActioneeComDisSub(value,key)
            allactionItems= blallActionsComDisSub(value,key)
            ApproverActions.insert(key,allactionItems)
            
        
        return ApproverActions

class DetailActioneeItems (DetailView):
    template_name   =   'userT/actionDetailActionee.html'
    #queryset = ActionItems.objects.all()

    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)


class ApproveItemsMixin(UpdateView,ListView, SingleObjectMixin):
    #paginate_by = 20
    template_name = "userT/actionUpdateApproveAction.html"
    form_class = ApproverForm
    success_url = '/ApproverList/'

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
            
            # ID =self.kwargs["pk"]
            # field = "QueSeriesTarget"
            
            # ApproverLevel =  blgetFieldValue(ID,field)
            
            # if (form.instance.QueSeries == (ApproverLevel[0].get(field)-1)): 
            #     form.instance.QueSeries = 99 # Random far end number to show all closed
            # else:
            #     form.instance.QueSeries += 1

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

        
       
        lstSignatoriesTimeStamp= blgettimeStampforSignatories (idAI, Signatories) 


        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(idAI)
        context['Approver'] = True
        context ['Signatories'] = Signatories
        return context

    def get_queryset(self):
       return self.object.attachments_set.all()

    def get_success_url(self):
        return reverse ('ApproverConfirm', kwargs={'id': self.object.id})

class ApproverConfirm(UpdateView):
    
    template_name = "userT/ApproverConfirmation.html"
    form_class = frmApproverConfirmation
    success_url = '/ApproverList/'
    
    def form_valid(self,form):
        if (self.request.POST.get('Cancel')):
#             
           return HttpResponseRedirect('/ApproverList/')

        if (self.request.POST.get('ApproveConfirm')): 
                #  need another intermediate screen for approval no comments
            
            ID =self.kwargs["id"]
           
            field = "QueSeriesTarget"
            
            ApproverLevel =  blgetFieldValue(ID,field)
            
            if (form.instance.QueSeries == (ApproverLevel[0].get(field)-1)): 
                form.instance.QueSeries = 99 # Random far end number to show all closed
            else:
                form.instance.QueSeries += 1

            return super().form_valid(form)

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
      
        return queryset.get(id=self.kwargs['id'])

class HistoryConfirm(UpdateView):
    
    template_name = "userT/historyconfirmpull.html"
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
            

            # field = "QueSeriesTarget"
            
            # ApproverLevel =  blgetFieldValue(ID,field)
            
            # if (form.instance.QueSeries == (ApproverLevel[0].get(field)-1)): 
            #     form.instance.QueSeries = 99 # Random far end number to show all closed
            # else:
            #     form.instance.QueSeries += 1

            return super().form_valid(form)

    def get_object(self,queryset=None):
        queryset=ActionItems.objects.all()
      
        return queryset.get(id=self.kwargs['id'])

class HistoryItemsMixin(ApproveItemsMixin):
    template_name = "userT/historyPullBack.html"
    form_class = frmApproverConfirmation
    
    def get_context_data(self,**kwargs):
        id = self.object.id #its actually the id and used as foreign key
        
        context = super().get_context_data(**kwargs)
        
        discsuborg = blgetDiscSubOrgfromID(id)
        ApproverLevel = blgetApproverLevel(discsuborg)
        
        blsetApproverLevelTarget(id,ApproverLevel)
        
        Signatories = blgetSignotories(discsuborg)
        
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(id)
        context['Approver'] = False
        context ['ApproverLevel'] = ApproverLevel
        context ['Signatories'] = Signatories
        
        return context

    def get_success_url(self):
        return reverse ('HistoryConfirm', kwargs={'id': self.object.id })

class ActioneeItemsMixin(ApproveItemsMixin):
    template_name = "userT/actionUpdateApproveAction.html"
    form_class = frmUpdateActioneeForm
    
    def get_context_data(self,**kwargs):
        fk = self.kwargs.get("pk") #its actually the id and used as foreign key
        context = super().get_context_data(**kwargs)
        

        discsuborg = blgetDiscSubOrgfromID(fk)
        ApproverLevel = blgetApproverLevel(discsuborg)
        
        blsetApproverLevelTarget(fk,ApproverLevel)
        
        Signatories = blgetSignotories(discsuborg)
        
        
        
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        context['Approver'] = False
        context ['ApproverLevel'] = ApproverLevel
        context ['Signatories'] = Signatories
        
        return context

    def get_success_url(self):
        return reverse ('multiplefiles', kwargs={'forkeyid': self.object.id})

def ContactUs (request):
    return render(request, 'userT/ContactUs.html')

class RejectReason (CreateView):
    model = Comments
    template_name = 'userT/rejectReason.html'
    form_class = frmAddRejectReason
    success_url = '/ApproverList/'

    def form_valid (self,form):
        if (self.request.POST.get('Reject')):
            ID = self.kwargs['forkeyid']
            #set using model manager since we want it back to actionee it has to be set at QueSeries=0
            ActionItems.mdlQueSeries.mgrsetQueSeries(ID,0)
            
            form.instance.Action_id = ID
            form.instance.Username = self.request.user.email
            rejectreason =  form.instance.Reason
            listSubjectContent = blbuildRejectionemail (ID, rejectreason)
            
            

            
            discsub = blgetDiscSubOrgfromID(ID)
            
            
            Signatoryemails = blgetSignatoryemail(discsub)
            ContentSubject  =blbuildRejectionemail(ID,rejectreason)

            success = emailSendindividual(emailSender,Signatoryemails,ContentSubject[0], ContentSubject[1]) #send email, the xyz is dummy data and not used
            
            return super().form_valid(form)
        if (self.request.POST.get('Cancel')):
            #cant use success url, its got assocaition with dict object, so have to use below
            
            return HttpResponseRedirect('/ApproverList/')
    def get_context_data(self, **kwargs):
        fk = self.kwargs['forkeyid']
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        return context

def IndividualBreakdownByUsers(request):
    #Need to do some maths here  most of the functions have been charted out just need to remap back to individual
    # 2 functions need to merge
    discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
   
    #Signatories = 
    
    QueOpen = [0,1,2,3,4,5,6,7,8,9]
    QueClosed = [99]
    Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)          
   
    context = {
        
        'Indisets' : Indisets,
        
    }
            
    return render(request, 'userT/Indibreakbyuser.html',context)

def IndividualBreakdownByActions(request):
    
    allactions = ActionItems.objects.all()
                #blgetdetailsofeachActions(allactions)
    lstattributes = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','InitialRisk']
   
    lstofindiactions = blgetActionStuckAt(allactions, lstattributes)

    context ={
        
        'context' : lstofindiactions

    }

    return render(request, 'userT/Indibreakdownbyactions.html', context)

def ContactUs (request):
    return render(request, 'userT/ContactUs.html')

def multiplefiles (request, **kwargs):
  
    form_multi = frmMultipleFiles()
        
    if (request.POST.get('Upload')):
        
        ID = kwargs['forkeyid']
        #set using model manager since we want it back to actionee it has to be set at QueSeries=0
        files = request.FILES.getlist('Attachment')
        for file in files:
            #should be doing via model manager , the problem is its justa line of code
            x = Attachments.objects.create(
                Attachment=file,
                Action_id=ID,
                Username=request.user.email
            )

        ActionItems.mdlQueSeries.mgrsetQueSeries(ID,1)
        
        return HttpResponseRedirect('/ActioneeList/')
            
    if (request.POST.get('Cancel')):
            #cant use success url, its got associattion with dict object, so have to use below

             return HttpResponseRedirect('/ApproverList/')

        
    context = {
        'form_multi' : form_multi

    }

    return render(request, 'userT/multiplefiles.html',context)



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
          
            createExcelReports(request)
            
        if ActionStatus =='Open':
            chartChanges = []
            if ActionsSorton == 'Company':
                
                Company = ActionRoutes.mdlAllCompany.mgr_getCompanyCount()
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
                Company = ActionRoutes.mdlAllCompany.mgr_getCompanyCount()
                
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
    return render (request, 'userT/reports.html',context )

def rptdiscSlice(request, **kwargs):
    
    #Function on businees logic to get data based on Queseries, Actionee and Approver levels
    #most of the data is
    TotalCount = [0,1,2,3,4,5,6,7,8,9,99]  #yhs updated to make flexible path
    OpenAccount = [0,1,2,3,4,5,6,7,8,9]
    ApproverQList = [1,2,3,4,5,6,7,8,9]
    ActioneeQlist = [0]
    Company = ActionRoutes.mdlAllCompany.mgr_getCompanyCount()
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
    return render (request, 'userT/repDisc.html', context)

def rptbyUser(request, **kwargs):
    context_allRou = getuserRoutes(request,request.user.email)
    Actionee_R =    context_allRou.get('Actionee_Routes')
    
    #This function just does a count using model managers , calling from businesslogic.py
    ActioneeCount = blfuncActionCount(Actionee_R,0)
    return render (request, 'userT/reports.html')
    
def GeneratePDF (request):
    filename = [] # for appending filename place before for loop
    if (request.POST.get('GeneratePDF')):      
        x=ActionItems.objects.all()  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
        y= x.values()          
        for item in y :            
            i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file  
            j = (i + '.pdf')  # easier to breakdown j           
            del item["id"]      
            data_dict=item       
            x = 'static/multiple.pdf'             
            out_file = 'static/media/' + j   # sending file to media folder inside static folder                                                        
            generated_pdf = pypdftk.fill_form(
                pdf_path = x,
                datas = data_dict,
                out_file = out_file,                             
            )
            filename.append(str(generated_pdf)) #can only append str   
            context={
                 'filename' : filename,
                 'table': True
            }
                              
        return render(request, 'userT/GeneratePDF.html', context)                    
    return render(request, 'userT/GeneratePDF.html')

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
        return render(request, 'userT/ReportingTable.html',context)
    return render (request, 'userT/ReportingTable.html', {'form':sub})

#def EmailReminder (request):
#    return render(request, 'userT/EmailReminder.html')

def EmailReminder(request):
    sub = Subscribe()
    if request.method == 'POST':
        sub = Subscribe(request.POST)
        recepient = str (sub ['Email'].value())
        
        context_allRou = getuserRoutes(request,recepient)
        Actionee_R =    context_allRou.get('Actionee_Routes')  
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
        return render(request, 'userT/EmailReminder.html',context)
    return render (request, 'userT/EmailReminder.html', {'form':sub})

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
    return render (request, 'userT/EmailReminder.html', {'form':sub})


    

def Profile (request):
    return render(request, 'userT/Profile.html')

def repPMTExcel (request):
   
    #Signatories = 
    #get individual actions
    QueOpen = [0,1,2,3,4,5,6,7,8,9]
    QueClosed = [99]
    discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
    Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)   
    #YHS
    print(Indisets)
    #YHS
    tableindiheader = ['User','Role', 'Open Actions' ,'Pending Res/Appr','Organisation Route','Closed']
    #Get all Actions
    allactions = ActionItems.objects.all()

    tableallheader = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','Response','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
    lstofallactions = blgetActionStuckAt(allactions, tableallheader) #basically you feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
    
    #lastly
    
    YetToRespondQue =[0]
    ApprovalQue = [1,2,3,4,5,6,7,8,9]

    allstudies = Studies.objects.all()
    tablestudiesheader = ['Studies','Open Actions', 'Yet to Respond' ,'Pending Appr','Closed']
    disciplinestatusheader = ['Disipline','Open Actions', 'Yet to Respond' ,'Pending Appr','Closed']
    lstbyWorkshop = blgetbyStdudiesCount(allstudies,QueOpen,YetToRespondQue,ApprovalQue,QueClosed)
   #YHS

   # lstbydiscipline = blgetbyDispCount(discsuborg,QueOpen,YetToRespondQue,ApprovalQue,QueClosed)  #HOLD

#YHS end of test code
    if request.method == 'POST':
                
        if (request.POST.get('allActions')):
          
            #workbook= createExcelReports(request,"\\excelDownload\\AllActions3.xlsx")
            tableallheader.append("Current Actionee/Approver") #appends the last column that the list spits out
            workbook = excelAllActions(lstofallactions,tableallheader,"All Action Items")
            
            response = HttpResponse(content_type='application/ms-excel') #
            response['Content-Disposition'] = 'attachment; filename=AllActions6.xlsx' 
            workbook.save(response) # odd fucking way but it works - took too long to figure out as no resource on the web
            return response
        elif (request.POST.get('indiActions')):
            

            workbook = excelAllActions(Indisets,tableindiheader,"Individual Actions")
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=AllActions6.xlsx' 
            workbook.save(response) # odd fucking way but it works - took too long to figure out as no resource on the web
            return response

        elif (request.POST.get('allStudies')):
            

            workbook = excelAllActions(lstbyWorkshop,tablestudiesheader,"Workshop Actions")
            
            response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
            response['Content-Disposition'] = 'attachment; filename=AllActions6.xlsx' 
            workbook.save(response) # odd fucking way but it works - took too long to figure out as no resource on the web
            return response
            

    context = {

        'lstbyWorkshop' : lstbyWorkshop,
        'Indisets' : Indisets,
        'lstofallactions' : lstofallactions,
        'tableindiheader' : tableindiheader,
        'tablestudiesheader' : tablestudiesheader,
        'tableallheader' : tableallheader,
        'disciplinestatusheader' : disciplinestatusheader, #YHS Test
        #'lstbydiscipline' : lstbydiscipline, #YHS Test
    }
    return render(request, 'userT/repPMTExcel.html', context)

def DisciplineBreakdown (request):
    return render(request, 'userT/DisciplineBreakdown.html')

def StickyNote(request):
    return render(request, 'userT/StickyNote.html')


def PDFtest(request):
    run()
    return HttpResponse('TEST')

#this part need to be tidied up. For time's sake i just copy from def (repPMTExcel). by YHS
def closeoutsheet(request): #new naming convention - all small letters
    QueOpen = [0,1,2,3,4,5,6,7,8,9]
    QueClosed = [99]
    YetToRespondQue =[0]
    ApprovalQue = [1,2,3,4,5,6,7,8,9]
    allstudies = Studies.objects.all()
    lstbyWorkshop = blgetbyStdudiesCount(allstudies,QueOpen,YetToRespondQue,ApprovalQue,QueClosed)
    allactions = ActionItems.objects.all()
    tableallheader = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','Response','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
    lstofallactions = blgetActionStuckAt(allactions, tableallheader) #basically you feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
    
    

    context = {

        'lstbyWorkshop' : lstbyWorkshop,
        'lstofallactions' : lstofallactions,
        
    }

    return render(request, 'userT/closeoutsheet.html', context)

def pdftest(request):
    filename = [] # for appending filename place before for loop
    if (request.POST.get('allActions')): 
        x=ActionItems.objects.filter(StudyName='HAZID')  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
        y= x.values()          
        for item in y :            
            i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file  
            j = (i + '.pdf')  # easier to breakdown j           
            del item["id"]      
            data_dict=item
            pdfgenerate('atrtemplateautofontreadonly.pdf',j,data_dict)
            filename.append(str(pdfgenerate)) #can only append str   
            context={
                'filename' : filename,
                'table': True
            }
            
            #return HttpResponse('TEST')
            return render(request, 'userT/closeoutsheet.html', context)
        return render(request, 'userT/closeoutsheet.html') 



