from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
#from .forms import UploadExlForm
from .forms import *
import matplotlib as plt
from .models import *
import csv
#from .filter import ActionItemsFilter - not sure might need this for later for upload excel. had to remove stuff in filter.py
#from .forms import UserRegisterForm
# Create your views here.
@csrf_exempt

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

    return render(request, 'uploadExcel/upload.html', context)
    
def LoadRoutes (request):
    #to load routes from excel when required
    pass