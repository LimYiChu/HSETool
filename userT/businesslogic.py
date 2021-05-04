import django_filters
from django.http import HttpResponse

from UploadExcel.models import ActionItems
from .models import *

def blbuildRejectionemail(ID,RejectReason):
    Content=[]
    actionDetails = ActionItems.objects.filter(id=ID).values() # Since off the bat i did not pass any other information besides ID to rejection form i now have to information back for emails
    studyActionNo =  actionDetails[0].get('StudyActionNo')
    studyName = actionDetails[0].get('StudyName')
    response = actionDetails[0].get('Response')

    Content.append(studyActionNo + " from " + studyName + " has been rejected ") #This is subject
    Content.append("Rejection Reason : " + RejectReason + "...Response" + response) #this is the content of the email

    return Content
def blgetHistoryforUser(useremail, actioneeroutes):
    
    #first get user ID from CustomUser as only user id is used in history tables
    ApproverQue = [1,2,3,4,5,6,7,8,9]
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
    
def blgetbyStdudiesCount(Studies,OpenQue,YetToRespondQue,pendingApprovalQue,closedActionsQueSeries):
   
    lstcountbyStudies = []
    lstofstudiesdetails =[]
    for Study in Studies:
        lstcountbyStudies.append (Study.StudyName)
        lstcountbyStudies.append  (blallActionCountbyStudies(Study.StudyName,OpenQue))
        lstcountbyStudies.append (blallActionCountbyStudies(Study.StudyName,YetToRespondQue))
        lstcountbyStudies.append (blallActionCountbyStudies(Study.StudyName,pendingApprovalQue))
        lstcountbyStudies.append (blallActionCountbyStudies(Study.StudyName,closedActionsQueSeries))
        
        lstofstudiesdetails.append(lstcountbyStudies)
        lstcountbyStudies =[]
    
    return lstofstudiesdetails

def blgettimeStampforSignatories (id, Signatories):
        #pass in all Signatories and ID of action
        #return Signatories with Time Stamp
        
        #firstgetcurrentqueseries
        
        lstDictQueSeries = ActionItems.objects.filter(id=id).values('QueSeries')
        currentQueSeries = lstDictQueSeries[0].get('QueSeries')
        
        #next get all history that has got to do with ID from history tables
        #thinking that if you order by decending then you are done by getting latest first
        lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=currentQueSeries).order_by('-history_date').values()
        #print (lstdictHistory)
        #print (y[lstdictHistory].get('history_date'))
        finallstoflst = []                                   
        for index, items in enumerate(Signatories):
            if index < currentQueSeries:
                #get all time stamps for all que series
                #index basically denominates Que series level. if Current que series =2 then only actionee = 0 and Approver 1 has signed
                lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=index).order_by('-history_date').values()
                timestamp = lstdictHistory[0].get('history_date') # get just the first record assume decending is the way togo
                items.append(timestamp)
                finallstoflst.append(items)
                items =[]
            else:
                items.append(0)
                finallstoflst.append(items)
                items =[]
        
        #print (finallstoflst)
          #que series will decide number of people whom have signed +1 because actionee is 0- Need a matching list index

        return finallstoflst

def blgetDiscSubOrgfromID (ID):
    # just returns the company, disipline and sub from one object
    #had to place the org at the last because already done other functions to return  DiscSub as first 2 index and wanted to reuse them
    orgdiscsub= []
    obj=ActionItems.objects.get(id=ID)
    
    
    orgdiscsub.append(obj.Disipline)
    orgdiscsub.append(obj.Subdisipline)
    orgdiscsub.append(obj.Organisation)
    
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

def blsetApproverLevelTarget(ID,ApproverLevel):
    
    x= ActionItems.mdlSetField.mgrSetField(ID,"QueSeriesTarget",ApproverLevel)

def blgetFieldValue(ID,field):
    
    return ActionItems.mdlgetField.mgrGetField(ID,field)

def blgetApproverLevelTarget(ID,field):
    
    return ActionItems.mdlSetField.mgrgetField(ID,field)

def blgetIndiResponseCount(discsuborg,queseriesset,queseriesclosed):

    indiPendingSeries =[]
    completePendingPair = []

    #first loop through all routes disc/sub/org
    for itemtriplet in discsuborg:
        
        totalopencount = blgetDiscSubActionCount ('Y',itemtriplet,queseriesset)
        totalclosedcount = blgetDiscSubActionCount ('Y',itemtriplet,queseriesclosed)
        lstofActioneeApprover = blgetSignotories(itemtriplet)
        #indiPendingPair.append(itemtriplet)
        for indique,indipair in enumerate(lstofActioneeApprover):
            if (indipair != []):
                
                #indiPendingSeries.append(indique) #Append QueSeries
                lstindique = [indique] #make que series into list otherwise doesn work
                indiPendingSeries.append(indipair[1]) #append Name - 
                pendingResponse = blgetDiscSubActionCount ('Y',itemtriplet,lstindique)
                #for items in itemtriplet:
                #wanted to append and not have list of list of disc sub org
                indiPendingSeries.append(indipair[0]) #AppendRole
                indiPendingSeries.append(totalopencount)
                indiPendingSeries.append(pendingResponse)
                indiPendingSeries.append('/'.join(itemtriplet))
                indiPendingSeries.append(totalclosedcount)
                
                
            
            completePendingPair.append (indiPendingSeries)
            indiPendingSeries = []

    finallistoflist = [x for x in completePendingPair if x]    
    return finallistoflist

def blgetActionStuckAt(allactions, lstoftableattributes):

    lstActionDetails = []
    lstgettriplet = []
    lstofindiactions =[]

    for items in allactions:
        for x in lstoftableattributes:
            lstActionDetails.append(eval('items.'+str(x))) #gets the value by basically executing the content
       
        lstgettriplet = [items.Disipline,items.Subdisipline,items.Organisation]
        lstofActioneeAppr = blgetSignotories (lstgettriplet)

        
        if items.QueSeries != 99 : # basically its looks at que series and then matches it against the list of entire signatories above
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
    #print (finallistoflist)
    return finallistoflist
def blgetSignatoryemail(lstdiscsuborg):
    
    pairSignatories = blgetSignotories(lstdiscsuborg) #just reusing what is already done 

    for items in pairSignatories:
        items.pop(0)
    
    lstfinal = [''.join(ele) for ele in pairSignatories] #this is just list comprehensioin to return a list and not list of list
    return lstfinal 

def blgetActioneeDiscSub(routes):
    discsub=[]
    listoflist =[[]]
     
    for items in routes:
        discsub.append(items.Disipline)
        discsub.append(items.Subdisipline)
         
        listoflist.append(discsub)
        discsub=[]
        
    finallistoflist = [x for x in listoflist if x]

    return finallistoflist

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

def blActionCountbyStudies(contextRoutes,studies,que):

    firststream = 0
    secondstream = 0
    thirdstream = 0
    
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        blque               =   que
        if x==0:
            firststream = ActionItems.myActionItemsCount.mgr_myItemsCountbyStudies(studies,blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque)
        if x==1:
            secondstream = ActionItems.myActionItemsCount.mgr_myItemsCountbyStudies(studies,blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque)
        if x==2:
            thirdstream =  ActionItems.myActionItemsCount.mgr_myItemsCountbyStudies(studies,blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque)
    #return ActionItems.ActioneeItems.get_myItemsbyCompDisSub(blvarorganisation,blvardisipline,blvarSUbdisipline)
    return [ firststream,  secondstream,  thirdstream]

def blActionCountbyStudiesStream(contextRoutes,studies,que):

    streamscount = []
    streamdisc  = []
    finalstreams = []
    secondstream = 0
    thirdstream = 0
    
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        blque               =   que
       
        
        streamscount.append(ActionItems.myActionItemsCount.mgr_myItemsCountbyStudies(studies,blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque))
        streamdisc.append (blvardisipline)
    #finalstreams.append (streams)
    #return ActionItems.ActioneeItems.get_myItemsbyCompDisSub(blvarorganisation,blvardisipline,blvarSUbdisipline)
    return streamscount, streamdisc
def blallActionCountbyStudies(studies,quelist):

    count = 0
    
    for que in quelist:
        count += ActionItems.myActionItemsCount.mgr_allItemsCountbyStudies(studies,que) 
   
    return count
#def blgetActionsResponded 

def blfuncActionCount(contextRoutes,que):
   #This functionality already works
   #Initilises count in case 
    firststream = 0
    secondstream = 0
    thirdstream = 0
    
    for x, item in enumerate(contextRoutes):
        blvarorganisation   = item.Organisation
        blvardisipline  = item.Disipline
        blvarSUbdisipline  = item.Subdisipline
        blque               =   que
        if x==0:
            firststream = ActionItems.myActionItemsCount.get_myItemsCount(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque)
        if x==1:
            secondstream = ActionItems.myActionItemsCount.get_myItemsCount(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque)
        if x==2:
            thirdstream =  ActionItems.myActionItemsCount.get_myItemsCount(blvarorganisation,
                                                                blvardisipline,
                                                                blvarSUbdisipline,blque)
    #return ActionItems.ActioneeItems.get_myItemsbyCompDisSub(blvarorganisation,blvardisipline,blvarSUbdisipline)
    return [ firststream,  secondstream,  thirdstream]

def blfuncgetallAction(workshop,que):
    count = 0
    for eachQs in que:

        count += ActionItems.mdlallActionItemsCount.mgr_getallItemsCount('X',eachQs)

    return count

def blgetDiscSubActionCount(workshop,discsub,quelist):
    count = 0
    
    for eachQs in quelist:
        count += ActionItems.mdlgetActionDiscSubCount.mgr_getDiscSubItemsCount('X',discsub,eachQs) 
   
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