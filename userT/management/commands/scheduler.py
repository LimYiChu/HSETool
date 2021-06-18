#edward scheduler
from userT.businesslogic import *
from django.shortcuts import render
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    help = 'sends weekly email' # run py manage.py -h for description of this function

    def handle(self, *args,**options): #sends reminder email for pending actions in basket 
        #sub = Subscribe()
        emaillist =[]
        #Get all Actions
        allactions = ActionItems.objects.all()
        #if (request.POST.get('SendPending')):
        QueOpen = [0,1,2,3,4,5,6,7,8,9]
        QueClosed = [99]
        discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
        Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)   
        subject = f"Pending Activities for {paremailphase} Risk Assessment Workshops"
        content=f"You have Pending Actions in your Queue. Please go to {paremailurl} to attend to the actions." 
        for items in Indisets : 
            if items[3]>0:
                emaillist.append(items[0])
        blemailSendindividual(emailSender,emaillist,subject,content)
        #below is for the overdue, it is linked to button, just waiting for overdue function
    # elif (request.POST.get('SendOverdue')):
          
    #     subject = f"Pending Activities for {paremailphase} Assessment Workshops"
    #     content=f"You have Overdue Actions in your Queue. Please go to {paremailurl} to attend to the actions." 
    #     blemailSendindividual(emailSender,emaillist,subject,content)

    #     return render (request, 'userT/emailreminders.html')
    # return render (request, 'userT/emailreminders.html')