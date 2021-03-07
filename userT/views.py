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

#from .forms import UserRegisterForm
# Create your views here.
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
    #get user routes from workflow for everything , actionee and approver1
    #userRoutes simply tied into model manager
    Approver = []
    context_allRou = getuserRoutes(request)
    Actionee_R =    context_allRou.get('Actionee_Routes')
    
    Approver_R =    context_allRou.get('Approver_Routes')
    
    for key, value in Approver_R.items():
         Approver.insert(key,blfuncActionCount(value,key))
    
    Approver1_R =    context_allRou.get('Approver1_routes')
    # Approver2_R =    context_allRou.get('Approver2_routes')
    # Approver3_R =    context_allRou.get('Approver3_routes')
    # Approver4_R =    context_allRou.get('Approver4_routes')
    # Approver5_R =    context_allRou.get('Approver4_routes')
    #logic stored in businesslogic.py, actionee queue = 0 approver1=1, approver2=2 etc
    ActioneeCountList = blfuncActionCount(Actionee_R,0)
    
    
    # Approver [i] = blfuncActionCount(Approver_R[i],i)
    print (Approver)
    Approver1CountList = blfuncActionCount(Approver1_R,1)
    # Approver2CountList = blfuncActionCount(Approver2_R,2)
    # Approver3CountList = blfuncActionCount(Approver3_R,3)
    # Approver4CountList = blfuncActionCount(Approver4_R,4)
    # Approver5CountList = blfuncActionCount(Approver5_R,5)
   # ApproverCountList = 
    print (Approver1CountList)
    print (ActioneeCountList)
    Context = {
        'Actionee_Count' : ActioneeCountList,
        'Approver_Count'       : Approver
      
            }
    return render(request, 'userT/ActioneeItems.html',Context)

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
    
    
    for ApproverLevel in range(1 , ApproverLevel+1):
       Approver_Routes [ApproverLevel]  =  ActionRoutes.ApproverRo.get_myroutes(userZemail,ApproverLevel)
      
    
    Approver1_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,1)
    Approver2_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,2)
    Approver3_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,3)
    Approver4_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,4)
    Approver5_routes    =  ActionRoutes.ApproverRo.get_myroutes(userZemail,5)
    contextRoutes = {
       'Actionee_Routes' : Actionee_Routes,
       'Approver_Routes': Approver_Routes,
       'Approver1_routes' : Approver1_routes,
       'Approver2_routes' : Approver2_routes,
       'Approver3_routes' : Approver3_routes,
       'Approver4_routes' : Approver4_routes,
       'Approver5_routes' : Approver5_routes,
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
        return getActioneeItemsbyStream(ActioneeRoutes,0)

class ActionDetailsForm (DetailView):
    model = ActionItems

    def get_object(self, **kwargs):
        pass