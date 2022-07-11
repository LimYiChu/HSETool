#edward bulkpdf
from userT.businesslogic import *
from django.shortcuts import render
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    
    help = 'Creates bulk pdf in & stores them in a zip file' # run py manage.py -h for description of this function

    def handle(self, *args,**options):

        if os.path.isdir(bulkpdfdir):
            shutil.rmtree(bulkpdfdir)
        bulkpdfzipfoldername = tempfolder + ("bulkpdffiles" +".zip")
        objactionitems = ActionItems.objects.filter(QueSeries = 99).values() # to be altered when move to bl
        objactionitemsfk = blannotatefktomodel(objactionitems)
        # dfstudy = pd.DataFrame(objactionitemsfk)
        # dfstudyfilter = dfstudy.iloc[:,:2]
        # dfstudyfilter.to_csv(tempfolder+'bulkdownload.csv')
        returnzipfile = blbulkdownload(objactionitemsfk,bulkpdfdir,bulkpdfcreatezipfilename) #to remove bulkpdfmakebulkpdfdir
        # os.chmod(bulkpdfdir, 0o770)                 #770 is linux permission
        # shutil.chown(bulkpdfdir, 0, 1004)           # 0 is root in linux, 1004 is varwwwusers (user group)
        # blchangelinuxpermissions(bulkpdfdir, 0o770)     
        # blchangelinuxgroup(bulkpdfdir, 1000, 1004)
        
        return returnzipfile