from .businesslogicQ import *
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
from datetime import date
#edward 20210722 added datetime
import datetime 
from datetime import date as dt 
from operator import itemgetter, or_
#edward 20210817 added pandas
import pandas as pd
# edward 20210915 bulk download
from userT.pdfgenerator import *
import shutil
# edward 20210929 fk
from django.db.models import F

def bladdfktodict(data_dict,foreignkeys):
    # actiondetails = ActionItems.objects.get(id=ID)
    # studyname = str(actiondetails.StudyName)
    # projectphase = str(actiondetails.ProjectPhase)
    # foreignkeys = {}
    # for field in ActionItems._meta.fields:
    #     if field.get_internal_type() == 'ForeignKey':
    #         fieldname = field.name
            
    #         x = {field.name : eval(f"{fieldname}")}
            
    #         foreignkeys.update(x)
    data_dict.update(foreignkeys) # updating original with study & phase 

    return data_dict
# edward 20210915 bulk download 


def blremoveemptylist (listoflist):
    '''
    pass in list of list and returns list with no empty list
    '''
    listfinal = [ele for ele in listoflist if ele != []]

    return listfinal
def blannotatefktomodel(actionvalues):
    """
    Edward
    pass queryset dictionary values() from ActionItems Table only and then Annotates (adds) the foriegn key 
    StudyName and Project Phase to the Model
    """
    allactionsannotated =  actionvalues.annotate(StudyName=F(
                            'StudyName__StudyName')).annotate(ProjectPhase = F('ProjectPhase__ProjectPhase'))
    
    return allactionsannotated

def blmakelistforjson (data,featurenames):
    data3=[]
    for items in data:
        
        
        data2= [dict(zip(featurenames,pies)) for pies in items]
        data3.append(data2)
        data2 =[]
        
    return data3
    


# edward 20210915 bulk download 
def blmakedir(makedstdir):
    """
    Creates a directory even if that directory already exists

    """
    createddir = os.makedirs(makedstdir,exist_ok=True)
    return createddir

# def blfkattachment(ObjAttach,attachments):

#     for eachfile in ObjAttach: 
#         filename = os.path.basename(eachfile.Attachment.name)
#         attachmentorigin = attachments + filename

#         return attachmentorigin
#this function needs to be fixed
def blbulkdownload(objactionitems,destinationfolders,createzipfilename): # changedstfolder destinationfolder
    # os.makedirs(makedstdir,exist_ok=True)
    # dir = 'static/media/temp/bulkpdf/'
    # shutil.rmtree(dir)
    
    for items in objactionitems: #objactionitems
        # closed = (items['QueSeries'] == 99)
        closed = True
        if closed == True :
            items['StudyActionNo'] = items['StudyActionNo'].replace("/","_")
            newcloseouttemplate = blsetcloseouttemplate (items['id'])
            data_dict=items
            discsub = blgetDiscSubOrgfromID(items['id']) 
            Signatories = blgetSignotories(discsub) 
            lstSignatoriesTimeStamp= blgettimestampuserdetails (items['id'], Signatories) 
            studyactno = items["StudyActionNo"] # i renamed to studyactno
            studyactnopdf = (studyactno + '.pdf')
            signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp)
            makesubfolders = os.makedirs(destinationfolders + studyactno, exist_ok=True ) # renamed i to studyactno
            destination =destinationfolders + studyactno #dst to destination
            out_file = os.path.join(destination,studyactnopdf)
            #20210923 edward fk study phase
            #updateddata_dict = blannotatefktomodel(data_dict)
            file = pdfgenerate(newcloseouttemplate,out_file,data_dict,signatoriesdict)
            #20210923 edward fk study phase
            objFk =ActionItems.objects.get(id = items['id']) 
            ObjAttach = objFk.attachments_set.all()

            for eachfile in ObjAttach: 
                filename = os.path.basename(eachfile.Attachment.path) # changed from .name to .path
                attachmentorigin= bulkdlattachments + filename

                shutil.copy(attachmentorigin, destination) #copying all done inside for loop for each attachment

    returnzipfile = shutil.make_archive(createzipfilename, 'zip', destinationfolders)

    return returnzipfile

#edward 20210817 excel format
def blexcelformat (dfallsorted,workbook,worksheet):
    
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#D3D3D3',
        'border': 1})
    header_format.set_bottom(6)
    for col_num, value in enumerate(dfallsorted.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)
    worksheet.set_column('B:V', 20)
    #worksheet.set_row(0,25) 
    worksheet.set_default_row(25)

    return worksheet

#edward 20210803 excel column formatting using dataframes
def blsortdataframes(dfall,sortedheader) : #use list for sortedheader, just place what you want in order in parameters.py
    sortedfall = dfall.reindex(columns=sortedheader) #sorting the columns based on specified sortedheader list if you want alphabetically just use df.sort_index(axis=1)
    return sortedfall


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

def bladdriskcolourandoptimise (actionitems,removelist=[]):
    ''' Accepts dictionary only items and then extracts InitialRisk using dataframes,
    then looks up RiskMatrix Model and gets a risk colour. It uses the Combined value in the RiskMatrix to map back to the Risk COlour
    the second parameter is optional seprate funtinality for removing addtional fields. Next revision this should be separated '''
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

def blgetRiskMatrixAvailable():
    
    if (RiskMatrix.objects.all()):
        availability = True
    else:
        availability = False
    
    print(availability)
    return availability

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
#edward 20211021 passing in actions 
def blgetActualRunDown(lstdatesandcount,closeditems): 
    
    #lstdatesandcount is passing in due dates and how many were meant to be closed

    
    closed = 99 #queseries
    countX = 0
    #closeditems = ActionItems.objects.filter(QueSeries=closed) #20211021 edward to be removed after one week from now 
    #closeditems = actions.filter(QueSeries=closed)#change in views #20211021 edward to be removed after one week from now 

    actualclosed =[]
    finalclosed =[]
    for items in closeditems:
        
        #check in history tables when it was closed
        dictactualhistory = ActionItems.history.filter(id=items["id"]).filter(QueSeries=closed).order_by('-history_date').values()
        #this is not supposed to be the case but for testing only it could be empty
        
        # make sure there is an entry in the history table, this is for testing
        # data going into js datatable has to be in a certain format & could not go as an empty entry 
        # items closed taken from history table & mapped to less than equals dates
        if dictactualhistory: 
            datestamp = dictactualhistory[0].get('history_date')
            id = dictactualhistory[0].get('id')
            
            actualdate = datetime.datetime.date(datestamp) #taking the date as a date object
            
            for dates in lstdatesandcount:

                if actualdate <= dates[0] : 
                    
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
    
    #History is always in the past so today is the latest day
    # Inject Today
    #finalactual
    return finalactual
#aggregates the duedate by counting each action item
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

def blbuildSubmittedemail(ID,ActioneeApproverReject, RejectReason=""):
    '''Pass in id of actions, and string of where its coming from i.e "Actionne", "Approver", "Reject" that have been submitted or approved and rejected and it returns list [Subject, Content]
    Optional Parameter of reject reason can be passed in to state reason in content'''

    urlview = f"/pmtrepviewall/{ID}/view"
    urlviewApprover = "/ApproverList/" # Not used yet thinking of redoing url below for simplification
    urlviewRejection = "/ActioneeList/"
    Content=[]

    #Changing the waythis is done since retreiving single  object plus doesnt work with filter and values ori code below with 
    # Foreign Key"
    actionDetails = ActionItems.objects.get(id=ID)
    studyActionNo = actionDetails.StudyActionNo
    studyName = str(actionDetails.StudyName)
    response = actionDetails.Response
    
    dictofsubjectcontent ={
        'ActioneeSubject' : studyActionNo + " from " + studyName + " has been submitted ",
        'ApproverSubject' : studyActionNo + " from " + studyName + " has been approved ",
        'RejectSubject' : studyActionNo + " from " + studyName + " has been rejected ",
        'ActioneeContent' : "To view this, please go to " + paremailurl +urlview + " . To approve go to your dashboard/approver que, to approve this and other actions",
        'ApproverContent' : "To view this, please go to " + paremailurl +urlview + " . To approve go to your dashboard/approver que, to approve this and other actions",
        'RejectContent' : "Rejection Reason : " + RejectReason + ". To attend to this go to your dashboard, view of rejection is available at " + paremailurl +urlview,
    }

    #as pythonic as it gets
    Content = [ v for k,v in dictofsubjectcontent.items() if k.startswith(ActioneeApproverReject)]
  
   
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
    '''Agregates by discpline across organisation. Takes in various QueSeries denoting Yettorespond, Approval 
    Open Actions, Total Queue'''
    
    lstofdiscdetails =[]
    lstcountbydisc =[]
    for disc in discsuborg:
        lstcountbydisc.append ("/".join(disc))
        # lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,YetToRespondQue))
        # lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,ApprovalQue))
        # lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,QueClosed))
        # lstcountbydisc.append  (blgetDiscSubOrgActionCount('X',disc,QueOpen))
        # lstcountbydisc.append (blgetDiscSubOrgActionCount('X',disc,TotalQue))
        
        #Rewritten with QObject for optimisation
        lstcountbydisc.append (blphasegetDiscSubOrgActionCountQ(disc,YetToRespondQue))
        lstcountbydisc.append (blphasegetDiscSubOrgActionCountQ(disc,ApprovalQue))
        lstcountbydisc.append (blphasegetDiscSubOrgActionCountQ(disc,QueClosed))
        lstcountbydisc.append  (blphasegetDiscSubOrgActionCountQ(disc,QueOpen))
        lstcountbydisc.append (blphasegetDiscSubOrgActionCountQ(disc,TotalQue))
      
        
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

        studynameQ = Study.StudyName
        lstcountbyStudies.append (studynameQ)
        
        # lstcountbyStudies.append (blallActionCountbyStudies(studynameQ,YetToRespondQue))
        # lstcountbyStudies.append (blallActionCountbyStudies(studynameQ,pendingApprovalQue))
        # lstcountbyStudies.append (blallActionCountbyStudies(studynameQ,closedActionsQueSeries))
        # lstcountbyStudies.append  (blallActionCountbyStudies(studynameQ,OpenQue))
        # lstcountbyStudies.append  (blallActionCountbyStudies(studynameQ,TotalQue))

        #Convert to QObject
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,YetToRespondQue))
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,pendingApprovalQue))
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,closedActionsQueSeries))
        lstcountbyStudies.append  (blallActionCountbyStudiesPhaseQ(studynameQ,OpenQue))
        lstcountbyStudies.append  (blallActionCountbyStudiesPhaseQ(studynameQ,TotalQue))

        lstofstudiesdetails.append(lstcountbyStudies)
        lstcountbyStudies =[]
    
    return lstofstudiesdetails

def blconverttodictforpdf(lstofsignatories): #edward altered this instead of creating new bl because it is only used for closedoutsheet 20210706
    
    for items in lstofsignatories:
        print(items)
        # print(items[5])
        # print(timezone.localtime())
        # if items[5] is None : 
        #     print('TEST')
        time = items[5] 
        if time == []    :
                
            localtimeX = timezone.localtime() #edward changed this according to new bl function for signatures 20210706    
            fields = items[0]
            #print(fields)
            if ("actionee" in fields.lower()) :
                #print(items[5])
                #localtimeX = timezone.localtime(items[5]) #edward changed this according to new bl function for signatures 20210706
                #edward changed this to add actioneesignature according to new bl function for signatures 20210706
                dict = {'actionee':items[0], 'actioneerole':items[3],'actioneename':items[2],'actioneesignature':items[4],
                        'actioneetimestamp':localtimeX
                }
                
            elif ("approver"in fields.lower()):
                
                
        
                strappr = str(items[0])
                strapprrole = strappr+"role"
                strapprname = strappr+"name"
                strapprsignature = strappr+"signature" #edward added strapprsignature according to new bl function for signatures 20210706
                strapprtimestamp = strappr+"timestamp"

                #edward added strapprsignature according to new bl function for signatures 20210706
                dictapp = {strappr.lower():items[0], strapprrole.lower():items[3],strapprname.lower():items[2],strapprsignature.lower():items[4],
                        strapprtimestamp.lower():localtimeX}
                dict.update(dictapp)
        else:
                
            localtimeX = timezone.localtime(time) #edward changed this according to new bl function for signatures 20210706    
            fields = items[0]
            #print(fields)
            if ("actionee" in fields.lower()) :
                #print(items[5])
                #localtimeX = timezone.localtime(items[5]) #edward changed this according to new bl function for signatures 20210706
                #edward changed this to add actioneesignature according to new bl function for signatures 20210706
                dict = {'actionee':items[0], 'actioneerole':items[3],'actioneename':items[2],'actioneesignature':items[4],
                        'actioneetimestamp':localtimeX
                }
                
            elif ("approver"in fields.lower()):
                
                
        
                strappr = str(items[0])
                strapprrole = strappr+"role"
                strapprname = strappr+"name"
                strapprsignature = strappr+"signature" #edward added strapprsignature according to new bl function for signatures 20210706
                strapprtimestamp = strappr+"timestamp"

                #edward added strapprsignature according to new bl function for signatures 20210706
                dictapp = {strappr.lower():items[0], strapprrole.lower():items[3],strapprname.lower():items[2],strapprsignature.lower():items[4],
                        strapprtimestamp.lower():localtimeX}
                dict.update(dictapp)
            
    return(dict)

def blgetvaliduserinroute (idAI,emailid,History=False):
    
    discsuborg = blgetDiscSubOrgfromID(idAI)
    queseries = blgetFieldValue(idAI,'QueSeries')

    #starting to work with dictinary objects 
    # so the below just converts the signatories in your action ID route to check
    Signatories = dict(blgetSignotories(discsuborg))
    
    # the join is just to convert into string Actionee Approver1 or Approver2
    # But just supposed to get 1 value, actionee or approver or...
    # Need to modify for testing as sometimes we want to have 
    approveractioneeseries = ''.join([k for k, v in Signatories.items() if v==emailid])
    approverlevel= ''.join(re.findall('[0-9]+', str(approveractioneeseries)))
    
    isvaliduser = emailid in Signatories.values()
    
    #must check queseries again to make sure queseries not at approver level
    #So this example below is if multiple actionee and then access id which is at approver level
    # 2 limb test must test for queseries because he could be an actionee and try and access url on approver que
    #This if statements below is to cater for testing as well where you might have been assigned to actionee and approver in one route
    #first test if you are actionee
    if  'Actionee' in approveractioneeseries :
        if (queseries==0) or History==True:
            isvaliduser = emailid in Signatories.values() # Triple quadruple checking even though above should have sufficed
            return isvaliduser
        #next need to check if approver in that mixed que for same route mostly while development
        
        elif ('Approver' in approveractioneeseries) and (str(queseries) in approverlevel):
            
            return True
        else:
            return False
    elif ('Approver' in approveractioneeseries) :
        
        if (str(queseries) in approverlevel) or History==True:
    
    # 2 limb test

        #if isvaliduser and (str(queseries)==int(approverlevel)):

            return True
    else :
        
        return False
#obsolete code commented by edward on 20210707 after adding signature field & creating new bl function, to be deleted in one month
# def blgettimestampuserdetails (id, Signatories): 
#         #pass in all Signatories and ID of action
#         #return Signatories with Time Stamp
        
#         #firstgetcurrentqueseries
        
#         lstDictQueSeries = ActionItems.objects.filter(id=id).values('QueSeries')
#         currentQueSeries = lstDictQueSeries[0].get('QueSeries')
        
#         #next get all history that has got to do with ID from history tables
#         #thinking that if you order by decending then you are done by getting latest first
#         lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=currentQueSeries).order_by('-history_date').values()
        
#         finallstoflst = []                                   
#         for index, items in enumerate(Signatories):
            
#             #get each user detail first
#             objuser = CustomUser.objects.filter(email=items[1]).values()
           
#             if objuser:
#                 fullname =   objuser[0].get('fullname')
#                 items.append(fullname)
#                 designation =  objuser[0].get('designation')
#                 items.append(designation)

#             else:
                    
#                 items.append("No User Defined")
            
#             if index < currentQueSeries: 
#                 #get all time stamps for all que series
#                 #index basically denominates Que series level. if Current que series =2 then only actionee = 0 and Approver 1 has signed
#                 lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=index).order_by('-history_date').values()
                
#                 if lstdictHistory: #to fix testing bug
#                     timestamp = lstdictHistory[0].get('history_date') # get just the first record assume decending is the way togo
#                 else:
#                     timestamp = []

#                 items.append(timestamp)
                
#                 finallstoflst.append(items)
                
#                 items =[]
            
#             else:
#                 #this simply says that i will give a time stamp for rest of levels to 0- no date and time
                
#                 items.append(0)
#                 finallstoflst.append(items)
#                 items =[]
        
    
#           #que series will decide number of people whom have signed +1 because actionee is 0- Need a matching list index
        
#         return finallstoflst

#edward new signatories for closeoutpreint 20210706
def blgettimestampuserdetails (id, Signatories):
        #pass in all Signatories and ID of action
        #return Signatories with Time Stamp
        
        #firstgetcurrentqueseries
        
        lstDictQueSeries = ActionItems.objects.filter(id=id).values('QueSeries')
        currentQueSeries = lstDictQueSeries[0].get('QueSeries')
        
        #next get all history that has got to do with ID from history tables
        #thinking that if you order by decending then you are done by getting latest first
        lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=currentQueSeries).order_by('-history_date').values()
        # edward appending blank string as filler 20210707   
        filler= ''
        finallstoflst = []                                   
        for index, items in enumerate(Signatories):
            
            #get each user detail first
            objuser = CustomUser.objects.filter(email=items[1]).values()
                      
            if objuser:
                fullname =   objuser[0].get('fullname')
                items.append(fullname)
                designation =  objuser[0].get('designation')
                items.append(designation)
                # signature =  objuser[0].get('signature')
                # items.append(signature)

            else:
                    
                items.append("No User Defined")
            
            if index < currentQueSeries: 
                #get all time stamps for all que series
                #index basically denominates Que series level. if Current que series =2 then only actionee = 0 and Approver 1 has signed
                lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=index).order_by('-history_date').values()
                
                if lstdictHistory: #to fix testing bug

                #edward trying to pass signature only if signed 20210707
                    signature = objuser[0].get('signature') 
                    
                    timestamp = lstdictHistory[0].get('history_date') # get just the first record assume decending is the way togo
                    
                else:
                #edward trying to pass signature only if signed 20210707
                    signature = [] # there is a bug here or i am making a mistake, not recognizing empty list after else but can print empty list
                    timestamp = []
                   
                #edward trying to pass signature only if signed 20210707   
                items.append(signature) 
                items.append(timestamp)
                
                finallstoflst.append(items)
                
                items =[]
            
            else:
                #this simply says that i will give a time stamp for rest of levels to 0- no date and time
                # edward 20210707 commented items.append(0) below
                # items.append(0) #appending zero here seems to substitute the signature field with zero when no one has signed, works for datefield but shows zero on page for signature
                # edward appending blacnk string as filler 20210707               
                items.append(filler)
                items.append(filler)
                finallstoflst.append(items)
                
                items =[]
        
    
          #que series will decide number of people whom have signed +1 because actionee is 0- Need a matching list index
        
        return finallstoflst
        #end of edward closeoutprint

def blgetDiscSubOrgfromID (ID):
    ''' just returns the company, disipline and sub (Triplet) for an object based on id of object in ActionItems
    Org was placed at the last because other existing functions use Disc and Sub first. The return is a triplet of 
    DiscSubOrg as a List '''
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
    
def blgetIndiResponseCount2(discsuborg,queseriesopen,queseriesclosed,phase=""): #Guna 20210703 to be consolidated

    indiPendingSeries =[]
    completePendingPair = []
    filler = 0
    #first loop through all routes disc/sub/org
    for itemtriplet in discsuborg:
        
        # totalopencount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesopen) 
        # totalclosedcount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesclosed)
        totalopencount = blphasegetDiscSubOrgActionCountQ (itemtriplet,queseriesopen,phase) 
        totalclosedcount = blphasegetDiscSubOrgActionCountQ (itemtriplet,queseriesclosed,phase)

        lstofActioneeApprover = blgetSignotories(itemtriplet)

       
        #indiPendingPair.append(itemtriplet)
        for indique,indipair in enumerate(lstofActioneeApprover):
            if (indipair != []):
                
                #indiPendingSeries.append(indique) #Append QueSeries
                lstindique = [indique] #make que series into list otherwise doesn work, indique is 0 for Actionee-start of loop                
                indiPendingSeries.append(indipair[1]) #append Name - #indipair gives all users in routes print indipair,indipendingseries
                #pendingResponse = blgetDiscSubOrgActionCount ('Y',itemtriplet,lstindique) #just uses queseries and maps back to the
                pendingResponse = blphasegetDiscSubOrgActionCountQ (itemtriplet,lstindique)

                #pendingresponse = blgetDiscSubOrgActionCount ('Y',itemtriplet,lstindique)
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
         
            indiPendingSeries = []

    

    finallistoflist = [x for x in completePendingPair if x]    
    return finallistoflist
def blgetActionStuckAt(allactions, lstoftableattributes,email=False):
    '''Pass a list of normmally all actions  and list of attributes to send back through 
    with where the action is stuck at'''
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
        lstgettriplet = [strdiscipline,strsubdiscipline,strorganisation] #edward 20210805 gets discsuborg from all the ActionItems
        lstofActioneeAppr = blgetSignotories (lstgettriplet) #edward 20210805 gets Action Route for each action, if you print you get AR for each Action in server/db
        

        
        if items.QueSeries != 99 and (lstofActioneeAppr !=[]): # basically its looks at que series and then matches it against the list of entire signatories above
            lststuckAt = lstofActioneeAppr[items.QueSeries]#basically just uses QueSeries to tell us where its stuck at #edward 20210805 uses qseries to match AR e.g. if 0 then Actionee
            
            lstActionDetails.append("/".join(lststuckAt)) # Because there is 2 parts to the formula = Actionee , gunav -- So im Just joining them into string
        else:
            lstActionDetails.append ("Closed") # if its 99 just have a tag closed 
        lstofindiactions.append (lstActionDetails)
        lstActionDetails =[]

    
    return lstofindiactions
#Guna new function for dict
# Cant get edward dictionary to work below
def blgetdictActionStuckAt(allactions):
    '''Pass a dictionary object from .values(...) and get the action stuck at data. This is done by gettings triplet 
    and then mapping against signatories and then using queseries to decifer in that route
    which signatory holds the actions. allactions passed in and modified directly and returned without making a copy of it. This will be the approach from here'''
   
    for items in allactions:
        
        lstoftriplet = blgetDiscSubOrgfromID (items['id']) 
        lstofActioneeAppr = blgetSignotories (lstoftriplet)
        
        if items['QueSeries'] != 99 and (lstofActioneeAppr !=[]):
             # basically its looks at que series and then matches it against the list of entire signatories above
            lststuckAt = lstofActioneeAppr[items['QueSeries']]#basically just uses QueSeries to tell us where its stuck at
            items['StuckAt'] = "/".join(lststuckAt)
            
        else:     
            items['StuckAt'] = "Closed"
   
    return allactions

#   edward 20210805 dictstuckat
# to have a generic function to pass in table headers for excel to call in views
def blgetActionStuckAtdict(allactions,email=False):

    lstActionDetails = []
    lstgettriplet = []
    
    for items in allactions : 

        # for x in lstoftableattributes: 
        #     lstActionDetails.append(x)

        strdis=items['Disipline'] # edward just using K-VP to identify & get the items
        strsubdis=items['Subdisipline']
        strorg=items['Organisation']

        lstgettriplet = [strdis,strsubdis,strorg] 
        lstofActioneeAppr = blgetSignotories (lstgettriplet)
        
        if items['QueSeries'] != 99 and (lstofActioneeAppr !=[]): #edward - looks at key QueSeries & its value pairs 
            lststuckAt = lstofActioneeAppr[items['QueSeries']] #edward - uses QSeries to see which level in AR it is
            lstActionDetails.append("/".join(lststuckAt)) # edward using similar method as blgetActionstuckat to combine 
            items['Action with'] = lstActionDetails[0] # edward sort of appending this value to a key
        else:
            items['Action with'] = ("Closed") # if its 99 just have a tag closed 

        
        Actionee = ActionRoutes.mdlgetActioneeAppr.mgr_getactioneefromtriplet(lstgettriplet) # getting Actionee for each Item
        items['Actionee'] = ((Actionee[0])['Actionee']) # just getting the Actionee from QuerySet

        
        
        lstActionDetails =[]
        allactionswithlocation = allactions
        
            
    return allactionswithlocation
#edward 20210805 dictstuckat

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

# edward 20210708 created new bl for signatory by queue 
def blgetSignatoryemailbyque2(lstdiscsuborg,queseries):
    
    pairSignatories = blgetSignotories(lstdiscsuborg) #just reusing what is already done 

    for items in pairSignatories:
        items.pop(0) # basically removes the Actionee, Approver from pair and maintains name
    
    abbrevatedemail=pairSignatories[queseries-1:queseries+1] # sends to current person who submits and the next person, dont know why this is -1 should be just queseries
    
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
    
    
    actionitemsbyid = ActionItems.objects.filter(id__in=dictofids).values(
        'id','StudyActionNo','StudyName__StudyName','Disipline',
                    'Subdisipline', 'Cause', 'Recommendations','DueDate',
                    'InitialRisk'

    )

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

# def blallphasegetAction(que,phase=""):
#     '''this function gets all actions and or phases . Pass phase and QueSeries to get count 
#     of items in a list of QueSeries[open,closed etc]'''
#     count = 0

#     for eachQs in que:
#         if phase!="":
#             filters = {'QueSeries':eachQs,'ProjectPhase__ProjectPhase':phase}
#         else:
#             filters = {'QueSeries':eachQs}

#         count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFilters(filters) 
   

#     return count



def blphasecreatepie(labels,values,title):
    '''Takes labels pie values and titles and  creates charts'''
    
    labels = labels
    values = values
    
    pienameoverall = title
    googlechartlistoverall = blprepGoogChartsbyStudies(labels,values,pienameoverall)
    
    return googlechartlistoverall
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
   
def blgetCompanyActionCount(company,quelist,phase="") :

    count = 0

    for eachQs in quelist:
        count += ActionItems.mdlgetActionCompanyCount.mgr_getCompanyCount(company,eachQs,phases=phase) 
   
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
    

def blstopcharttoday(content,testtotal,testclosed):
    " Function that stops the Rundown curve at todays date. edward 20211021 "
    
    strtoday = dt.today().strftime('%Y-%m-%d') #todays date as string
    today= dt.today()#.strftime('%Y-%m-%d') #todays date as date object

    actual = (testtotal-testclosed) # use this to append the actual data which is Total - Closed
    
    currentdate = [today,' ',actual] # it is what it says it is

    for items in content:
        items[0] = datetime.datetime.strptime(items[0], '%Y-%m-%d').date() # convert from string to date object. datetime obj has problems bcs comparing down to the minute

    if not any(today in items for items in content) : #using list comprehension in place of for loop to look for date inside the list of list 
        content.insert(0,currentdate) # insert at beginning of the list
    else :
        content
    sortedcontent = sorted(content, key=itemgetter(0)) # sorts  the list after insertion. itemgetter(0) sorts by first entry inside list of list (date in this case) 
    
    for items in sortedcontent:        
        items[0]=items[0].strftime('%Y-%m-%d') # convert date object back to string so js can use it
        if items[0]> strtoday:
            items.pop(2)
      
    updatedcontent=sortedcontent
    

    return updatedcontent
# edward 20210723 end new graphing to stop on current day

#edward 20210803 excel

def bladdriskcolourandoptiforflater2 (actionitems):
    
    dfRiskMatrix = pd.DataFrame(list(RiskMatrix.objects.all().values()))
            
    for items in actionitems:
               
                #[items.pop(key) for key in removelist] # Reducing the data going to html
                #
                RiskColour = dfRiskMatrix.loc[dfRiskMatrix['Combined'].isin([items.get('InitialRisk')]),'RiskColour'].tolist() #cant use .item() as its causing an error when not matching
                
                if RiskColour:
                    items['RiskColour'] = RiskColour[0]
                else: 
                    items['RiskColour'] = False
    
    return actionitems

