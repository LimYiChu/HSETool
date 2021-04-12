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
        UploadExl.objects.all().delete()
       # ActionItems.objects.all().delete()
        form = UploadExlForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            form = UploadExlForm()
            obj = UploadExl.objects.get()
            
            with open (obj.filename.path, 'r') as input_file:
                csv_reader = csv.reader(input_file)
                for i, row in enumerate(csv_reader):
            
                    ActionItems.objects.create(
                    StudyActionNo= row [1],
                    StudyName= row[2],
                    Facility=row[3],
                    ProjectPhase=row[4],
                    Cause= row [5],
                    Consequence= row[6],
                    Recommendations= row[7],
                    Organisation=row[8],
                    Disipline=row[9],
                    Subdisipline=row[10],
                    FutureAction=row[11],
                    DueDate=row[12],
                    QueSeries=row[13],
                    
                    )
    else:
        form = UploadExlForm()
        print ("IN NOT VALID")
    return render(request, 'uploadExcel/upload.html', {'form':form})
    
def LoadRoutes (request):
    #to load routes from excel when required
    pass