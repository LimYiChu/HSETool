from userT.models import *
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
#from .forms import UploadExlForm
from .forms import *
from .models import *
import matplotlib as plt
from .models import *
import csv
import pandas as pd
import re
import datetime
#from .filter import ActionItemsFilter - not sure might need this for later for upload excel. had to remove stuff in filter.py
#from .forms import UserRegisterForm
# Create your views here.
@csrf_exempt

def loadriskmatrix (request):

    form_upload= UploadExlForm()

    #just reusing codes mostly from below but with data frames, hope it works better
    if request.method == 'POST':
        #UploadExl.objects.all().delete()
       # ActionItems.objects.all().delete()
       
        form_upload = UploadExlForm(request.POST ,request.FILES)
        if form_upload.is_valid():
            
            matrix = 5
            firstmatrixset =10
            form_upload.instance.Username = request.user.email
            form_upload.save()
            ID = form_upload.instance.id
            form_upload = UploadExlForm()
            obj = UploadExl.objects.get(id=ID)
           
            data_df = pd.read_excel(obj.Filename.path,nrows=matrix,keep_default_na=False)
            
            
            listofcombined = [] 
            for i in range (1,matrix+1):
                
                listofcombined.extend(data_df[i].tolist())
            bulklist =[]
            #Ranking=val[val.find("//")+2:]
            for val in listofcombined:
                valsplit = val.split("::")
                
                bulklist.append(RiskMatrix(Combined=valsplit[0], Consequence=valsplit[0][0],Likelihood=valsplit[0][1],
                
                                Ranking=valsplit[1],RiskColour=valsplit[2]))
            
            #[RiskMatrix(Combined=val[0:2], Consequence=val[0],Likelihood=val[1],Ranking=re.search("::")) for val in listofcombined]
            RiskMatrix.objects.bulk_create(bulklist)
            messages.add_message(request, messages.SUCCESS, 'File Uploaded Successfully')
            #print ("COLUMNS",data_df[1].tolist())
            # with open (obj.Filename.path, 'r') as input_file:
            #     csv_reader = csv.reader(input_file)
            #     next(csv_reader)

    context = {
        'form_upload' : form_upload

    }

    return render(request, 'uploadexcel/upload.html', context)

def Load (request):
    
    if request.method == 'POST':
        #UploadExl.objects.all().delete()
       # ActionItems.objects.all().delete()
        form_upload = UploadExlForm(request.POST ,request.FILES)
        if form_upload.is_valid():
            form_upload.instance.Username = request.user.email
            form_upload.save()
            ID = form_upload.instance.id
            form_upload = UploadExlForm()
            obj = UploadExl.objects.get(id=ID)
            
            with open (obj.Filename.path, 'r') as input_file:
                csv_reader = csv.reader(input_file)
                next(csv_reader)
                for i, row in enumerate(csv_reader):
                    
                    
                    objdateformat=datetime.datetime.strptime(row[15], '%d/%m/%Y')
                    #new_dateformat=datetime.datetime.strptime(old_dateformat, '%m/%dd/%YYYY').strftime('%YYYY-%mm-%dd')
                    
                    ActionItems.objects.create(
                    StudyActionNo= row [1],
                    StudyName= row[2],
                    Facility=row[3],
                    ProjectPhase=row[4],
                    Cause= row [5],
                    Consequence= row[6],
                    Safeguard = row[7],
                    InitialRisk = row [8],
                    Recommendations= row[9],
                    ResidualRisk = row[10],
                    Organisation=row[11],
                    Disipline=row[12],
                    Subdisipline=row[13],
                    FutureAction=row[14],
                    DueDate=objdateformat,
                    Guidewords = row[16],
                    #QueSeries=row[17],
                    Deviation = row[18],
                    )
            messages.add_message(request, messages.SUCCESS, 'File Uploaded Successfully')
    else:
        form_upload= UploadExlForm()
    
    context = {
        'form_upload' : form_upload

    }

    return render(request, 'uploadexcel/upload.html', context)
def uploadfield (request):
    
    if request.method == 'POST':
        #UploadExl.objects.all().delete()
       # ActionItems.objects.all().delete()
        form_upload = UploadExlForm(request.POST ,request.FILES)
        if form_upload.is_valid():
            form_upload.instance.Username = request.user.email
            form_upload.save()
            ID = form_upload.instance.id
            form_upload = UploadExlForm()
            obj = UploadExl.objects.get(id=ID)
            
            with open (obj.Filename.path, 'r') as input_file:
                csv_reader = csv.reader(input_file)
                next(csv_reader)
                for i, row in enumerate(csv_reader):
            
                    ActionItems.objects.create(
                    StudyActionNo= row [1],
                    StudyName= row[2],
                    Facility=row[3],
                    ProjectPhase=row[4],
                    Cause= row [5],
                    Consequence= row[6],
                    Safeguard = row[7],
                    InitialRisk = row [8],
                    Recommendations= row[9],
                    ResidualRisk = row[10],
                    Organisation=row[11],
                    Disipline=row[12],
                    Subdisipline=row[13],
                    FutureAction=row[14],
                    DueDate=row[15],
                    Guidewords = row[16],
                    #QueSeries=row[17],
                    
                    )
            messages.add_message(request, messages.SUCCESS, 'File Uploaded Successfully')
    else:
        form_upload= UploadExlForm()
    
    context = {
        'form_upload' : form_upload

    }

    return render(request, 'uploadexcel/upload.html', context)    
def LoadRoutes (request):
    #to load routes from excel when required
    pass


#YHS added
def AddonLoad (request):
    
    if request.method == 'POST':
        #UploadExl.objects.all().delete()
       # ActionItems.objects.all().delete()
        form_upload = UploadExlForm(request.POST ,request.FILES)
        if form_upload.is_valid():
            form_upload.instance.Username = request.user.email
            form_upload.save()
            ID = form_upload.instance.id
            form_upload = UploadExlForm()
            obj = UploadExl.objects.get(id=ID)
            
            with open (obj.Filename.path, 'r') as input_file:
                csv_reader = csv.reader(input_file)
                next(csv_reader)
                for i, row in enumerate(csv_reader):
            
                    ActionItems.objects.create(
                    StudyActionNo= row [1],
                    StudyName= row[2],
                    Facility=row[3],
                    ProjectPhase=row[4],
                    Cause= row [5],
                    Consequence= row[6],
                    Safeguard = row[7],
                    InitialRisk = row [8],
                    Recommendations= row[9],
                    ResidualRisk = row[10],
                    Organisation=row[11],
                    Disipline=row[12],
                    Subdisipline=row[13],
                    FutureAction=row[14],
                    DueDate=row[15],
                    Guidewords = row[16],
                    #QueSeries=row[17],
                    Deviation = row[18],
                    )
            messages.add_message(request, messages.SUCCESS, 'File Uploaded Successfully')
    else:
        form_upload= UploadExlForm()
    
    context = {
        'form_upload' : form_upload

    }

    return render(request, 'uploadexcel/addonupload.html', context)