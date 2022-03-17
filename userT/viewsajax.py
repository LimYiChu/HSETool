from django.db.models.fields import NullBooleanField
from django.forms.fields import JSONString
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

def dynamicstudiesexceldisc(request,data):

    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)
        print(data)
        filteredstring = {'StudyName__StudyName': data}
        reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation']

        actionsstuckat = bldynamicstudiesactionformat(filteredstring,reducedfields)
        discmultilist = bldynamicstudiesdisc(actionsstuckat)
        disclst = discmultilist[1]
        dfdisc = pd.DataFrame(disclst)
        dictheader = {0:'Discipline',1:'Pending Submission',2:'Submitted',3:'Closed',4:'Open Actions',5:'Total Actions'}
        dfdisc.rename(columns=dictheader,inplace=True)
        print(dfdisc)
        in_memory = BytesIO()
        response = HttpResponse(content_type='application/ms-excel') 
        response['Content-Disposition'] = 'attachment; filename=DisciplinebyStudies.xlsx'

        with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
            dfdisc.to_excel(writer, sheet_name='Discipline',engine='xlsxwriter',header=None,startrow=1)
            workbook = writer.book #gives excelwriter access to workbook
            worksheet = writer.sheets['Discipline'] #gives excelwriter access to worksheet
            formattedexcel = blexcelformat(dfdisc,workbook,worksheet)
            
        in_memory.seek(0)
        response.write(in_memory.read())
        print(response)
        
        return response
        

def dynamicstudies(request):

    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)

        filteredstring = {'StudyName__StudyName': data}
        reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation']
        headerlst = ['Study Action No', 'DueDate' ,'Action At','Discipline','Initial Risk']

        actionsstuckat = bldynamicstudiesactionformat(filteredstring,reducedfields)

        discmultilist = bldynamicstudiesdisc(actionsstuckat)
        discheaderlst = discmultilist[0]
        disclst = discmultilist[1]

        dfall = pd.DataFrame.from_dict(actionsstuckat) #puts it into df columns format
        dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation']
        dfalldynamicstudiessorted = blsortdataframes(dfall,dfstudiescolumns) # sort dfall
        dfstudieslst = dfalldynamicstudiessorted.values.tolist()

        lstofcount = bldynamicchart(dfalldynamicstudiessorted)
        countclosed = lstofcount[0]
        countopen = lstofcount[1]
        dfstuckatlst=bldynamicchartopen(dfalldynamicstudiessorted)

        headeropenclose = ['\\\Status:::', 'Number']
        lstofcount.insert(0,headeropenclose)
        
        multilst = [lstofcount,dfstuckatlst]

        dfdisc = pd.DataFrame(disclst)
        dictheader = {0:'Discipline',1:'Pending Submission',2:'Submitted',3:'Closed',4:'Open Actions',5:'Total Actions'}
        dfdisc.rename(columns=dictheader,inplace=True)
      

        
        # if request.method == 'POST':
        #     print('pass 1')
        #     if (request.POST.get('dynamicstudiesdisc')):
        #         print('pass 2')
        #         in_memory = BytesIO()
        #         response = HttpResponse(content_type='application/ms-excel') 
        #         response['Content-Disposition'] = 'attachment; filename=DisciplinebyStudies.xlsx'
            
        #         with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        #             dfdisc.to_excel(writer, sheet_name='Discipline',engine='xlsxwriter',header=None,startrow=1)
        #             workbook = writer.book #gives excelwriter access to workbook
        #             worksheet = writer.sheets['Discipline'] #gives excelwriter access to worksheet
        #             formattedexcel = blexcelformat(dfdisc,workbook,worksheet)
                    
        #         in_memory.seek(0)
        #         response.write(in_memory.read())
        #         return response
        
        context = {
        'multilst':multilst,
        'dflist':dfstudieslst,
        'headerlist' : headerlst,
        'donutclose' : countclosed,
        'donutopen' : countopen,
        'dfstuckatlst':dfstuckatlst,
        'discheaderlst':discheaderlst,
        'disclst':disclst,
        'data':data
        }
        return JsonResponse(context,status=200)
    else:
        return render(request, 'userT/incldynamicstudies.html')


def dynamicindisumm(request):
    
    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)

        # filteredstring = {'StuckAt':data}
        # reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation']

        # actionsbystudy = blgetsinglefilteractionsitemsQ(filteredstring,reducedfields) #getting actions based on studies filter
        # print(actionsbystudy)
        # filteredstring = {'QueSeries' : }
        # reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation','StudyName__StudyName']
        # actionsbydisc = blgetsinglefilteractionsitemsQ(filteredstring,reducedfields) 
        # print(actionsbydisc)
        all_actions =   ActionItems.objects.all().values()
        all_actionwithfk = blannotatefktomodel(all_actions)
        all_actionswithrisk = bladdriskelements(all_actionwithfk)
        dfalllist = blgetActionStuckAtdict(all_actionswithrisk) # getting a list of everything
        dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
        dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation'] # combining discsuborg
        dfallindisummsorted = blsortdataframes(dfall,dfindisummcolumns) # sort dfall
        dfsortbyindi = dfallindisummsorted[dfallindisummsorted["StuckAt"].str.contains(data) ] #this value should be modular like phases, need to look up ajax more to get this to work
        dfindisummlist = dfsortbyindi.values.tolist()
        
        headerlist = ['StudyActionNo','DueDate','Study Name','Discipline','Initial Risk']
        context =   {
                    'dflist':dfindisummlist,
                    'headerlist' : headerlist,
                    }
     
        return JsonResponse(context,status=200)
    else:
        return render(request, 'userT/incldynamicindisumm.html')


def dynamicdiscipline(request):
    
    if request.is_ajax and request.method == "GET":
        data = request.GET.get("data", None)

        discsuborglst = bldiscstrmatch(data)
        filteredstring = {'Disipline':discsuborglst[0],'Subdisipline':discsuborglst[1],'Organisation':discsuborglst[2]}
        reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation','StudyName__StudyName']
        actionsbydisc = blgetsinglefilteractionsitemsQ(filteredstring,reducedfields) 
        
        dfalllist = blgetdictActionStuckAt(actionsbydisc) # getting a list of everything
        dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
        dfalldynamicdisciplinesorted = blsortdataframes(dfall,dfdisciplinecolumns) # sort dfall
        dfdisclist =  dfalldynamicdisciplinesorted.values.tolist()

        lstofcount = bldynamicchart(dfalldynamicdisciplinesorted)
        countclosed = lstofcount[0]
        countopen = lstofcount[1]

        dfstuckatlst=bldynamicchartopen(dfalldynamicdisciplinesorted)

        headerlist = ['Study Action No', 'Study Name' ,'Due Date','Action At' ]

        headeropenclose = ['\\\Status:::', 'Number']
        lstofcount.insert(0,headeropenclose)
        
        multilst = [lstofcount,dfstuckatlst]

        discmultilist = bldynamicstudiesdisc(actionsbydisc)
        discheaderlst = discmultilist[0]
        disclst = discmultilist[1]
        print(discmultilist)
        context = {
                    'multilst':multilst,
                    'dflist':dfdisclist,
                    'headerlist' : headerlist,
                    'donutclose' : countclosed,
                    'donutopen' : countopen,
                    'dfstuckatlst':dfstuckatlst,
                    'discheaderlst':discheaderlst,
                    'disclst':disclst
                    }
     
        return JsonResponse(context,status=200)
    else:
        return render(request, 'userT/incldynamicdiscipline.html')