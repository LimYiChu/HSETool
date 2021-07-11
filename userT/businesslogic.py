import django_filters
from django.http import HttpResponse
import pandas as pd
from UploadExcel.models import ActionItems
from .models import *
from django.db.models import Count
from django.utils import timezone
import datetime
from django.core.mail import EmailMessage
import numpy as np
from dateutil.relativedelta import *
from userT.parameters import *
import re

def bladdriskcolourandoptiforflater (actionitems,removelist):
    
    dfRiskMatrix = pd.DataFrame(list(RiskMatrix.objects.all().values()))
            
    for items in actionitems:
                [items.pop(key) for key in removelist] # Reducing the data going to html
                #
                RiskColour = dfRiskMatrix.loc[dfRiskMatrix['Combined'].isin([items.get('InitialRisk')]),'RiskColour'].tolist() #cant use .item() as its causing an error when not matching
                
                if RiskColour:
                    items['RiskColour'] = RiskColour[0]
                else: 
                    items['RiskColour'] = False
    
    return actionitems

def bladdriskcolourandoptimise (actionitems,removelist):
    
    dfRiskMatrix = pd.DataFrame(list(RiskMatrix.objects.all().values()))
                
    for dictitems in actionitems:
        
        for items in dictitems:
                [items.pop(key) for key in removelist] # Reducing the data going to html
                #
                RiskColour = dfRiskMatrix.loc[dfRiskMatrix['Combined'].isin([items.get('InitialRisk')]),'RiskColour'].tolist() #cant use .item() as its causing an error when not matching
                
                if RiskColour:
                    items['RiskColour'] = RiskColour[0]
                else: 
                    items['RiskColour'] = False
    
    return actionitems

def blgroupbyaggsum(databody,dataheader,groupby,sumby):
    
    dfindisets = pd.DataFrame(databody,columns=dataheader)
    #create dictionary comprehension from below commented codes to gives readers ease of read
    # aggsum = {}
    # for items in sumby:
    #     aggsum.update({items:['sum']})
    
    aggsum = {el:['sum'] for el in sumby }# this is the defined format for frames 
   
    dfindisetssummary=dfindisets.groupby('User').agg(aggsum)
    dfindisetssummary.columns = sumby #ineeficient way but original adds 'sum' to header name
    listaggregatedindi = dfindisetssummary.reset_index().values.tolist() # cheating the system by just adding a sequential index at the start
    listaggregatedindiheader = dfindisetssummary.reset_index().columns.values.tolist()

    return listaggregatedindi,listaggregatedindiheader

def blgetfieldCustomUser(emailid,field):

    
    fieldval = CustomUser.mdlSetGetField.mgrGetField(emailid,field)
    strfieldval = fieldval[0].get(field)

    return strfieldval

def blsetfieldCustomUser(emailid,field,strvalue):
     CustomUser.mdlSetGetField.mgrSetField(emailid,field,strvalue)

def blgetRiskMatrixColour():
    dictRiskMatrix = RiskMatrix.objects.all().values()
    datadict =[]
    
    for details in dictRiskMatrix:
        keynames ={'Combined', 'RiskColour'}
        newdict = ({key:value for key,value in details.items() if key in keynames})
        datadict.append(newdict)
    
    return datadict
    

def blgetuserRoutes(useremail):
    ApproverLevel = 8
    userZemail = useremail
    Approver_Routes = {}

    #Actionee routes is straight forward
    Actionee_Routes   =   ActionRoutes.ActioneeRo.get_myroutes(userZemail)
    
    #Optimised to get all approver levels; readjust the key to 1 instead of 0
    for ApproverLevel in range(1 , ApproverLevel+1):
       Approver_Routes [ApproverLevel]  =  ActionRoutes.ApproverRo.get_myroutes(userZemail,ApproverLevel)
    #context just another form of return
    dictRoutes = {
       'Actionee_Routes' : Actionee_Routes,
       'Approver_Routes': Approver_Routes,
    }
    
    return dictRoutes #basically returning a dictionary object

def blemailSendindividual(sender,recipient, subject,content,ccl = cclist):

    subject = subject
    message = content
    cc = ccl
    Msg=EmailMessage(subject, message,sender, recipient,cc)
    Msg.content_subtype="html"
    
    Msg.send()
def blquerysetdicttolist(dict):
    finallist =[]
    for datetimepair in dict:
        newlist = list(datetimepair.values())

        finallist.append (newlist)

    return finallist

def blformulateRundown(lstplanned,lstactual):
    
    #took an arm and a leg to complete this logic - so needs some explnation
    plannedlistcount=[]
    lstnewplanned = []
    finallstplanned =[]
    for items in lstplanned :
        plannedlistcount.append(items[1])

    plannedtotalcount = sum(plannedlistcount) #Need to get Total count and then do the maths around it
    plannedcounter = 0
    actualcounter = plannedtotalcount #second attempt going to try terbalik style as its not an easy fix
    for items in lstplanned :

        lstnewplanned.append(str(items[0]))
        
        if plannedcounter==0: #this counter is required to do a rundown
            plannedcounter = plannedtotalcount - (items[1])
        else:
            plannedcounter = plannedcounter - (items[1])
        lstnewplanned.append (plannedcounter)
        
        blnsetwithdate = True
        for dates in lstactual :
      
             if (dates[0] == items[0]) :
           
                 actualcounter = actualcounter - (dates[1])
                 lstnewplanned.append (actualcounter)
                 finallstplanned.append(lstnewplanned)
                 lstnewplanned =[]
                 blnsetwithdate = False
                 break
        
        if blnsetwithdate  :
           #actualcounter = actualcounter 
            lstnewplanned.append (actualcounter)
            finallstplanned.append(lstnewplanned)
            lstnewplanned =[]
          
    return finallstplanned

def blgetActualRunDown(lstdatesandcount):
    
    
    closed = 99 #queseries
    countX = 0
    closeditems = ActionItems.objects.filter(QueSeries=closed)
    actualclosed =[]
    finalclosed =[]
    for items in closeditems:
        
        #check in history tables when it was closed
        dictactualhistory = ActionItems.history.filter(id=items.id).filter(QueSeries=closed).order_by('-history_date').values()
        #this is not supposed to be the case but for testing only it could be empty
        
        #make sure there is an entry in the history table, this is for testing
        if dictactualhistory: 
            datestamp = dictactualhistory[0].get('history_date')
            id = dictactualhistory[0].get('id')
            
            actualdate = datetime.datetime.date(datestamp)
            
            for dates in lstdatesandcount:

                if actualdate < dates[0] :
                    
                    countX = 1
                    actualclosed.append(dates[0])
                    actualclosed.append(countX)
                    finalclosed.append(actualclosed)
                    actualclosed =[]
                    break
    
    df = pd.DataFrame(finalclosed, columns=["duedate","tally"])
    dd = df.groupby(by=["duedate"]).count()
    dictdd = dd.to_dict()
 
    newactual=[]
    finalactual=[]
    for key,value in dictdd.items():
            
      
            for key in value:
                newactual.append(key)
                newactual.append(value[key])
                finalactual.append(newactual)
                newactual=[]
                
 
    return finalactual
def blaggregatebydate (objActions):

    thedates = objActions.values('DueDate').annotate(count=Count('id')).values('DueDate', 'count').order_by('DueDate')
    
    return thedates

def blprepareGoogleChartsfromDict(QuerySet):
    finallist=[]
    for dictitems in QuerySet:
        finallist.append(list(dictitems.values()))
    
    firstdatefiller = [finallist[0][0] - relativedelta(months=+1),0] #just inserts a date one month before and uses dateutil
    
    finallist.insert(0,firstdatefiller)

    return finallist
def blprepGoogChartsbyStudies (labels,count,newstudyname):

    studyname = "///" + newstudyname + ":::" # gotta do this since its passes all weird charaters to the jave script, with this i can then get the in between string in javascript
    initiallist =[]
    finallist =[]
    Startlist = ['By Studies',studyname ]
    for index , disc in  enumerate(labels):

        initiallist.append(disc)
        initiallist.append(count[index])

        finallist.append(initiallist)

        initiallist=[]
    
    finallist.insert(0,Startlist)

    return finallist

def blsetrejectionActionItems(ID,queseries):

    ActionItems.mdlQueSeries.mgrsetQueSeries(ID,queseries) 
    ActionItems.mdlQueSeries.mgrincrementRevision(ID)

def blbuildSubmittedemail(ID):
    urlview = f"/pmtrepviewall/{ID}/view"
    Content=[]
    actionDetails = ActionItems.objects.filter(id=ID).values() # Since off the bat i did not pass any other information besides ID to rejection form i now have to information back for emails
    studyActionNo =  actionDetails[0].get('StudyActionNo')
    studyName = actionDetails[0].get('StudyName')
    response = actionDetails[0].get('Response')

    Content.append(studyActionNo + " from " + studyName + " has been submitted ") #This is subject
    
    Content.append("To view this, please go to " + paremailurl +urlview + " . To approve go to your dashboard/approver que, to approve this and other actions")#+ "...Response" + response) #this is the content of the email #passed the url here in the content
    
    return Content
def blbuildRejectionemail(ID,RejectReason):
    urlview = f"/pmtrepviewall/{ID}/view"
    Content=[]
    actionDetails = ActionItems.objects.filter(id=ID).values() # Since off the bat i did not pass any other information besides ID to rejection form i now have to information back for emails
    studyActionNo =  actionDetails[0].get('StudyActionNo')
    studyName = actionDetails[0].get('StudyName')
    response = actionDetails[0].get('Response')

    Content.append(studyActionNo + " from " + studyName + " has been rejected ") #This is subject
    #edward add-on for rejection url
    Content.append("Rejection Reason : " + RejectReason + ". To attend to this, please go to " + paremailurl +urlview)#+ "...Response" + response) #this is the content of the email #passed the url here in the content
    
    return Content
def blgetHistoryforUser(useremail, actioneeroutes):
    
    #first get user ID from CustomUser as only user id is used in history tables
    ApproverQue = [1,2,3,4,5,6,7,8,9] #Once its closed its done is it so 99 is taken out
    lstUserSeries =  CustomUser.objects.filter(email=useremail).values()
    currentUserID = lstUserSeries[0].get('id')

    #get all history values from history tables first
   # userHistoric = ActionItems.history.filter(history_user_id=currentUserID).order_by('-history_date') #finally not using this
    actionsintheQue = blallActionsComDisSubbyList(actioneeroutes,ApproverQue)

    return actionsintheQue

def blgetApproverHistoryforUser(useremail, actioneeroutes):
    
    #first get user ID from CustomUser as only user id is used in history tables
    ApproverQue = [1,2,3,4,5,6,7,8,9,99]
    lstUserSeries =  CustomUser.objects.filter(email=useremail).values()
    currentUserID = lstUserSeries[0].get('id')

    #get all history values from history tables first
    userHistoric = ActionItems.history.filter(history_user_id=currentUserID).order_by('-history_date')
    actionsintheQue = blallActionsComDisSubbyList(actioneeroutes,ApproverQue)

    return actionsintheQue

def blallActionsComDisSubbyList(contextRoutes,quelist):
    
    streams = []

    
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline

        for que in quelist:
            streams.append (ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                               blvarSUbdisipline,que))
    
    return streams
def blgetrejectedcount(discsuborg,revision):

    lstrejectcountbydisc =[]
    lstfinallistcount = []
    for items in discsuborg:
        
        lstrejectcountbydisc.append("/".join(items))
        lstrejectcountbydisc.append(ActionItems.mdlgetActionDiscSubCount.
                                        mgr_getDiscSubOrgRejectedItemsCount(items,revision)) 
        
        
        lstfinallistcount.append(lstrejectcountbydisc)
        lstrejectcountbydisc = []

    return lstfinallistcount

def blaggregatebyDisc(discsuborg,  YetToRespondQue, ApprovalQue,QueClosed,QueOpen,TotalQue):
    lstofdiscdetails =[]
    lstcountbydisc =[]

    
    for disc in discsuborg:
        lstcountbydisc.append ("/".join(disc))
        lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,YetToRespondQue))
        lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,ApprovalQue))
        lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,QueClosed))
        lstcountbydisc.append  (blgetDiscSubOrgActionCount('X',disc,QueOpen))
        
        
        
        lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,TotalQue))
        
        # lstcountbydisc.append  (blallActionCountbyDisc(disc[0],QueOpen))
        # lstcountbydisc.append (blallActionCountbyDisc(disc[0],YetToRespondQue))
        # lstcountbydisc.append (blallActionCountbyDisc(disc[0],ApprovalQue))
        # lstcountbydisc.append (blallActionCountbyDisc(disc[0],QueClosed))
        # lstcountbydisc.append (blallActionCountbyDisc(disc[0],TotalQue))
        
        
        lstofdiscdetails.append(lstcountbydisc)
        lstcountbydisc =[]
    
   
    return lstofdiscdetails
def blallActionCountbyDisc(Disc,quelist):

    count = 0
    
    for que in quelist:
        count += ActionItems.myActionItemsCount.mgr_allItemsCountbyDisc(Disc,que) 
   
    return count
def blgetbyStdudiesCount(Studies,YetToRespondQue,pendingApprovalQue,closedActionsQueSeries,OpenQue,TotalQue):
   
    lstcountbyStudies = []
    lstofstudiesdetails =[]
    for Study in Studies:
        lstcountbyStudies.append (Study.StudyName)
        
        lstcountbyStudies.append (blallActionCountbyStudies(Study.StudyName,YetToRespondQue))
        lstcountbyStudies.append (blallActionCountbyStudies(Study.StudyName,pendingApprovalQue))
        lstcountbyStudies.append (blallActionCountbyStudies(Study.StudyName,closedActionsQueSeries))
        lstcountbyStudies.append  (blallActionCountbyStudies(Study.StudyName,OpenQue))
        lstcountbyStudies.append  (blallActionCountbyStudies(Study.StudyName,TotalQue))
        lstofstudiesdetails.append(lstcountbyStudies)
        lstcountbyStudies =[]
    
    return lstofstudiesdetails

#YHS copying for test
#def blallActionCountbyDisipline(disipline,quelist):

#    count = 0
    
#    for que in quelist:
#        count += ActionItems.myActionItemsCount.mgr_myItemsCountbyStudies(disipline,que) #Stuck here.
       
   
#    return count
   

#def blgetbyDispCount(discsuborg,OpenQue,YetToRespondQue,pendingApprovalQue,closedActionsQueSeries):
   
#    lstcountbydisciplines = []
#    lstofdisciplinesdetails =[]
#    for disipline in discsuborg:
#        lstcountbydisciplines.append (blgetIndiResponseCount(disipline.discount))
#        lstcountbydisciplines.append (blallActionCountbyDisipline(disipline.discount,OpenQue))
#        lstcountbydisciplines.append (blallActionCountbyDisipline(disipline.discount,YetToRespondQue))
#        lstcountbydisciplines.append (blallActionCountbyDisipline(disipline.discount,pendingApprovalQue))
#        lstcountbydisciplines.append (blallActionCountbyDisipline(disipline.discount,closedActionsQueSeries))
#        
#        lstofdisciplinesdetails.append(lstcountbydisciplines)
#        lstbydiscipline =[]
    
#    return lstbydiscipline

#end of test code
def blconverttodictforpdf(lstofsignatories):
    
    for items in lstofsignatories:
        fields = items[0]
        if ("actionee" in fields.lower()) :
            
            localtimeX = timezone.localtime(items[4])
           
            dict = {'actionee':items[0], 'actioneerole':items[3],'actioneename':items[2],
                    'actioneetimestamp':localtimeX
            }
        elif ("approver"in fields.lower()):

            localtimeX = timezone.localtime(items[4])

            strappr = str(items[0])
            strapprrole = strappr+"role"
            strapprname = strappr+"name"
            strapprtimestamp = strappr+"timestamp"


            dictapp = {strappr.lower():items[0], strapprrole.lower():items[3],strapprname.lower():items[2],
                    strapprtimestamp.lower():localtimeX}
            dict.update(dictapp)
            
    return(dict)

def blgetvaliduserinroute (idAI,emailid):
    
    discsuborg = blgetDiscSubOrgfromID(idAI)
    queseries = blgetFieldValue(idAI,'QueSeries')

    #starting to work with dictinary objects 
    # so the below just converts the signatories in your action ID route to check
    Signatories = dict(blgetSignotories(discsuborg))
    
    # the join is just to convert into string Approver1 or Approver2 or even actionee
    approverseries = ''.join([k for k, v in Signatories.items() if v==emailid])

    #must check queseries again to make sure queseries not at approver level
    #So this example below is if multiple actionee and then access id which is at approver level
    # 2 limb test must test for queseries because he could be an actionee and try and access url on approver que
    if  approverseries == 'Actionee' :
        if (queseries==0):
            isvaliduser = emailid in Signatories.values() # Triple quadruple checking even though above should have sufficed
            return isvaliduser
        else :
            return False
    #if not actionee Next is just to find the approvernumber(level) with re.findall creates a list, even with 1 element, just to make it into an integer
    approverlevel= ''.join(re.findall('[0-9]+', str(approverseries)))
    
    # 2 limb test

    isvaliduser = emailid in Signatories.values()
    if isvaliduser and (int(queseries)==int(approverlevel)):

        return True
    else :
        return False

def blgettimestampuserdetails (id, Signatories):
        #pass in all Signatories and ID of action
        #return Signatories with Time Stamp
        
        #firstgetcurrentqueseries
        
        lstDictQueSeries = ActionItems.objects.filter(id=id).values('QueSeries')
        currentQueSeries = lstDictQueSeries[0].get('QueSeries')
        
        #next get all history that has got to do with ID from history tables
        #thinking that if you order by decending then you are done by getting latest first
        lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=currentQueSeries).order_by('-history_date').values()
        
        finallstoflst = []                                   
        for index, items in enumerate(Signatories):
            
            #get each user detail first
            objuser = CustomUser.objects.filter(email=items[1]).values()
           
            if objuser:
                fullname =   objuser[0].get('fullname')
                items.append(fullname)
                designation =  objuser[0].get('designation')
                items.append(designation)

            else:
                    
                items.append("No User Defined")
            
            if index < currentQueSeries: 
                #get all time stamps for all que series
                #index basically denominates Que series level. if Current que series =2 then only actionee = 0 and Approver 1 has signed
                lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=index).order_by('-history_date').values()
                
                if lstdictHistory: #to fix testing bug
                    timestamp = lstdictHistory[0].get('history_date') # get just the first record assume decending is the way togo
                else:
                    timestamp = []

                items.append(timestamp)
                
                finallstoflst.append(items)
                
                items =[]
            
            else:
                #this simply says that i will give a time stamp for rest of levels to 0- no date and time
                
                items.append(0)
                finallstoflst.append(items)
                items =[]
        
    
          #que series will decide number of people whom have signed +1 because actionee is 0- Need a matching list index
        
        return finallstoflst

def blgetDiscSubOrgfromID (ID):
    # just returns the company, disipline and sub from one object
    #had to place the org at the last because already done other functions to return  DiscSub as first 2 index and wanted to reuse them
    orgdiscsub= []
    obj=ActionItems.objects.get(id=ID)
    
    
    orgdiscsub.append(obj.Disipline.rstrip().lstrip())
    orgdiscsub.append(obj.Subdisipline.rstrip().lstrip())
    orgdiscsub.append(obj.Organisation.rstrip().lstrip())
    
    return orgdiscsub

def blgetApproverLevel (lstorgdiscsub):
    #returns the approver level from routes, if 3 approvers it returns 4 meaning 4th is blank. 
    #basiclly looks up the route table and returns the next blank where field is approver
   
    obj= ActionRoutes.mdlgetApproverLevel.mgr_getApproverLevel (lstorgdiscsub)

    allfields = [f.name for f in ActionRoutes._meta.get_fields()] 
    del allfields[0:3] #- remove ID field, company and discpline - need to be carefull with this 
    
    blnOverride = False # sets the override to true when you hit the first Approver being none
    for fields in allfields:
        
        for x, items in enumerate(obj):
            param = 'items.'+ str(fields)
            
            if (eval(param) == None and ("Approver" in fields)and (blnOverride==False) ):
                blnOverride = True
                ApproverLevel = fields[-1]# only 9 Approvers allowed for now 
    
    return ApproverLevel
def blsetcloseouttemplate (ID):
    
    discsuborg = blgetDiscSubOrgfromID(ID)
    ApproverLevel = int(blgetApproverLevel(discsuborg)) -1# its not really a mistake as it was used now everywhere in que serires target
    
    
    #Particularly for SFSB in production and to get it to work of test
    #this needs to change and supposed to be based on some modular parameters 
    if ApproverLevel==5 or ApproverLevel == 7:
        newcloseouttemplate = f'{closeouttemplate}{ApproverLevel}{".pdf"}'
    else:
        newcloseouttemplate = f'{closeouttemplate}{".pdf"}'

    return newcloseouttemplate

def blsetApproverLevelTarget(ID,ApproverLevel):
    
    x= ActionItems.mdlSetField.mgrSetField(ID,"QueSeriesTarget",ApproverLevel)

def blgetFieldValue(ID,field):
    
    qs = ActionItems.mdlgetField.mgrGetField(ID,field)
    strintvalue = qs[0].get(field)
    
    return strintvalue
     

def blgetApproverLevelTarget(ID,field):
    
    return ActionItems.mdlSetField.mgrgetField(ID,field)

def blgetIndiResponseCount(discsuborg,queseriesopen,queseriesclosed):

    indiPendingSeries =[]
    completePendingPair = []

    #first loop through all routes disc/sub/org
    for itemtriplet in discsuborg:
        
        totalopencount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesopen) # changed by edward to queseriesopen shows how many action open in each routes
        totalclosedcount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesclosed)
        lstofActioneeApprover = blgetSignotories(itemtriplet)
        #indiPendingPair.append(itemtriplet)
        for indique,indipair in enumerate(lstofActioneeApprover):
            if (indipair != []):
                
                #indiPendingSeries.append(indique) #Append QueSeries
                lstindique = [indique] #make que series into list otherwise doesn work, indique is 0 for Actionee-start of loop                
                indiPendingSeries.append(indipair[1]) #append Name - #indipair gives all users in routes print indipair,indipendingseries
                pendingResponse = blgetDiscSubOrgActionCount ('Y',itemtriplet,lstindique) #print itemtriplet comes to triplet looks for 0 then goes to lstindique and maps to name->lstindique is all the users 0-9 in routes   
                #for items in itemtriplet:
                #wanted to append and not have list of list of disc sub org
                indiPendingSeries.append(indipair[0]) #AppendRole
                indiPendingSeries.append('/'.join(itemtriplet))
                indiPendingSeries.append(pendingResponse)
                
                indiPendingSeries.append(totalclosedcount)
                indiPendingSeries.append(totalopencount) # Removing opencount since its misleading
                
            
            completePendingPair.append (indiPendingSeries)
            indiPendingSeries = []

    finallistoflist = [x for x in completePendingPair if x]    
    return finallistoflist
def blgetIndiResponseCount2(discsuborg,queseriesopen,queseriesclosed):

    indiPendingSeries =[]
    completePendingPair = []
    filler = 0
    #first loop through all routes disc/sub/org
    for itemtriplet in discsuborg:
        
        totalopencount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesopen) 
        totalclosedcount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesclosed)
        lstofActioneeApprover = blgetSignotories(itemtriplet)

       
        #indiPendingPair.append(itemtriplet)
        for indique,indipair in enumerate(lstofActioneeApprover):
            if (indipair != []):
                
                #indiPendingSeries.append(indique) #Append QueSeries
                lstindique = [indique] #make que series into list otherwise doesn work, indique is 0 for Actionee-start of loop                
                indiPendingSeries.append(indipair[1]) #append Name - #indipair gives all users in routes print indipair,indipendingseries
                pendingResponse = blgetDiscSubOrgActionCount ('Y',itemtriplet,lstindique) #just uses queseries and maps back to the 
                #for items in itemtriplet:
                #wanted to append and not have list of list of disc sub org
                indiPendingSeries.append(indipair[0]) #AppendRole
                indiPendingSeries.append('/'.join(itemtriplet))
                if indique == 0:
                    indiPendingSeries.append(pendingResponse)
                    indiPendingSeries.append(filler)
                else:
                    indiPendingSeries.append(filler)
                    indiPendingSeries.append(pendingResponse)
                    
                indiPendingSeries.append(totalclosedcount)
                indiPendingSeries.append(totalopencount) # Removing opencount since its misleading
                
            
            completePendingPair.append (indiPendingSeries)
            print (indiPendingSeries)
            indiPendingSeries = []

    finallistoflist = [x for x in completePendingPair if x]    
    return finallistoflist
def blgetActionStuckAt(allactions, lstoftableattributes,email=False):

    lstActionDetails = []
    lstgettriplet = []
    lstofindiactions =[]

    for items in allactions:
        for x in lstoftableattributes:
            lstActionDetails.append(eval('items.'+str(x))) #gets the value by basically executing the string content, just dynamic content stuff
       
        #the disc sub and company are not case sensitive but space sensitive, remove leading and end white spaces
        #bug fixes for version 1.8
        strdiscipline = items.Disipline.rstrip().lstrip()
        strsubdiscipline = items.Subdisipline.rstrip().lstrip()
        strorganisation = items.Organisation.rstrip().lstrip()
        #end bug fix - should move this into signatories
        lstgettriplet = [strdiscipline,strsubdiscipline,strorganisation]
        lstofActioneeAppr = blgetSignotories (lstgettriplet)

        
        if items.QueSeries != 99 and (lstofActioneeAppr !=[]): # basically its looks at que series and then matches it against the list of entire signatories above
            lststuckAt = lstofActioneeAppr[items.QueSeries]#basically just uses QueSeries to tell us where its stuck at
            
            
            lstActionDetails.append("/".join(lststuckAt)) # Because there is 2 parts to the formula = Actionee , gunav -- So im Just joining them into string
        else:
            lstActionDetails.append ("Closed") # if its 99 just have a tag closed
           
        lstofindiactions.append (lstActionDetails)
        lstActionDetails =[]

    return lstofindiactions

def blgetSignotories (lstorgdiscsub):
    #in - list of company disc sub
    # - out Actionee & Approver approver names - basically the signatories
    
    #need to strip white spaces in case its passed
    stripedDisc = lstorgdiscsub[0].rstrip().lstrip()
    stripedSub = lstorgdiscsub[1].rstrip().lstrip()
    stripedOrg = lstorgdiscsub[2].rstrip().lstrip()
    
    stripedDiscSubOrg = [stripedDisc,stripedSub,stripedOrg]
    obj= ActionRoutes.mdlgetApproverLevel.mgr_getApproverLevel (lstorgdiscsub)
        
    allfields = [f.name for f in ActionRoutes._meta.get_fields()] 
    del allfields[0:3] #- remove ID field, company and discpline , can remove others- need to be carefull with this 
    
    
    blnOverride = False # sets the override to true when you hit the first Approver being none
    SigPair = []
    finalSigPair =[]
    for fields in allfields:
        
        for x, items in enumerate(obj): #getattr doesnt work so just iterate the object again - not effiecient but not too bad
            
            
            if (("Approver" in fields)or ("Actionee" in fields) ):
                
                param = 'items.'+ str(fields)
                fieldValue = eval(param)
                if ( fieldValue != None): 
                    SigPair.append(fields)
                    SigPair.append (fieldValue)

                finalSigPair.append (SigPair)# only 9 Approvers allowed for now

                SigPair =[] 

    finallistoflist = [x for x in finalSigPair if x]
    
    return finallistoflist
def blgetSignatoryemailbyque(lstdiscsuborg,queseries):
    
    pairSignatories = blgetSignotories(lstdiscsuborg) #just reusing what is already done 

    for items in pairSignatories:
        items.pop(0) # basically removes the Actionee, Approver from pair and maintains name
        
    
    abbrevatedemail=pairSignatories[:queseries] # returns only before queseries

    lstfinal = [''.join(ele) for ele in abbrevatedemail] #this is just list comprehensioin to return a list and not list of list
    
    
    return lstfinal 


def blgetActioneeDiscSub(routes):
    discsub=[]
    listoflist =[[]]
     
    for items in routes:
        discsub.append(items.Disipline.rstrip().lstrip())
        discsub.append(items.Subdisipline.rstrip().lstrip())
         
        listoflist.append(discsub)
        discsub=[]
        
    finallistoflist = [x for x in listoflist if x]

    return finallistoflist

def blRejectedHistortyActionsbyId (useremail,queseriesat, Revision):
    
    #get user from email id since history tables use user ID
    lstUserSeries =  CustomUser.objects.filter(email=useremail).values()
    currentUserID = lstUserSeries[0].get('id')

    #get all history values from history tables first
    userrejectedhistory = ActionItems.history.filter(history_user_id=currentUserID).filter(
                            
                                Revision__gte=Revision).filter(QueSeries=queseriesat).order_by('-history_date').values('id')
    
           
    return userrejectedhistory
def blgetActionItemsbyid(dictofids):

    #Convert list of dictionaries into list
    listofids =[x['id']for x in dictofids]
    
    
    actionitemsbyid = ActionItems.objects.filter(id__in=dictofids).values()

    return actionitemsbyid

def blApproverHistoryActions(contextRoutes,que):
    streams = []

    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarsubbdisipline  = item.Subdisipline


        approverlevel=int(blgetApproverLevel([blvardisipline,blvarsubbdisipline,blvarorganisation])) #normally gives you one extra
        #This is different slice added 1 since items are past that approver meaning Queseries +1 but in that route
        for queseries in range (que+1,approverlevel):

            streams.append (ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                               blvarsubbdisipline,queseries))
    
    
    return streams
def blallActionsComDisSub(contextRoutes,que):
    
    streams = []

    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline

        streams.append (ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                               blvarSUbdisipline,que))
    
    
    return streams

def blfuncActioneeComDisSub(contextRoutes,que):
   #This functionality already works 
    firststream = []
    secondstream = []
    thirdstream = []
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        if x==0:
            firststream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
        if x==1:
            secondstream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
        if x==2:
            thirdstream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
    #return ActionItems.ActioneeItems.get_myItemsbyCompDisSub(blvarorganisation,blvardisipline,blvarSUbdisipline)
    return firststream, secondstream, thirdstream
    #(Organisation__icontains=blvarorganisation).filter(Disipline__icontains=blvardisipline).filter(Subdisipline__icontains=blvarSUbdisipline)
def blActioneeComDisSubManyStr(contextRoutes,que):
   #This functionality already works 
    streams = []
    secondstream = []
    thirdstream = []
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        if x==0:
            firststream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
        if x==1:
            secondstream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
        if x==2:
            thirdstream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
    #return ActionItems.ActioneeItems.get_myItemsbyCompDisSub(blvarorganisation,blvardisipline,blvarSUbdisipline)
    return firststream, secondstream, thirdstream
    #(Organisation__icontains=blvarorganisation).filter(Disipline__icontains=blvardisipline).filter(Subdisipline__icontains=blvarSUbdisipline)



def blActionCountbyStudiesStream(contextRoutes,studies,que):

    streamscount = []
    streamdisc  = []
    
    
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        blque               =   que
       
        
        streamscount.append(ActionItems.myActionItemsCount.mgr_myItemsCountbyStudies(studies,blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque))
        streamdisc.append (blvardisipline)
    
    return streamscount, streamdisc
def blallActionCountbyStudies(studies,quelist):

    count = 0
    
    for que in quelist:
        count += ActionItems.myActionItemsCount.mgr_allItemsCountbyStudies(studies,que) 
   
    return count
#def blgetActionsResponded 

def blfuncActionCount(contextRoutes,que):
   #just pass your routes it counts everything in your routes
    
    allstreams = []
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        blque               =   que
        
        allstreams.append(ActionItems.myActionItemsCount.get_myItemsCount(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque))

    return allstreams

def blfuncgetallAction(workshop,que):
    count = 0
    for eachQs in que:

        count += ActionItems.mdlallActionItemsCount.mgr_getallItemsCount('X',eachQs)

    return count
def blgetDiscSubActionCount(workshop,discsuborg,quelist):
    count = 0
    
    for eachQs in quelist:
        count += ActionItems.mdlgetActionDiscSubCount.mgr_getDiscSubItemsCount('X',discsuborg,eachQs) 
   
    return count
def blgetDiscSubOrgActionCount(workshop,discsuborg,quelist):
    count = 0
    
    for eachQs in quelist: #eachqs is 0 to 9
        count += ActionItems.mdlgetActionDiscSubCount.mgr_getDiscSubOrgItemsCount('X',discsuborg,eachQs) 
   
    return count
   
def blgetCompanyActionCount(company,quelist) :

    count = 0

    for eachQs in quelist:
        count += ActionItems.mdlgetActionCompanyCount.mgr_getCompanyCount(company,eachQs) 
   
    return count
def blgetActioneeItemsbyStream(contextRoutes,stream): 
    que = 0 #denotes actionee items
    firststream = []
    secondstream = []
    thirdstream = []
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        if x==stream:
            firststream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
            return firststream
        if x==stream:
            secondstream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
            return secondstream
        if x==stream:
            thirdstream = ActionItems.myActionItems.get_myItemsbyCompDisSub(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,que)
            return thirdstream

def blgetAllStudies ():

    return Studies.objects.all()

def stripAndmatch(lstcount,lstlabel):
    
    # extends the list if the actionee routes are only1 (anything less than 3)
    #needs a buffer of 3 to get it right 
    #lstlabels.extend([0] * (3 - len(lstlabels)))
   
    indextoremove =[]
    #newlabels = lstlabels
    newlstcount = lstcount
    for index, X in enumerate(lstcount):
       
        if X == 0:
            indextoremove.append(index)
    
    for index in sorted(indextoremove, reverse=True):
        del newlstcount[index]
        del lstlabel[index]
            
    
    return newlstcount,lstlabel

