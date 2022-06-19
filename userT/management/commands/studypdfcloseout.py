#edward bulkpdf
from userT.businesslogic import *
from django.shortcuts import render
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    
    help = 'Creates bulk pdf by study & stores them in a zip file' # run py manage.py -h for description of this function


    def handle(self, *args,**options):

        studies = blgetAllStudies()
        shutil.rmtree(pdfbystudy)
        for eachstudy in studies:
            StudyName = eachstudy.StudyName
            makesubfolders = os.makedirs(pdfbystudy+f'{StudyName}',exist_ok=True) 
            studydetails = ActionItems.objects.filter(StudyName__StudyName = StudyName)
            studydetailsfilter = studydetails.filter(QueSeries = 99).values()
            objactionitemsfk = blannotatefktomodel(studydetailsfilter)
            dfstudy = pd.DataFrame(objactionitemsfk)
            dfstudyfilter = dfstudy.iloc[:,:2]
            dfstudyfilter.to_csv(pdfbystudy+f'{StudyName}'+'.csv')
            studyfolder = (pdfbystudy+f'{StudyName}'+"/")
            zipname = pdfbystudy+f'{StudyName}'
            returnzipfile = blbulkdownload(objactionitemsfk,studyfolder,zipname)
        return returnzipfile