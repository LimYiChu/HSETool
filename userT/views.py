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
#test for login required
from django.contrib.auth.decorators import login_required

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

def home (request):
    return render(request, 'userT/home.html' )

def UserActions(request):
    #user = get_user_model(email)
    return HttpResponse(request.user.organisation)

def mainDashboardOLD (request):
    
    context_allRou = userRoutes(request)
    #print(context_allRou)
    #XX = context_allRou.get('Actionee_routes')
    #for items in XX:
     #   y= (items.Organisation)
      #  ActioneeItemsX  =   ActionItems.ActioneeItems.get_myItems(y)
    Actionee_R =    context_allRou.get('Actionee_routes')
    Approver_R =    context_allRou.get('Approver1_routes')
    firstStreamActionee,secondStreamActionee,thirdStreamActionee = blfuncActioneeComDisSub(Actionee_R)
    firstStreamApp1st,secondStreamApp1st,thirdStreamApp1st = blfuncActioneeComDisSub(Approver_R)
    #firstStreamApprover,secondStreamApprover, thirdStreamApprover = blfuncActioneeComDisSubApprover(context_allRou)
    newContext = {
        'obj_Actionee1st' : firstStreamActionee,
        'obj_Actionee2nd' : secondStreamActionee,
        'obj_Actionee3rd' : thirdStreamActionee,
        'obj_Approver11' : firstStreamApp1st,
        'obj_Approver12' : secondStreamApp1st,
        'obj_Approver13' : thirdStreamApp1st,
    }
    #return render(request, 'userT/RouteList.html',context_allRou)
    return render(request, 'userT/Actionlist.html',newContext)
    
def mainDashboard (request):
    #get user routes from workflow for everything , actionee and approver1
    #userRoutes simply tied into model manager
    context_allRou = userRoutes(request)
    Actionee_R =    context_allRou.get('Actionee_routes')
    Approver_R =    context_allRou.get('Approver1_routes')

    #logic stored in businesslogic.py
    ActioneeCountList = blfuncActioneeCount(Actionee_R)
   # ApproverCountList = 
    Context = {
        'Actionee_Count' : ActioneeCountList,
            
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
def userItems():
    pass
    #userOrganisation = 
def userRoutes(request):
    userZemail = request.user.email
    Actionee_routes   =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
    Approver1_routes    =  ActionRoutes.Approver1Ro.get_myroutes(userZemail)
    Approver2_routes    =  ActionRoutes.Approver2Ro.get_myroutes(userZemail)
    Approver3_routes    =  ActionRoutes.Approver3Ro.get_myroutes(userZemail)
    Approver4_routes    =  ActionRoutes.Approver4Ro.get_myroutes(userZemail)
    Approver5_routes    =  ActionRoutes.Approver5Ro.get_myroutes(userZemail)
    contextRoutes = {
       'Actionee_routes' : Actionee_routes,
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