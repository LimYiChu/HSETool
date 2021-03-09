from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model
import matplotlib as plt
from .businesslogic import *
from .models import *
from UploadExcel.models import ActionItems
from django.views.generic import ListView, DetailView, UpdateView,TemplateView

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
    # a route example is in Action routes table Say EHS: Technical Safety - then there is emails defined for Actionee and Approvers
    for i in range(len(ActioneeCount)):
        labelsActionee.append('Stream'+str(i+1))
        dataActionee.append(ActioneeCount[i])
       
    #get count for all approver levels just by looping through the key
    #Not very accurate but im summing approver level actions together
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
    Actionee_Routes   =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
    
    #Optimised to get all approver levels
    for ApproverLevel in range(1 , ApproverLevel+1):
       Approver_Routes [ApproverLevel]  =  ActionRoutes.ApproverRo.get_myroutes(userZemail,ApproverLevel)
      
      #delete below in green once done
    #Approver1_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,1)
   # Approver2_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,2)
    
    contextRoutes = {
       'Actionee_Routes' : Actionee_Routes,
       'Approver_Routes': Approver_Routes,
       
    }
    
    #return render(request, 'userT/RouteList.html',contextRoutes)
    return contextRoutes
# class yourRoutes (ListView):
#     #template_name   =   'userT/Actionlist.html'
#     template_name   =   'userT/Routes.html'
#     #queryset = ActionItems.objects.all()
#     model = Routes
#     #userOrganisation = user.organisation
#     def get_queryset(self):
#         userZOrg = self.request.user.organisation
#         userZDis =  self.request.user.disipline
#         userZSubD =  self.request.user.subdisipline
#         userZemail = self.request.user.email

#         if Routes.objects.filter(Actionee__icontains=userZemail):
#             #ActionItems.objects.filter(organisation__icontains=userZOrg).filter(Disipline__icontains=userZDis).filter(Subdisipline__icontains=userZSubD)
#             #return ActionItems.objects.filter(organisation__icontains=userZOrg).filter(Disipline__icontains=userZDis).filter(Subdisipline__icontains=userZSubD)
#             return Routes.objects.filter(Actionee__icontains=userZemail)
class ActioneeList (ListView):
    template_name   =   'userT/ActioneeList1st.html'
    
    
    def get_queryset(self):
        userZemail = self.request.user.email
        ActioneeRoutes =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
        actioneeItems = blfuncActioneeComDisSub(ActioneeRoutes,0)
        #print (actioneeItems)
        return actioneeItems
class ActionDetailsForm (DetailView):
    model = ActionItems

    def get_object(self, **kwargs):
        pass