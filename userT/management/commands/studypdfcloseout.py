#edward bulkpdf
from userT.businesslogic import *
from django.shortcuts import render
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    
    help = 'Creates bulk pdf by study & stores them in a zip file' # run py manage.py -h for description of this function


    def handle(self, *args,**options):

        studies = blgetAllStudies()
        if os.path.isdir(pdfbystudy):
            shutil.rmtree(pdfbystudy)
        for eachstudy in studies:
            StudyName = eachstudy.StudyName
            studypath = pdfbystudy+StudyName
            studyfolder = (studypath+"/")
            excelpath = studypath+'.csv'
            makesubfolders = os.makedirs(studypath,exist_ok=True)   
            studydetails = ActionItems.objects.filter(StudyName__StudyName = StudyName)
            studydetailsfilter = studydetails.filter(QueSeries = 99).values()
            objactionitemsfk = blannotatefktomodel(studydetailsfilter)
            dfstudy = pd.DataFrame(objactionitemsfk)
            dfstudyfilter = dfstudy.iloc[:,:2]
            dfstudyfilter.to_csv(excelpath)
            returnzipfile = blbulkdownload(objactionitemsfk,studyfolder,studypath)
        change_permissions_recursive(pdfbystudy, 0o770)     # 770 is linux permission
        change_group_recursive(pdfbystudy, 1000, 1004)      # 1000 is bitnami in linux, 1004 is varwwwusers (user group)

        return returnzipfile