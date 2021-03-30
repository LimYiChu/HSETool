from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
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
from UploadExcel.models import ActionItems
from django.views.generic import ListView, DetailView, UpdateView,TemplateView, CreateView
#test for login required
from django.contrib.auth.decorators import login_required
from django.conf import settings
import pypdftk
from django.views.generic.base import ContextMixin
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
    context_allRou = getuserRoutes(request)

    #Just get Actionee and Approver Routes, tied into model managers
    Actionee_R =    context_allRou.get('Actionee_Routes')
    Approver_R =    context_allRou.get('Approver_Routes')

    
    #This function just does a count using model managers , calling from businesslogic.py
    ActioneeCount = blfuncActionCount(Actionee_R,0)
    
    #Actionee is a different from approver wherein the pie/polar chart actually show the streams. Each stream is just a route
    # a route example is in Action routes table Say EHS: Technical Safety or Marine. 
    # 
    for i in range(len(ActioneeCount)):
        labelsActionee.append('Stream'+str(i+1))
        dataActionee.append(ActioneeCount[i])
       
    #get count for all approver levels just by looping through the key
    #Not very accurate but im summing approver level actions together
    # key is already rationalised in getuserRoutes
    for key, value in Approver_R.items():
        x= blfuncActionCount(value,key)
        Approver.insert(key,x)
        labelsApprover.append('ApproverLevel'+str(key))
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

def getuserRoutes(request):
    ApproverLevel = 5
    userZemail = request.user.email
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
        context_allRou = getuserRoutes(self.request)
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

class UpdateActioneeItems (UpdateView):
    template_name   =   'userT/actionUpdateApproveAction.html'
   
    form_class = UpdateActioneeForm
    success_url = '/ActioneeList/'
    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)

    def form_valid(self,form):
        if (super().form_valid(form)):
            #if form is valid just increment q series by 1 so it goes to Approver que so it goes to next queSeries
            
            form.instance.QueSeries += 1
            return super().form_valid(form)

    def get_context_data(self,**kwargs):
        fk = self.kwargs.get("id")
        context = super().get_context_data(**kwargs)
        context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(fk)
        return context
    
class ApproveItems (UpdateView):
    template_name   =   'userT/actionUpdateApproveAction.html'
    form_class = ApproverForm
    second_form_class = frmAddRejectReason #-loading multiple forms
    success_url = '/ApproverList/'
    
    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)

    def form_valid(self,form):
        
            #if form is valid just increment q series by 1 so it goes to Approver que so it goes to next queSeries
            if (self.request.POST.get('Reject')):
                #If reject que series should be 0, but need another intermediate screen for comments
                #form.instance.QueSeries = 0
                
                #Need to do below with HTTPResponseredirect because normal reverse seems to give an str error
                #reverse simply redirects to url path so can call class RejectReason below since cant really call it from fucntion call directly
                #makes sense since really django wants to work with views coming from URL paths- simply a strutured way of doing stuff
                return HttpResponseRedirect(reverse ('RejectComments', kwargs={'forkeyid': form.instance.id}))
                
            if (self.request.POST.get('Approve')): 
                #  need another intermediate screen for approval no comments
                form.instance.QueSeries += 1
                return super().form_valid(form)
    
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


#Develop PDF
def testing(self):    
    x=ActionItems.objects.filter(pk__icontains=20)
    y= x.values()
    for item in y :
        i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file (refer to line 216)
        del item["id"]      
        data_dict=item
        PDF_PATH = 'multiple.pdf' 
        out_file = i + 'out_file.pdf' 
        generated_pdf = pypdftk.fill_form(
            pdf_path = PDF_PATH,
            datas = data_dict,
            out_file = out_file,
        )
    return HttpResponse("this is a test")
        
