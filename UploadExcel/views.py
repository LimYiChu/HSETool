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
#edward 20211008

#from .filter import ActionItemsFilter - not sure might need this for later for upload excel. had to remove stuff in filter.py
#from .forms import UserRegisterForm
# Create your views here.
def readsqltable(request):
    studiesval = Studies.objects.values()
    dfstudiesval=pd.DataFrame(studiesval)
    print(dfstudiesval)
    actionitemsval = ActionItems.objects.values()
    dfactionitemsval = pd.DataFrame(actionitemsval)
    dfstudiesval['StudyName_id'] = dfstudiesval['id']
    print(dfstudiesval['StudyName_id'])
    
    
    return HttpResponse("TEST")
    
def uploadexceldf (request):
    
    if request.method == 'POST':
       
        form_upload = UploadExlForm(request.POST ,request.FILES)
        if form_upload.is_valid():
            
            
            form_upload.instance.Username = request.user.email
            form_upload.save()
            ID = form_upload.instance.id
            form_upload = UploadExlForm()
            obj = UploadExl.objects.get(id=ID)

            #edward 20211011
            #studies
            studiesval = Studies.objects.values()
            dfstudiesval=pd.DataFrame(studiesval) #2 columns to dict (id & studyname)

            dfstudies2cols = dfstudiesval[['id','StudyName']]
            dfstudiesindex = dfstudies2cols.set_index('id',inplace=True) #reindexing 
            dfstudiesdict = dfstudies2cols.to_dict()['StudyName']
            dfstudieswapkvp = dict((value, key) for key, value in dfstudiesdict.items()) #swapping kvp since we are using string as key & returning id as value pair

            #phases
            phasesval = Phases.objects.values()
            dfphasesval=pd.DataFrame(phasesval) #2 columns to dict (id & studyname)

            dfphases2cols = dfphasesval[['id','ProjectPhase']]
            dfphasesindex = dfphases2cols.set_index('id',inplace=True) #reindexing 
            dfphasesdict = dfphases2cols.to_dict()['ProjectPhase']
            dfphaseswapkvp = dict((value, key) for key, value in dfphasesdict.items()) #swapping kvp since we are using string as key & returning id as value pair

            data_df = pd.read_excel(obj.Filename.path,keep_default_na=False) #df conversion of studyname to studyname id should be done here

            data_df['StudyName_id']= data_df['StudyName_id'].map(dfstudieswapkvp)
            data_df['ProjectPhase_id']= data_df['ProjectPhase_id'].map(dfphaseswapkvp)

            dictdata = data_df.to_dict('records') # need to have records in there, converts df to kvp dic data in a queryset 
            
            #edward 20211011
            
            ActionItems.objects.bulk_create(
                                              [ActionItems(**vals) for vals in dictdata])

            messages.add_message(request, messages.SUCCESS, 'File Uploaded Successfully')

            #backup code dont delete
            # allfields = [field.name for field in ActionItems._meta.get_fields() 
            #                 if field.name != "id" and not field.get_internal_type() == "ForeignKey"]
                            
            #backup code dont delete
            # for x in dictdata:
            #     m = ActionItems(**x)

            #     m.save()
            #XX=[ActionItems(**vals) for vals in [dictdata]]
    else:
        form_upload= UploadExlForm()
    
    context = {
        'form_upload' : form_upload

    }
    
    return render(request, 'uploadexcel/upload.html', context)    

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

#changin to dataframes



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