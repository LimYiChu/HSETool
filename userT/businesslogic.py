from ast import Index
from tarfile import XGLTYPE

from matplotlib import testing
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
from collections import Counter


def blholdtime(allaction):
    """This function gets the cumulative holding time for all Actions in Actioneee or Approver basket"""
    timezonenow = timezone.now()

    for items in allaction: 

        if items['QueSeries'] != 99:
            
            if items['QueSeries'] != 0: 
                ID = items['id']
                dictactualhistory = ActionItems.history.filter(id=ID).order_by('-history_date').values('history_date')
                historyrecentimeapp = dictactualhistory[0].get('history_date')
                timeinbasket = timezonenow - historyrecentimeapp    
                items['HoldingTime'] = timeinbasket.days 

            else:
                ID = items['id']
                historyrecentimeapp = items.get('DateCreated')
                timeinbasket = timezonenow.date() - historyrecentimeapp  
                items['HoldingTime'] = timeinbasket.days 

        else:
            items['HoldingTime'] = "None"

    return allaction

def blaggregatebyDisc_hidden(discsuborg, lstbyDisc_hidden):
    """
    27/04/2022 Ying Ying 
    Created to get disuborg list as hidden element to pass to dynamic discipline table. 
    Add Dissuborg list (e.g ['dis','sub','org']) as hidden element for PMT reporting discipline table.
    """
    for x, y in enumerate(lstbyDisc_hidden):
        y.append(discsuborg[x])
   
    return lstbyDisc_hidden


def bldynamicindisummchart(dfindisummsorted):
    """ 
    27/04/2022 Ying Ying 
    This function gets the count of how many closed & open actions for dynamic indisumm first dynamic charts
    """
    dfcopysorted = dfindisummsorted.copy()
    dfcopysorted.drop_duplicates(subset=['Organisation Route'], keep='first', inplace=True)
    dfcopysorted.drop(columns=['Pending Submission', 'Pending Approval'], axis=1, inplace=True)
    df_sum = dfcopysorted.sum(numeric_only=True)
    dfcloseopenlist = df_sum.values.tolist()
    headerlist = ['Closed', 'Open Actions']
    opencloselst = [list(l) for l in zip(headerlist, dfcloseopenlist)]
    return opencloselst


def bldynamicindisummpend(dfalldynamicindisummsorted):
    """
    27/04/2022 Ying Ying 
    This function gets the number of pending submission and pending approval action for dynamic indisumm second dynamic charts
    """
    dfcopysorted = dfalldynamicindisummsorted.copy()
    dfcopysorted.drop(columns=['Closed', 'Open Actions'], axis=1, inplace=True)
    df_sum = dfcopysorted.sum(numeric_only=True)
    dfcloseopenlist = df_sum.values.tolist()
    headerlist = ['Pending Submission', 'Pending Approval']
    pendinglst = [list(l) for l in zip(headerlist, dfcloseopenlist)]
    titlelst = ['\\\Status:::', 'Number']
    pendinglst.insert(0,titlelst)
    return pendinglst


def bldynamicindisummactionformat(filteredstring, reducedfields):
    """
    27/04/2022 Ying Ying 
    This function gets the open action, closed action, pending submission and pending approval from discipline, organization and suborganization for user.
    """
    disuborg_list = blgetdisuborg(filteredstring)
    combinelst = blgetIndiResponseCount2(disuborg_list, QueOpen, QueClosed, phase="") 
    Email_filter = [filteredstring]                                                                       
    Indisets = [i for i in combinelst if any(b in Email_filter for b in i)]
    indisumm_dict = []
    for row in Indisets:
        indisumm_dict.append(dict(zip(reducedfields, row)))
    return indisumm_dict

    
def blgetdisuborg(clickedemail):
    """
    27/04/2022 Ying Ying 
    This function gets the discipline, organization and suborganization involved by user 
    """
    data = blgetuseroutesnew(clickedemail)
    
    Actioneelist = [item for item in data['Actionee_Routes']]
    Approver_dict = data.get('Approver_Routes') 
    Approver_convertlst = [Approver_dict[i] for i in Approver_dict if Approver_dict[i]!=[]]      
    Approver_rmxbracket = [val for sublist in Approver_convertlst for val in sublist]    
    
    Actioneelist.extend(Approver_rmxbracket)
    ActioneeApproverdiscuborg = [[i["Disipline"],i["Subdisipline"],i["Organisation"]] for i in Actioneelist]
    ActioneeApprover_disuborg = [i for n, i in enumerate(ActioneeApproverdiscuborg) if i not in ActioneeApproverdiscuborg[:n]]

    return ActioneeApprover_disuborg


# def blgetallapproverlevels(usersemail):
#     """
#     10/04/2022 Ying Ying 
#     This function gets the information for discipline, subdisipline, organisation and the entire action route of the usersemail for approver role. 
#     """
#     All_Routesxx = ActionRoutes.objects.values()
#     Approver_Level = 8
#     Approver_Routes = {}
#     for Approver_Level in range(1, Approver_Level+1):
#         Approver_Routes [Approver_Level] = list(filter(lambda approver: approver['Approver'+str(Approver_Level)] == usersemail, All_Routesxx))
#     return Approver_Routes


def bldynamicstudiesactionformat(filteredstring,reducedfields):
    """
    This function gets the filtered string & reduced fields for the dynamic studies & then adds the risk elements & where the action is stuck at & subsequently returns the formulated action set
    """
    actionsbystudy = blgetsinglefilteractionsitemsQ(filteredstring,reducedfields) #getting actions based on studies filter
    actionswithrisk = bladdriskelements(actionsbystudy) 
    actionsstuckat = blgetdictActionStuckAt(actionswithrisk)
    return actionsstuckat


def bldynamicstudiesdisc(actionsstuckat):
    """
    This function gets the count for pending submission,submitted,closed,open & total actions for disciplines based on each studies.
    """
    discmultilist=[]
    actionsvalues = actionsstuckat.values('Disipline',
                'Subdisipline','Organisation')
    dfactionitem = pd.DataFrame(actionsvalues)
    dfactionitemfilter = dfactionitem.drop_duplicates()
    dfdiscsuborglist = dfactionitemfilter.values.tolist()
    discheaderlst = ['Discipline', 'Pending Submission' ,'Submitted', 'Closed','Open Actions','Total Actions']
    discmultilist.append(discheaderlst)
    disclst= blaggregatebyDisc(dfdiscsuborglist,  YetToRespondQue, ApprovalQue,QueClosed,QueOpen,TotalQue)
    discmultilist.append(disclst)
    return discmultilist


def blriskranking(ActioneeActionsrisk, Approver_R, reducedfields) :
      """
      This function gets the risk ranking summary that shows the count of actions in low medium and high in the first box
      """
      newcounter = {}
      riskrankingsummary = blaggregateby(ActioneeActionsrisk,"RiskRanking")
      for QSeries, ApproRoutes in Approver_R.items():
          ApproverActions = blallactionscomdissubQ(ApproRoutes,QSeries,reducedfields)
          ApproverActionsrisk = bladdriskelements(list(ApproverActions))
          riskrankingapproverraw = blaggregateby(ApproverActionsrisk,"RiskRanking")
          if riskrankingapproverraw is not None:
              newcounter = Counter(riskrankingapproverraw) + Counter(newcounter)
              riskrankingapprover = newcounter
              riskrankingactionee = Counter(riskrankingsummary)
              riskrankingsummary = riskrankingapprover + riskrankingactionee
      return riskrankingsummary


def bldynamicchartopen(dfalldynamicstudiessorted):
    """
    This function gets the Action Stuck at for the dynamic Submitted Chart
    """
    dfcountopenfilter = ['ActionAt']

    dfcopysorted = dfalldynamicstudiessorted.copy()
    dffilteropensorted = blsortdataframes(dfcopysorted,dfcountopenfilter)
    dffilteropensorted['ActionAt'] = dffilteropensorted.ActionAt.str.split('@').str.get(0)
    dffilteropensorted['ActionAt'] = dffilteropensorted.ActionAt.str.split('/').str.get(-1)
    dffilteropensorted['count'] = dffilteropensorted.ActionAt.map(dffilteropensorted.ActionAt.value_counts())
    dffinalcountloc = dffilteropensorted.drop_duplicates()
    dffilteropen = dffinalcountloc.loc[dffinalcountloc['ActionAt'].str.contains('Closed') == False]
    dfstuckatlst=dffilteropen.values.tolist()
    headerlst = ['\\\Action At:::','Actions']
    dfstuckatlst.insert(0,headerlst)
    return dfstuckatlst


def bldiscstrmatch(data) :
    """ This function does a string matching on the discsuborg for use in the discipline dynamic table"""
    emptylst = []
    blanklst = []
    discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg()
    for items in discsuborg:
        blanklst.append("/".join(items))
        
        if [item for item in [data] if item in blanklst] :
            emptylst.append(items)
    discsuborglst = emptylst[0]
    return discsuborglst


def bldynamicchart(dfsorted):
    """ This function gets the count of how many closed & open actions for dynamicstudies and dynamicdiscipline dynamic charts"""
    dfcopysorted = dfsorted.copy()
    dfcopysorted.loc[dfcopysorted['ActionAt'] == 'Closed','Closed Action'] = 'Closed' 
    dfcopysorted.loc[dfcopysorted['ActionAt'].str.contains('Closed') == False,'Open Action'] = 'Open'
    dfcloseopen = blsortdataframes(dfcopysorted,dfdonutcolumns)
    dfcloseopenlist = dfcloseopen.values.tolist()
    flat_list = [item for sublist in dfcloseopenlist for item in sublist]
    dfcountclosed = flat_list.count('Closed')
    dfcountopen = flat_list.count('Open')
    lstofcount =[]
    countclosed = ['Closed', dfcountclosed]
    countopen = ['Open', dfcountopen]
    lstofcount.append(countclosed)
    lstofcount.append(countopen)
    return lstofcount
    

def blexceedholdtime(Approver_R,reducedfileds):
    """This function gets the number of actions with holding time more than 1 or 2 weeks """
    timezonenow = timezone.now()
    oneweeklist=[]
    twoweeklist=[]
    countlistbyweek = []
    sevendays = datetime.timedelta(days=7)
    fourteendays = datetime.timedelta(days=14)

    for QSeries, ApproRoutes in Approver_R.items():
        ApproverActions= blallactionscomdissubQ(ApproRoutes,QSeries,reducedfileds)
    
        for items in ApproverActions:
            dictactualhistory = ActionItems.history.filter(id=items["id"]).order_by('-history_date').values()
            historyrecentimeapp = dictactualhistory[0].get('history_date')
            timeinbasket = timezonenow - historyrecentimeapp

            if timeinbasket > sevendays :
                oneweeklist.append(items["id"])

            if timeinbasket > fourteendays :
                twoweeklist.append(items["id"])
         
    oneweekcount = len(oneweeklist)
    countlistbyweek.append(oneweekcount)
    twoweekcount = len(twoweeklist)
    countlistbyweek.append(twoweekcount)
    return countlistbyweek


def bltotalholdtime(Approver_R,reducedfileds):
    """This function gets the cumulative holding time for all Actions in Actioneee or Approver basket"""
    timezonenow = timezone.now()

    blanklist=[]

    for QSeries, ApproRoutes in Approver_R.items():
        ApproverActions= blallactionscomdissubQ(ApproRoutes,QSeries,reducedfileds)
        
        for items in ApproverActions:
            dictactualhistory = ActionItems.history.filter(id=items["id"]).order_by('-history_date').values()
            historyrecentimeapp = dictactualhistory[0].get('history_date')
            #using current time & subtracting the history date to get all the timestamp for each id & history date got from dictactualhistory
            timeinbasket = timezonenow - historyrecentimeapp
            blanklist.append(timeinbasket)
    dfdates = pd.DataFrame(blanklist)
    
    if not dfdates.empty : 
        dfdatessum = dfdates.sum(axis=0)
        dftodict = dfdatessum.to_dict()
        new_key = "total"
        old_key = 0
        dftodict[new_key] = dftodict.pop(old_key)
        if dftodict['total'].days < 1:
            strdays = "0"
        else:
            strdays = str(dftodict['total'].days)
        return strdays


def bldfdiscsuborgphase(phase):
    """This function gets the discsuborg for actions based on differing phases"""
    if phase == "":
        ActionItem = ActionItems.objects.values('Disipline',
                        'Subdisipline','Organisation')
    else:
        ActionItem= ActionItems.objects.filter(ProjectPhase__ProjectPhase=phase).values('Disipline',
                        'Subdisipline','Organisation')
                        
    dfactionitem = pd.DataFrame(ActionItem)
    dfactionitemfilter = dfactionitem.drop_duplicates()
    dfactionitemlist = dfactionitemfilter.values.tolist()
    return dfactionitemlist


def blexcelgetactioneeandlocation (dfalllist):
    lstActionDetails = []
    for items in dfalllist:  
        lstoftriplet = blgetDiscSubOrgfromID (items['id']) 
        lstofActioneeAppr = blgetSignotories (lstoftriplet)
        if items['QueSeries'] != 99 and (lstofActioneeAppr !=[]): #edward - looks at key QueSeries & its value pairs 
            lststuckAt = lstofActioneeAppr[items['QueSeries']] #edward - uses QSeries to see which level in AR it is
            lstActionDetails.append("/".join(lststuckAt)) # edward using similar method as blgetActionstuckat to combine 
            items['Action with'] = lstActionDetails[0] # edward sort of appending this value to a key
        else:
            items['Action with'] = ("Closed") # if its 99 just have a tag closed 
        Actionee = ActionRoutes.mdlgetActioneeAppr.mgr_getactioneefromtriplet(lstoftriplet) # getting Actionee for each Item
        items['Actionee'] = ((Actionee[0])['Actionee']) # just getting the Actionee from QuerySet
    return dfalllist


def blfilteractionsbyphase(finallistoflist):
    phaseindisets = []
    for items in finallistoflist:
        for item in items:
            # looks at pending submission, pending approval,closed,open actions to determine if there is anything > 0 (determined by phase, eg if you select phase T&I it will only show the values for each selected phase in range (3,6), then it will print items which contains those that are >0
            if item in range(3,6) != 0: 
                phaseindisets.append(items)
    return phaseindisets


def bladdfktodict(data_dict,foreignkeys):
    """This functions adds foreignkeys to Action Items data dictionary"""
    data_dict.update(foreignkeys) # updating original with study & phase 
    return data_dict


def blremoveemptylist (listoflist):
    """This function passes in list of list and returns list with no empty list"""
    listfinal = [ele for ele in listoflist if ele != []]
    return listfinal


def blannotatefktomodel(actionvalues):
    """This function passes queryset dictionary values() from ActionItems Table only and then Annotates (adds) the foriegn key StudyName and Project Phase to the Model"""
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
    

def blmakedir(makedstdir):
    """Creates a directory even if that directory already exists"""
    createddir = os.makedirs(makedstdir,exist_ok=True)
    return createddir


def blbulkdownload(objactionitems,destinationfolders,createzipfilename): 
    """This function does the bulkdownload for the PDF closeoutreports"""
    for items in objactionitems: 
        closed = True
        if closed == True :
            items['StudyActionNo'] = items['StudyActionNo'].replace("/","_")
            newcloseouttemplate = blsetcloseouttemplate (items['id'])
            data_dict=items
            discsub = blgetDiscSubOrgfromID(items['id']) 
            Signatories = blgetSignotories(discsub) 
            lstSignatoriesTimeStamp= blgettimestampuserdetails (items['id'], Signatories) 
            currentQueSeries = blgetFieldValue(items['id'],'QueSeries')
            blgettimehistorytables(items['id'],lstSignatoriesTimeStamp,currentQueSeries)
            studyactno = items["StudyActionNo"] 
            studyactnopdf = (studyactno + '.pdf')
            signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp)
            makesubfolders = os.makedirs(destinationfolders + studyactno, exist_ok=True )
            destination =destinationfolders + studyactno 
            out_file = os.path.join(destination,studyactnopdf)
            file = pdfgenerate(newcloseouttemplate,out_file,data_dict,signatoriesdict)
            objFk =ActionItems.objects.get(id = items['id']) 
            ObjAttach = objFk.attachments_set.all()

            for eachfile in ObjAttach: 
                filename = os.path.basename(eachfile.Attachment.path) # changed from .name to .path
                attachmentorigin= bulkdlattachments + filename
                dst = os.path.join(destination, os.path.basename(attachmentorigin))
                shutil.copyfile(attachmentorigin,os.path.join(dst) ) #copying all done inside for loop for each attachment

    returnzipfile = shutil.make_archive(createzipfilename, 'zip', destinationfolders)

    return returnzipfile


def blexcelformat (dfallsorted,workbook,worksheet):
    """This function sets the formatting for the excel workbook which is sent to client"""
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
    worksheet.set_default_row(25)
    return worksheet


def blsortdataframes(dfall,sortedheader) : 
    """This function sorts dataframes in which order that the user wants. 
    User passes in all the data in dfall & it uses a list for sortedheader to sort the data based on the order of headers in sortedheaders"""
    #sorting the columns based on specified sortedheader list if you want alphabetically just use df.sort_index(axis=1)
    sortedfall = dfall.reindex(columns=sortedheader) 
    return sortedfall


def blduedateecountrelative (dictofdates):
    """Pass in dict of due dates and it checks due dates and returns a dict of count 
    for isduedate, isduein1week, isduein2weeks. Uses Releativedelta and 1week=8days 2 weeks=15days added 
    to check due date horizon"""
    if dictofdates:
        isdue = {duedate:count for duedate, count in dictofdates.items() if date.today()>duedate}
        isduevalues = isdue.values()
        isduecount = sum(isduevalues)

        isduenextweek = {duedate:count for duedate, count in dictofdates.items() if date.today()+relativedelta(days=+8)>duedate}
        isduenextweekvalues = isduenextweek.values()
        isduein1weekcount = sum(isduenextweekvalues) - isduecount

        isduein2weeks = {duedate:count for duedate, count in dictofdates.items() if date.today()+relativedelta(days=+15)>duedate}
        isduein2weeksvalues = isduein2weeks.values()
        isduein2weekscount = sum(isduein2weeksvalues) - isduecount - isduein1weekcount
        return {"isdue":isduecount,"isduein1week":isduein1weekcount,"isduein2weeks":isduein2weekscount}


def blaggregateby(actionitems,fieldtoaggregate):
    """Actions items will be aggregated according to the required field. pass in action items and 
    field (must be in the action items) and the function will aggregate or summarise with a count and return Dictionary object """
    if actionitems:
        dfallactions = pd.DataFrame(actionitems)
        dfallactionssortbyranking = dfallactions[fieldtoaggregate].value_counts()
        return dfallactionssortbyranking.to_dict()

def bladdriskelements (actionitems):
    """ Accepts dictionary only items and then extracts InitialRisk using dataframes,
    then looks up RiskMatrix Model and gets a risk colour. It uses the Combined value in the RiskMatrix to map back to the Risk COlour
    the second parameter is optional seprate funtinality for removing addtional fields. """
    if actionitems:
        dfRiskMatrix = pd.DataFrame(list(RiskMatrix.objects.all().values())) 
        for items in actionitems:
                    #[items.pop(key) for key in removelist] 
                    RiskValue = dfRiskMatrix.loc[dfRiskMatrix['Combined'].isin([items.get('InitialRisk')]),['RiskColour','Ranking']]
                    if not RiskValue.empty:
                        items['RiskColour'] = RiskValue['RiskColour'].item()
                        items['RiskRanking'] = RiskValue['Ranking'].item()
                    else: 
                        items['RiskColour'] = False
                        items['RiskRanking'] = False
    else :
        actionitems = []
    return actionitems


def bladdriskcolourandoptimise (actionitems,removelist=[]):
    """ Accepts dictionary only items and then extracts InitialRisk using dataframes,
    then looks up RiskMatrix Model and gets a risk colour. It uses the Combined value in the RiskMatrix to map back to the Risk COlour
    the second parameter is optional seprate funtinality for removing addtional fields. Next revision this should be separated """
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
    """This function groups by aggregate summary, DOCSTRING TO BE EDITED"""
    dfindisets = pd.DataFrame(databody,columns=dataheader)
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


def blgetriskmatrixtable ():
    count = RiskMatrix.objects.all().count()

    if count == 0 :
        blntable = False
    elif (count > 0) :
        blntable = True
    return blntable


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
    return availability


def blgetuseroutesnew(useremail):
    """This new functions get all routes for logged on user or any user passed in. Its an improvement to
    the function blgetuserRoutes. it uses python filter and dictionary comprehension for approver loops and instead of
    of hitting the database just does a quick pythonic filter. Have to use .values for this"""

    ApproverLevel = 8
    Approver_Routes = {}
    Actionee_Routes = ActionRoutes.ActioneeRo.get_myroutes(useremail).values()
    All_Routes = ActionRoutes.objects.values()
    for ApproverLevel in range(1 , ApproverLevel+1):
        Approver_Routes [ApproverLevel] = list(filter(lambda approver: approver['Approver'+str(ApproverLevel)] == useremail, All_Routes))
    dictRoutes = {
       'Actionee_Routes' : Actionee_Routes,
       'Approver_Routes': Approver_Routes,
    }
    return dictRoutes


def blgetuserRoutes(useremail):
    ApproverLevel = 8
    userZemail = useremail
    Approver_Routes = {}
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
    """This email sends individual email notifications to each user"""
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


def blgetActualRunDown(lstdatesandcount,closeditems): 
    """This function gets the Actual Rundown Curve for All Actions that are closed.
    Parameters lstdatesandcount is passing in due dates and how many were meant to be closed & closeditems are how many items that are closed ( Queseries = 99 )"""
    closed = 99 #queseries
    countX = 0

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
    return finalactual


def blaggregatebydate (objActions):
    """This function aggregates the duedate by counting each action item"""
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
    """Pass in id of actions, and string of where its coming from i.e "Actionne", "Approver", "Reject" that have been submitted or approved and rejected and it returns list [Subject, Content]
    Optional Parameter of reject reason can be passed in to state reason in content"""
    urlview = f"/pmtrepviewall/{ID}/view"
    urlviewApprover = f"/ApproverList/{ID}/approve" # Not used yet thinking of redoing url below for simplification
    urlviewRejection = f"/ActioneeList/{ID}/update"
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
        'ActioneeContent' : "To view this, please go to " + paremailurl + urlviewApprover + " . To approve go to your dashboard/approver que, to approve this and other actions",
        'ApproverContent' : "To view this, please go to " + paremailurl + urlviewApprover + " . To approve go to your dashboard/approver que, to approve this and other actions",
        'RejectContent' : "Rejection Reason : " + RejectReason + ". To attend to this go to your dashboard, view of rejection is available at " + paremailurl +urlviewRejection,
    }

    #as pythonic as it gets
    Content = [ v for k,v in dictofsubjectcontent.items() if k.startswith(ActioneeApproverReject)]
    return Content


def blgetHistoryforUser(useremail, actioneeroutes):
    """This function gets the History for the User"""
    #first get user ID from CustomUser as only user id is used in history tables
    ApproverQue = [1,2,3,4,5,6,7,8,9] #Once its closed its done is it so 99 is taken out
    lstUserSeries =  CustomUser.objects.filter(email=useremail).values()
    currentUserID = lstUserSeries[0].get('id')
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
    test = discsuborg

    for items in discsuborg:
        lstrejectcountbydisc.append("/".join(items))
        lstrejectcountbydisc.append(ActionItems.mdlgetActionDiscSubCount.
                                        mgr_getDiscSubOrgRejectedItemsCount(items,revision)) 
        
        lstfinallistcount.append(lstrejectcountbydisc)
        lstrejectcountbydisc = []
    return lstfinallistcount



def blaggregatebyDisc(discsuborg, YetToRespondQue, ApprovalQue, QueClosed, QueOpen, TotalQue):
    """Agregates by discpline across organisation. Takes in various QueSeries denoting Yettorespond, Approval 
    Open Actions, Total Queue"""
    lstofdiscdetails =[]
    lstcountbydisc =[]
    for disc in discsuborg:
        lstcountbydisc.append("/".join(disc)) 
        lstcountbydisc.append(blphasegetDiscSubOrgActionCountQ(disc,YetToRespondQue))
        lstcountbydisc.append(blphasegetDiscSubOrgActionCountQ(disc,ApprovalQue))
        lstcountbydisc.append(blphasegetDiscSubOrgActionCountQ(disc,QueClosed))
        lstcountbydisc.append(blphasegetDiscSubOrgActionCountQ(disc,QueOpen))
        lstcountbydisc.append(blphasegetDiscSubOrgActionCountQ(disc,TotalQue))
        lstofdiscdetails.append(lstcountbydisc)
        lstcountbydisc =[]
    return lstofdiscdetails


def blallActionCountbyDisc(Disc,quelist):
    count = 0
    for que in quelist:
        count += ActionItems.myActionItemsCount.mgr_allItemsCountbyDisc(Disc,que) 
    return count


def blgetbyStdudiesCountphase(Studies,YetToRespondQue,pendingApprovalQue,closedActionsQueSeries,OpenQue,TotalQue):
    """This function is used for differentiating Studies by phase because the way the phases are coming in is by wayt of dictionary instead of a queryset (e.g. Studies.objects.all() )"""
    lstcountbyStudies = []
    lstofstudiesdetails =[]
    for Study in Studies:
        studynameQ = (Study['StudyName'])
        lstcountbyStudies.append (studynameQ)
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,YetToRespondQue))
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,pendingApprovalQue))
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,closedActionsQueSeries))
        lstcountbyStudies.append  (blallActionCountbyStudiesPhaseQ(studynameQ,OpenQue))
        lstcountbyStudies.append  (blallActionCountbyStudiesPhaseQ(studynameQ,TotalQue))
        lstofstudiesdetails.append(lstcountbyStudies)
        lstcountbyStudies =[]
    return lstofstudiesdetails


def blgetbyStdudiesCount(Studies,YetToRespondQue,pendingApprovalQue,closedActionsQueSeries,OpenQue,TotalQue):
    """Note to look into this again, seems to be obsolete as we seem to be using blgetbyStdudiesCountphase() now"""
    lstcountbyStudies = []
    lstofstudiesdetails =[]
    for Study in Studies:
        studynameQ = Study.StudyName
        lstcountbyStudies.append (studynameQ)
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,YetToRespondQue))
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,pendingApprovalQue))
        lstcountbyStudies.append (blallActionCountbyStudiesPhaseQ(studynameQ,closedActionsQueSeries))
        lstcountbyStudies.append  (blallActionCountbyStudiesPhaseQ(studynameQ,OpenQue))
        lstcountbyStudies.append  (blallActionCountbyStudiesPhaseQ(studynameQ,TotalQue))
        lstofstudiesdetails.append(lstcountbyStudies)
        lstcountbyStudies =[]
    return lstofstudiesdetails


def blconverttodictforpdf(lstofsignatories): 
    for items in lstofsignatories:
        time = items[5] 

        if time == []    :    
            localtimeX = timezone.localtime() #edward changed this according to new bl function for signatures 20210706    
            fields = items[0]
        
            if ("actionee" in fields.lower()) :
                #localtimeX = timezone.localtime(items[5]) #edward changed this according to new bl function for signatures 20210706
                #edward changed this to add actioneesignature according to new bl function for signatures 20210706
                dict = {'actionee':items[0], 'actioneerole':items[3],'actioneename':items[2],'actioneesignature':items[4],
                        'actioneetimestamp':localtimeX
                }
                
            elif ("approver"in fields.lower()):
                strappr = str(items[0])
                strapprrole = strappr+"role"
                strapprname = strappr+"name"
                strapprsignature = strappr+"signature" 
                strapprtimestamp = strappr+"timestamp"
                dictapp = {strappr.lower():items[0], strapprrole.lower():items[3],strapprname.lower():items[2],strapprsignature.lower():items[4],
                        strapprtimestamp.lower():localtimeX}
                dict.update(dictapp)

        else:   
            localtimeX = timezone.localtime(time) 
            fields = items[0]
        
            if ("actionee" in fields.lower()) :
                dict = {'actionee':items[0], 'actioneerole':items[3],'actioneename':items[2],'actioneesignature':items[4],
                        'actioneetimestamp':localtimeX
                }
                
            elif ("approver"in fields.lower()):
                strappr = str(items[0])
                strapprrole = strappr+"role"
                strapprname = strappr+"name"
                strapprsignature = strappr+"signature" #edward added strapprsignature according to new bl function for signatures 20210706
                strapprtimestamp = strappr+"timestamp"
                dictapp = {strappr.lower():items[0], strapprrole.lower():items[3],strapprname.lower():items[2],strapprsignature.lower():items[4],
                        strapprtimestamp.lower():localtimeX}
                dict.update(dictapp)
    return(dict)

def blmultisignareplace (Signatories,emailid,ActioneeApprover=""):

    """ This is for multiple signatory . This function searches signatory for actionee or approver level passed in and 
    reduces it to a single person showing on the signatory section.It finds it in list of list and then strips out all others
     And uses tuple to get value to insert into index you need to change."""

    indexaAcctAppr= [[index for actappr in items if actappr == ActioneeApprover]
                            for index, items in enumerate(Signatories) ]
    res = [item for sublist in indexaAcctAppr for item in sublist  if sublist != [] ]
    intres = int(''.join(map(str, tuple(res))))
    Signatories [intres][1] = emailid
    
def blgetvaliduserinroute (idAI,emailid,History=False):
    """This function gets the valid users in a Route"""
    discsuborg = blgetDiscSubOrgfromID(idAI)
    queseries = blgetFieldValue(idAI,'QueSeries')
    Signatories = dict(blgetSignotories(discsuborg))
    
    # the join is just to convert into string Actionee Approver1 or Approver2
    # But just supposed to get 1 value, actionee or approver or...
    # Need to modify for testing as sometimes we want to have 
   #approveractioneeseries = ''.join([k for k, v in Signatories.items() if v==emailid])
    approveractioneeseries = ''.join([k for k, v in Signatories.items() if emailid in v])
    approverlevel= ''.join(re.findall('[0-9]+', str(approveractioneeseries)))
    
    #check this line and why we need it
    isvaliduser = emailid in Signatories.values()
   
    #must check queseries again to make sure queseries not at approver level
    #So this example below is if multiple actionee and then access id which is at approver level
    # 2 limb test must test for queseries because he could be an actionee and try and access url on approver que
    #This if statements below is to cater for testing as well where you might have been assigned to actionee and approver in one route
    #first test if you are actionee
    if  'Actionee' in approveractioneeseries :
        if (queseries==0) or History==True:
            #Used for multiple actionee, didnt split, just used direct
            isvaliduser = emailid in Signatories['Actionee'] 
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
def bldeletehistorytablesignatory(id) :
    '''Function to delete the last entry based on id . This function was done primarily 
    to solve a bug with the sinatories (blgettimehistorytables) reading from history table if Approver hits Cancel'''
    filterkwargs = {'id':id,}#'QueSeries' :QueSeries
    ActionItems.history.filter(**filterkwargs).select_related("history_user").order_by('-history_date')[0].delete()

def blgettimehistorytables (id, Signatories, QueSeries=0):
    """Gets time stamp based on queseries and whom signed from history tables. Overwrites name and time stamp from action routes
    with actual people whom have signed. This happens when routing table is changed half way through
    The idea is its the first record in history table when Queseries is one ahead
    and turns to a second record if QueSeries is 2 or more ahead .
    e.g If its queseries = 3 and you want actionee signature then it is the second record. 
    This function also caters for changing the number of approvers once actions have been closed"""
    QueSeriesTarget = 5 #Random Distant Number to be reset after first loop
    def setSignatoriesItems (setofsignatories,historyindex):
                setofsignatories [1] = lstdictHistory[historyindex].history_user.email
                setofsignatories [2] = lstdictHistory[historyindex].history_user.fullname
                setofsignatories [3] = lstdictHistory[historyindex].history_user.designation
                setofsignatories [4] = lstdictHistory[historyindex].history_user.signature
                setofsignatories [5] = lstdictHistory[historyindex].history_date

                nonlocal QueSeriesTarget 
                QueSeriesTarget = lstdictHistory[historyindex].QueSeriesTarget #sets it after the first time
               
    for index, items in enumerate(Signatories):
        
        #This is for when number of approvers have changed and want to use historic tables to formulate the signatories
        #Say if have 6 Approvers now and previous QueSeriesTarget=4 (3Approvers), have to delete last blank 3 from Signatories
        if index == QueSeriesTarget:
            if len (Signatories) != QueSeriesTarget :
                noblanksignatures = len (Signatories)-QueSeriesTarget
                del Signatories[-noblanksignatures:]
            break
        if index >= QueSeries:
            break
        #elif (index < QueSeries) and (len(Signatories)-1 != index):
        elif (index < QueSeries) and (QueSeriesTarget-1 != index):
            #Once you sign you increment the queseries . The historic tables values for user is index+1
            filterkwargs = {'id':id, 'QueSeries': index+1} 
            lstdictHistory = ActionItems.history.filter(**filterkwargs).select_related("history_user").order_by('-history_date')
            #This is the logic of one step and 2 step away
            if  QueSeries - index == 1 :
                setSignatoriesItems(items,0)
                continue
            if  QueSeries - index > 1:
                setSignatoriesItems(items,1)
        elif QueSeries == 99 and (QueSeriesTarget-1 == index):
            filterkwargs = {'id':id, 'QueSeries': 99}
            lstdictHistory = ActionItems.history.filter(**filterkwargs).select_related("history_user").order_by('-history_date')
            setSignatoriesItems(items,0)
                
    return Signatories
def blreplacemultiplesignatories (signatories,id,index):
    """returns a single signatory, just a dummy data since the exact signatory is checked 
    in blgettimehistorytables subsequently. Uses ; to check for multiple signtory and return first item
    as dummy data """
    
    multipleSignatories = ";" in signatories

    if multipleSignatories:
        listofmultiplesignatories = signatories.split(";")
        return listofmultiplesignatories[0]
    else:
        return signatories

def blgettimestampuserdetails (id, Signatories):
       
        """Get time stamp for each approver from hstory tables. It uses Routes table intially. but
        needs to change to check if there is routing table change"""
        
        # lstDictQueSeries = ActionItems.objects.filter(id=id).values('QueSeries')
        # currentQueSeries = lstDictQueSeries[0].get('QueSeries')
        currentQueSeries = blgetFieldValue(id,'QueSeries')
        #next get all history that has got to do with ID from history tables
        #thinking that if you order by decending then you are done by getting latest first
        lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=currentQueSeries).order_by('-history_date').values()
        filler= ''
        finallstoflst = [] 
        #get details from signatory as in signature, full name etc for all entries in the ActionRoutes                                  
        for index, items in enumerate(Signatories):
            #get each user detail first
            singlesignatory = blreplacemultiplesignatories (items[1],id,index)
            objuser = CustomUser.objects.filter(email=singlesignatory).values()
                  
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
        
        return finallstoflst

def blgetDiscSubOrgfromID (ID):
    """ This function just returns the company, disipline and sub (Triplet) for an object based on id of object in ActionItems
    Org was placed at the last because other existing functions use Disc and Sub first. The return is a triplet of 
    DiscSubOrg as a List """
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
    """This function sets the template which should be used for the pdf closeout report based on the number of approvers & the type of studies using forms method"""

    #20220119 edward formstudies
    discsuborg = blgetDiscSubOrgfromID(ID)
    ApproverLevel = int(blgetApproverLevel(discsuborg)) -1
    form_class = (blgetFieldValue(ID,"StudyName__Form"))

    if form_class :
        if ApproverLevel==5 or ApproverLevel == 7 :
            newcloseouttemplate = f'{closeouttemplate}{form_class}{ApproverLevel}{".pdf"}'
        else:
            newcloseouttemplate = f'{closeouttemplate}{form_class}{".pdf"}'  
    else: 
        if ApproverLevel==5 or ApproverLevel == 7 :
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

#20211201 edward remove discsuborg    
# def blgetIndiResponseCount2(discsuborg,queseriesopen,queseriesclosed,phase=""): #Guna 20210703 to be consolidated
def blgetIndiResponseCount2(dfdiscsuborgphase,queseriesopen,queseriesclosed,phase=""): #Guna 20210703 to be consolidated
    
    indiPendingSeries =[] #emptylist
    completePendingPair = [] #emptylist
    filler = 0

    #first loop through all routes disc/sub/org
    for itemtriplet in dfdiscsuborgphase:
        
        # totalopencount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesopen) 
        # totalclosedcount = blgetDiscSubOrgActionCount ('Y',itemtriplet,queseriesclosed)
        
        # gets open action dependiong on phase
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

                #edward 20211129 phase indi details
                pendingResponse = blphasegetDiscSubOrgActionCountQ (itemtriplet,lstindique,phase)

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
    """Pass a dictionary object from .values(...) and get the action stuck at data. This is done by gettings triplet 
    and then mapping against signatories and then using queseries to decifer in that route
    which signatory holds the actions. allactions passed in and modified directly and returned without making a copy of it. This will be the approach from here"""

    for items in allactions:

        lstoftriplet = blgetDiscSubOrgfromID (items['id']) 
        lstofActioneeAppr = blgetSignotories (lstoftriplet)

        if items['QueSeries'] != 99 and (lstofActioneeAppr !=[]):
             # basically its looks at que series and then matches it against the list of entire signatories above
            lststuckAt = lstofActioneeAppr[items['QueSeries']]#basically just uses QueSeries to tell us where its stuck at
            items['ActionAt'] = "/".join(lststuckAt)

            
        else:     
            items['ActionAt'] = "Closed"
        if lstofActioneeAppr :
            items['Actionee'] = lstofActioneeAppr[0][1]
          
    return allactions

#   edward 20210805 dictstuckat
# to have a generic function to pass in table headers for excel to call in views
def blgetActionStuckAtdict(allactions,email=False):
    """This function gets where each action is currently at in terms of Actionee or Approver"""

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
    """This function gets the List of Signatories from ActionRoutes Tables"""
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
def blcheckmultipleactionee (id,signatories,queseries):
    """Checks for multiple signatories for actionee . Basically it returns a single actionee from 
    history tables. Use the same logic as previous based on current queseries before it gets rejected"""
    
    filterkwargs = {'id':id, 'QueSeries': 1} 
    lstdictHistory = ActionItems.history.filter(**filterkwargs).select_related("history_user").order_by('-history_date')
    if queseries > 1:
            emailid = lstdictHistory[1].history_user.email
    else:
            emailid = lstdictHistory[0].history_user.email
    
    blmultisignareplace(signatories,emailid,"Actionee")
    

def blgetSignatoryemailbyquereject(lstdiscsuborg,queseries,id):
    
    pairSignatories = blgetSignotories(lstdiscsuborg) #just reusing what is already done 
    blcheckmultipleactionee (id, pairSignatories,queseries)
    
    #Logic for multiple actionee
    for items in pairSignatories:
        items.pop(0) # basically removes the Actionee, Approver from pair and maintains name
    abbrevatedemail=pairSignatories[:queseries] # returns only before queseries

    lstfinal = [''.join(ele) for ele in abbrevatedemail] #this is just list comprehensioin to return a list and not list of list
    
    
    return lstfinal

# edward 20210708 created new bl for signatory by queue 
def blgetSignatoryemailbyque(lstdiscsuborg,queseries):
    """This function gets the Signatories by email que & sends email notification to the next person in the que when Action is Submitted or Approved"""
    
    pairSignatories = blgetSignotories(lstdiscsuborg) #just reusing what is already done 
    
    for items in pairSignatories:
        items.pop(0) # basically removes the Actionee, Approver from pair and maintains name

    # sends email notification to the next person in queue
    abbrevatedemail=pairSignatories[queseries:queseries+1] 
    
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

def bldropduplicateandcount (queryset):
    
    """Accepts queryset and then uses data frames , pandas to drop_duplicate and count unique
    i.e the number of individual rows"""
    
    dfdata = pd.DataFrame(queryset)
    dataframeunique = dfdata.drop_duplicates()
    countofrows = len(dataframeunique.index)
    return countofrows
 

def blRejectedHistortyActionsbyId (useremail,queseries, Revision):
    """get rejected items from history table. Only accepts single queseries. Revision wise it accepts 
    revision gte (greater than) which means input can be 1 and it will filter for anything above 1.
    """
    #get user from email id since history tables use user ID
    lstUserSeries =  CustomUser.objects.filter(email=useremail).values()
    currentUserID = lstUserSeries[0].get('id')

    #get all history values from history tables first
    userrejectedhistory = ActionItems.history.filter(history_user_id=currentUserID).filter(
                            
                                Revision__gte=Revision).filter(QueSeries=queseries).order_by('-history_date').values('id')
    
    return userrejectedhistory
def blgetActionItemsbyid(dictofids):

    #Convert list of dictionaries into list
    listofids =[x['id']for x in dictofids]
    
    
    actionitemsbyid = ActionItems.objects.filter(id__in=dictofids).values(
        'id','StudyActionNo','StudyName__StudyName','Organisation','Disipline',
                    'Subdisipline', 'Cause', 'Recommendations','DueDate',
                    'InitialRisk','Revision'

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
    '''Pass routes in and it counts everything in your routes . the old way of doing it , should change to the new way
    '''
    
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
    "This function stops the rundown curve at todays date"
    
    strtoday = dt.today().strftime('%Y-%m-%d') #todays date as string
    today= dt.today()#.strftime('%Y-%m-%d') #todays date as date object

    # use this to append the actual data which is Total - Closed
    actual = (testtotal-testclosed) 
    
    currentdate = [today,' ',actual]

    for items in content:
        # convert from string to date object. datetime obj has problems bcs comparing down to the minute
        items[0] = datetime.datetime.strptime(items[0], '%Y-%m-%d').date() 

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





