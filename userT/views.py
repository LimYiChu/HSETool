from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib.auth import get_user_model
import matplotlib as plt
from .businesslogic import *
from .models import *
from UploadExcel.models import ActionItems
from django.views.generic import ListView, DetailView, UpdateView,TemplateView
#test for login required
from django.contrib.auth.decorators import login_required

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

class yourActions (ListView):
    template_name   =   'userT/Actionlist.html'
    #queryset = ActionItems.objects.all()
    model = ActionItems
    #userOrganisation = user.organisation
    def get_queryset(self):
        userZOrg = self.request.user.organisation
        userZDis =  self.request.user.disipline
        userZSubD =  self.request.user.subdisipline
        #return ActionItems.objects.filter(Organisation__icontains='Hess')
        return ActionItems.objects.filter(Organisation__icontains=userZOrg).filter(Disipline__icontains=userZDis).filter(Subdisipline__icontains=userZSubD)

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
            
        ActioneeRoutes =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
        actioneeItems = blfuncActioneeComDisSub(ActioneeRoutes,0)
        #print(actioneeItems)
        for X in (ApproverActions):
            print(X)
        #print (ApproverActions)
        return ApproverActions

class DetailActioneeItems (DetailView):
    template_name   =   'userT/actionDetailActionee.html'
    #queryset = ActionItems.objects.all()

    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)

class UpdateActioneeItems (UpdateView):
    template_name   =   'userT/actionUpdateApproveAction.html'
    #queryset = ActionItems.objects.all()
    form_class = UpdateActioneeForm
    success_url = '/ActioneeList/'
    def get_object(self):
        id1 = self.kwargs.get("id")
        return get_object_or_404(ActionItems, id=id1)

    def form_valid(self,form):
        if (super().form_valid(form)):
            #if form is valid just increment q series by 1 so it goes to Approver que so it goes to next queSeries
            #form.instance.QueSeries += 1
            return super().form_valid(form)

class ApproveItems (DetailView):
    template_name   =   'userT/actionUpdateApproveAction.html'
    
    success_url = '/ApproverList/'
    
    def get_context_data(self,**kwargs):
        context = super(ApproveItems,self).get_context_data(**kwargs)
        context ['form'] = ApproverForm
        return context

    def get_object(self):
         id1 = self.kwargs.get("id")
         print(id1)
         return get_object_or_404(ActionItems, id=id1)

    def form_valid(self,form):
        if (super().form_valid(form)):
            #if form is valid just increment q series by 1 so it goes to Approver que so it goes to next queSeries
            form.instance.QueSeries += 1
            return super().form_valid(form)

#yhs testing for adding urls views
def ContactUs (request):
   return render(request, 'userT/ContactUs.html')

