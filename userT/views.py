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
from Trackem.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.template import loader
from django.core.mail import EmailMessage


#import mixins
from django.views.generic.detail import SingleObjectMixin
#from .forms import UserRegisterForm
# Create your views here.

from UploadExcel.forms import *
@csrf_exempt

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
    #get all routes first
    context_allRou = getuserRoutes(request,request.user.email)
    
    #Just get Actionee and Approver Routes, tied into model managers
    Actionee_R =    context_allRou.get('Actionee_Routes')
    Approver_R =    context_allRou.get('Approver_Routes')

    print(Actionee_R)
    
    #This function just does a count using model managers , calling from businesslogic.py
    ActioneeCount = blfuncActionCount(Actionee_R,0)
    discsub = blgetActioneeDiscSub(Actionee_R)
    
    #Actionee is a different from approver wherein the pie/polar chart actually show the streams. Each stream is just a route
    # a route example is in Action routes table Say EHS: Technical Safety or Marine. 
    #
    for pairs in discsub:
        labelsActionee.append(pairs[0])
    for i in range(len(ActioneeCount)):
        
        dataActionee.append(ActioneeCount[i])
       
    #get count for all approver levels just by looping through the key
    #Not very accurate but im summing approver level actions together
    # key is already rationalised in getuserRoutes
    for key, value in Approver_R.items():
        x= blfuncActionCount(value,key)
        Approver.insert(key,x)
        labelsApprover.append('Level'+str(key))
        dataApprover.append(sum(x))
    #Context just returns to HTML so that we can use it in the HTML page
    Context = {
        'Actionee_Count' : ActioneeCount,
        'Approver_Count'       : Approver,
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
    ApproverLevel = 5
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
        actioneeItems = blfuncActioneeComDisSub(ActioneeRoutes,0)
     
        return actioneeItems
    
    
class ApproverList (ListView):
    template_name   =   'userT/actionListApprover.html'
    
    def get_queryset(self):
        userZemail = self.request.user.email
        ApproverActions = []
        context_allRou = getuserRoutes(self.request,userZemail)
        Approver_R =    context_allRou.get('Approver_Routes')
        
        for key, value in Approver_R.items():
            x = blfuncActioneeComDisSub(value,key)
            ApproverActions.insert(key,x)
            
        
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
       
        #self.object = self.get_object(queryset=ActionItems.objects.all())
        #return super().get(request, *args, **kwargs)
        #X = queryset.get(id=self.kwargs['pk'])
       
        return queryset.get(id=self.kwargs['pk'])
       
    def form_valid(self,form):
        
            #if form is valid just increment q series by 1 so it goes to Approver que so it goes to next queSeries
        if (self.request.POST.get('Reject')):
                #If reject que series should be 0, but need another intermediate screen for comments
                #form.instance.QueSeries = 0
            
                #Need to do below with HTTPResponseredirect because normal reverse seems to give an str error
                #reverse simply redirects to url path so can call class RejectReason below since cant really call it from fucntion call directly
                #makes sense since really django wants to work with views coming from URL paths- simply a strutured way of doing stuff
            context = {
                        'StudyActionNo' : form.instance.StudyActionNo


                }
            return HttpResponseRedirect(reverse ('RejectComments', kwargs={'forkeyid': form.instance.id}))

        if (self.request.POST.get('Cancel')):
#             
           return HttpResponseRedirect('/ActioneeList/')

        if (self.request.POST.get('Approve')): 
                #  need another intermediate screen for approval no comments
            form.instance.QueSeries += 1
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
        fk = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        context['Approver'] = True
        return context

    def get_queryset(self):
       return self.object.attachments_set.all()

class ActioneeItemsMixin(ApproveItemsMixin):
    template_name = "userT/actionUpdateApproveAction.html"
    form_class = frmUpdateActioneeForm
    
    def get_context_data(self,**kwargs):
        fk = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        context['Approver'] = False
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
            return super().form_valid(form)
        if (self.request.POST.get('Cancel')):
            #cant use success url, its got assocaition with dict object, so have to use below
            
            return HttpResponseRedirect('/ApproverList/')
    def get_context_data(self, **kwargs):
        fk = self.kwargs['forkeyid']
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        return context
        
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
    
    #Function on businees logic to get data based on Queseries, Actionee and Approver levels
    #most of the data is
    openActionsQueSeries = [0,1,2,3,4,5]
    closedActionsQueSeries = [6]
    allOpenActions= blfuncgetallAction('Y', openActionsQueSeries)
    allClosedActions = blfuncgetallAction('Y', closedActionsQueSeries)
    
    #this is for overall charts
    listofOpenClosed = [allOpenActions,allClosedActions]
    labelsOpenClosed = ['Open', 'Closed']
    chart = showPie(listofOpenClosed,labelsOpenClosed,"Overall Action Status")
    
    #this is for disc/sub-disipline
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
    #countDiscSub = ActionItems.mdlDisSub
    #important to separate list otherwise it will fuck it up
    listcountbyDisSub= []
    listlablesDisc =[]
    listcountbyCompany= []
    listlabelsCompany = []

    #default view
    for itemPair in discsub:
        
        listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,openActionsQueSeries))
        listlablesDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
    
    chartChanges = showPie(listcountbyDisSub,listlablesDisc, "Open Actions by Disc/Sub-Disc")

    #if generatePdf is hit
    if request.method == 'POST':
        ActionStatus = request.POST.get ('ActionStatus')
        ActionsSorton = request.POST.get ('SortOn')
        if ActionStatus =='Open':
            if ActionsSorton == 'Company':
                Company = ActionRoutes.mdlAllCompany.mgr_getCompanyCount()
                for items in Company:
                        listcountbyCompany.append(blgetCompanyActionCount (items,openActionsQueSeries))
                            #dont need to append list as its already in the list above
                chartChanges = showPie(listcountbyCompany,Company, "Open Actions by Company")
        else: #This is for closed actions if selected
            if ActionsSorton == 'Company':
                Company = ActionRoutes.mdlAllCompany.mgr_getCompanyCount()
                for items in Company:
                        listcountbyCompany.append(blgetCompanyActionCount (items,closedActionsQueSeries))
                            #dont need to append list as its already in the list above
                chartChanges = showPie(listcountbyCompany,Company, "Open Actions by Company")
    context = {
            "chart":chart,
            "chartChanges":chartChanges,
            "overall":True

    }
    return render (request, 'userT/reports.html',context )

def rptdiscSlice(request, **kwargs):
    
    #Function on businees logic to get data based on Queseries, Actionee and Approver levels
    #most of the data is
    TotalCount = [0,1,2,3,4,5,6]
    OpenAccount = [0,1,2,3,4,5]
    discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
    
    listcountbyDisSub= []
    listlablebyDisSub =[]
    totalcountbyDisSub = []
    Title = "Open Actions by Discipline"
    label1 = "Open Actions"
    label2 = "Total Actions"
    generalxlabel = "Discipline"

    for itemPair in discsub:
        
        listcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,OpenAccount))
        totalcountbyDisSub.append(blgetDiscSubActionCount ('Y',itemPair,TotalCount))
        listlablebyDisSub.append(str(itemPair[0])) # to include sub disc later -- +"/"+str(itemPair[1])
    
    chart = showbar(listcountbyDisSub,totalcountbyDisSub,listlablebyDisSub, label1,label2,generalxlabel,Title)

    context = {
            "chart":chart,
            "discpslice" : True
            }
    return render (request, 'userT/reports.html', context)
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
            print(context) # context now outside for loop                   
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
        Msg=EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
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
        
        Msg=EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
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
        Msg=EmailMessage(subject, message, EMAIL_HOST_USER, [recepient])
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

def AllActions (request):
    return render(request, 'userT/AllActions.html')

def DisciplineBreakdown (request):
    return render(request, 'userT/DisciplineBreakdown.html')
