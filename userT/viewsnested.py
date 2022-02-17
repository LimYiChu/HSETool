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

import json

import datetime
from datetime import date as dt
from operator import itemgetter
from collections import OrderedDict
from collections import Counter #Ishna 20211209
#edward 20210924
from django.forms.models import model_to_dict
from django.db.models import F
#edward 20211027 bulk pdf fix for large file dl
from django.http import StreamingHttpResponse
#edward 20211122 stitch pdf
# import xlwings as xw
#20211202 edward commented out this import because there is a problem with img2pdf library on linux
# import img2pdf
# from PIL import Image
#edward 20211207 
from datetime import datetime as dtime
from django.utils import timezone
#20211227 edward importing formstudies
from UploadExcel.formstudies import *
from time import time


def nestedstudy(request):

    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)

        all_actions =   ActionItems.objects.all().values()
        all_actionwithfk = blannotatefktomodel(all_actions)
        all_actionsopt = bladdriskelements(all_actionwithfk)
        dfalllist = blgetActionStuckAtdict(all_actionsopt) # getting a list of everything
        dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
        dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation']
        dfallnestedstudysorted = blsortdataframes(dfall,dfstudiescolumns) # sort dfall
        dfsortbystudy = dfallnestedstudysorted[dfallnestedstudysorted["StudyName"] == data ] #this value should be modular like phases, need to look up ajax more to get this to work
        
        dfstudieslist = dfsortbystudy.values.tolist()
        dfstudiesdict = dfsortbystudy.to_dict()
        
        lstofcount = blnestedchart(dfsortbystudy)
        countclosed = lstofcount[0]
        countopen = lstofcount[1]
       
        nestedheader = ['Study Action No', 'DueDate' ,'Action With','Discipline','Initial Risk']

        context = {
        'dflist':dfstudieslist,
        'nestedheader' : nestedheader,
        'dfstudiesdict': dfstudiesdict,
        'donutclose' : countclosed,
        'donutopen' : countopen,

        }
     
        return JsonResponse(context,status=200)
    else:
        return render(request, 'userT/inclnestedstudytable.html')


def nestedindisumm(request):
    
    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)

        all_actions =   ActionItems.objects.all().values()
        all_actionwithfk = blannotatefktomodel(all_actions)
        all_actionswithrisk = bladdriskelements(all_actionwithfk)
        dfalllist = blgetActionStuckAtdictnestedindisumm(all_actionswithrisk) # getting a list of everything
        dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
        dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation'] # combining discsuborg
        dfallindisummsorted = blsortdataframes(dfall,dfindinestedcolumns) # sort dfall
        dfsortbyindi = dfallindisummsorted[dfallindisummsorted["Action with"] == data ] #this value should be modular like phases, need to look up ajax more to get this to work
        dfindisummlist = dfsortbyindi.values.tolist()
        print(dfsortbyindi)
        nestedheader = ['StudyActionNo','DueDate','Study Name','Discipline','Initial Risk']
        context =   {
                    'dflist':dfindisummlist,
                    'nestedheader' : nestedheader,
                    }
     
        return JsonResponse(context,status=200)
    else:
        return render(request, 'userT/inclnestedindisummtable.html')


def nesteddiscipline(request):
    
    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)

        all_actions =   ActionItems.objects.all().values()
        all_actionwithfk = blannotatefktomodel(all_actions)
        dfalllist = blgetActionStuckAtdict(all_actionwithfk) # getting a list of everything
        dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
        dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation'] # combining discsuborg
        dfallnesteddisciplinesorted = blsortdataframes(dfall,dfdisciplinecolumns) # sort dfall
        dfsortbydiscipline = dfallnesteddisciplinesorted[dfallnesteddisciplinesorted["discsuborg"] == data ] #this value should be modular like phases, need to look up ajax more to get this to work
        dfdisclist =  dfsortbydiscipline.values.tolist()

        lstofcount = blnestedchart(dfsortbydiscipline)
        countclosed = lstofcount[0]
        countopen = lstofcount[1]

        nestedheader = ['Study Action No', 'Study Name' ,'Due Date','Action with' ]
        context =   {
                    'dflist':dfdisclist,
                    'nestedheader' : nestedheader,
                    'donutclose' : countclosed,
                    'donutopen' : countopen,
                    }
     
        return JsonResponse(context,status=200)
    else:
        return render(request, 'userT/inclnestedisciplinetable.html')