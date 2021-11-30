#edward bulkpdf
from userT.businesslogic import *
from django.shortcuts import render
from django.core.management.base import BaseCommand
#20211123 edward pdf cleanup
from pdfgenerator import *

class Command(BaseCommand):
    
    help = 'Creates the stitched pdf closeout report' # run py manage.py -h for description of this function

    def handle(self, *args,**options): 
        
        objactionitems = ActionItems.objects.filter(QueSeries = 99).values() 
        objactionitemsfk = blannotatefktomodel(objactionitems)

        pdfpath = pdfcloseoutwithattachments(objactionitemsfk) 
        excel_list = os.listdir(pdfpath)
        pdf_list = os.listdir(pdfpath)
        
        #List Comprehensions searching for specific types of files in pdf_list
        pdf_list_onlypdf = [pdf for pdf in pdf_list if '.pdf' in pdf]
        pdf_list_onlyjpg = [jpg for jpg in pdf_list if '.jpg' in jpg]   
        pdf_list_onlyexcel = [excel for excel in excel_list if '.xlsx' in excel]
        
        exceltopdf = blexceltopdf(pdfpath,pdf_list_onlyexcel)

        imagetopdf = blimagetopdf(pdfpath,pdf_list_onlyjpg)

        pdfgeneratorstitch = stitchingpdf(pdf_list_onlypdf,pdfpath) #working 

        return pdfgeneratorstitch