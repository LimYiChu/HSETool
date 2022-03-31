#New Business logic to centralise the new Way with Q Object
from django.db.models import Q
from functools import reduce
import operator
from UploadExcel.models import ActionItems
from .models import *

def blgetsinglefilteractionsitemsQ(dictfilter,reducedfields):

    QObjectfilter =Q(**dictfilter)
    filteredactions =  ActionItems.mdlallActionItemsCount.mgr_GeneralItemsFiltersKwargsQReduced(QObjectfilter,reducedfields)

    return filteredactions

#20211221 em get the rejected count for Actionee
def blActioneerejectedcountQ(Actionee_R):
    """This function gets the count of rejected actions from Action Items table by going through Action Routes of Actionee."""
    revision = 1
    routes = Actionee_R
    count=0
    if routes :
        QObjectSeries =[]
        for x, item in enumerate(routes):
            organisation   = item.Organisation
            discipline  = item.Disipline
            subdiscipline  = item.Subdisipline
            QObjectSeries.append(Q(**{'Disipline':discipline, 'Subdisipline': subdiscipline, 
                                'Organisation': organisation,'Revision__gte':revision }))

        filters = reduce(operator.or_,QObjectSeries)
        count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(filters)
        
    
    return count

#20211220 em get the rejected actions count PMT Reporting
def blnewgetrejecteditemsQ(dfdiscsuborg,revision,phase,reducedfields):
    """This function gets the Action Items that were rejected from Action Items table for PMT Reporting """
    count = 0  
    TotalQue = [0,1,2,3,4,5,6,7,8,9,99]
    QObjectMiscAND =Q()
    
    if phase!="":
        QObjectMiscAND = Q(**{'Disipline':dfdiscsuborg[0], 'Subdisipline': dfdiscsuborg[1], 'Organisation': dfdiscsuborg[2],
                        'ProjectPhase__ProjectPhase':phase,'Revision__gte':revision})
    else:
        QObjectMiscAND = Q(**{'Disipline':dfdiscsuborg[0], 'Subdisipline': dfdiscsuborg[1],
                        'Organisation': dfdiscsuborg[2],'Revision__gte':revision })

    #filters = blQobjectQueSeries(TotalQue) & QObjectMiscAND
    RejectedActions =  ActionItems.mdlallActionItemsCount.mgr_GeneralItemsFiltersKwargsQReduced(QObjectMiscAND,reducedfields)
    return RejectedActions

#20211220 edward get the rejected Actions count PMT Reporting
def blnewgetrejecteditemsQcount(dfdiscsuborg,revision,phase):
    """This function gets the count of rejected actions from Action Items table for PMT Reporting """
    count = 0  
    TotalQue = [0,1,2,3,4,5,6,7,8,9,99]
    QObjectMiscAND =Q()
    
    if phase!="":
        QObjectMiscAND = Q(**{'Disipline':dfdiscsuborg[0], 'Subdisipline': dfdiscsuborg[1], 'Organisation': dfdiscsuborg[2],
                        'ProjectPhase__ProjectPhase':phase,'Revision__gte':revision})
    else:
        QObjectMiscAND = Q(**{'Disipline':dfdiscsuborg[0], 'Subdisipline': dfdiscsuborg[1],
                        'Organisation': dfdiscsuborg[2],'Revision__gte':revision })

    filters = blQobjectQueSeries(TotalQue) & QObjectMiscAND
    count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(QObjectMiscAND)
    
    return count

#20211203 edward 
def blphasegetStudyreducedfieldsQ(reducedfields,phase=""):
    """This function only looks through the Studies table. It filters studies by phase only in the Studies table.If phase is empty it retrives all studies. Reduced field parameter  
    is used to return less data to html. Pass in list for reduced field e.g ['id','DueDate', 'QueSeries' etc]
    .It uses QObject"""
    count = 0
    dictofQueSeries ={}
    QObjectSeries = []
    filterargs = Q()
    QObjectMiscAND =Q()
   
    if phase != "":
        QObjectMiscAND = (Q(**{'ProjectPhase__ProjectPhase':phase}))
      
    #filters = blQobjectQueSeries(que) & QObjectMiscAND
    filters = QObjectMiscAND
    StudiesPhase =  Studies.mdlallStudies.mgr_GeneralItemsFiltersKwargsQReduced(filters,reducedfields)
    
    return StudiesPhase
#20211203 edward 

def blallactionscomdissubQ(routes,queseries,reducedfields):
    '''Uses Q object for more efficient queries. Pass in routes from actinee or approver.
    routes is a list of routes defined when user logs in. 
    This function then loops through all routes that logged in user holds actions based on que series
    Addtionally Pass in reduced fields so it does not retrieve all values() and limits the data transfer . 
    '''
    allactions = []
    
    if routes :
        QObjectSeries =[]
        for x, item in enumerate(routes):
            organisation   = item.Organisation
            discipline  = item.Disipline
            subdiscipline  = item.Subdisipline

            QObjectSeries.append(Q(**{'Disipline':discipline, 'Subdisipline': subdiscipline, 
                                'Organisation': organisation, 'QueSeries' : queseries}))
        filters = reduce(operator.or_,QObjectSeries)
        allactions = ActionItems.mdlallActionItemsCount.mgr_GeneralItemsFiltersKwargsQReduced(filters,reducedfields)

    return allactions

def blActionCountbyStudiesStreamQ(contextRoutes,studies,que):
    '''Need to change this to q object '''
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

def blfuncActionCountQ(routes,que=[]):
    '''Pass routes in and it counts everything in your routes . 
    '''
    count=0
    allstreams = []
    QObjectSeries =[]
    if routes: 
        for x, item in enumerate(routes):
            organisation   = item.Organisation
            discipline  = item.Disipline
            subdiscipline  = item.Subdisipline
            QObjectSeries.append(Q(**{'Disipline':discipline, 'Subdisipline': subdiscipline, 
                                'Organisation': organisation, })& blQobjectQueSeries(que) )

            #filters = blQobjectQueSeries(que) & QObjectMiscAND
        ORQobjroutes = reduce(operator.or_,QObjectSeries)
        count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(ORQobjroutes)
    
    return count

def blQobjectQueSeries (queseries):
    '''Passes the QSeries item and makes it into OR call. Insteaed of multiple select  statment for each Que Series 
    the Q object strings multiple OR object'''

    QObjectSeries = []
    for eachQ in queseries:
        QObjectSeries.append(Q(**{'QueSeries' :eachQ}))
    
    ORQueSeries = reduce(operator.or_,QObjectSeries)

    return ORQueSeries
def blphasegetDiscSubOrgActionCountQ(discsuborg,quelist,phase=""):
    '''Uses DiscSubOrg, and a list of QueSeries and phase to return a count based on phase
    It uses Q Object for optimisation'''
    count = 0   
    
    QObjectMiscAND =Q()
    
    if phase!="":
        QObjectMiscAND = Q(**{'Disipline':discsuborg[0], 'Subdisipline': discsuborg[1], 'Organisation': discsuborg[2],
                        'ProjectPhase__ProjectPhase':phase})
    else:
        QObjectMiscAND = Q(**{'Disipline':discsuborg[0], 'Subdisipline': discsuborg[1],
                        'Organisation': discsuborg[2] })

    filters = blQobjectQueSeries(quelist) & QObjectMiscAND
    count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(filters)
    
    return count
    
def blallphasegetAction(que,phase=""):
    '''this function gets all actions and or phases . Pass phase and QueSeries to get count 
    of items in a list of QueSeries[open,closed etc]'''
    count = 0
    dictofQueSeries ={}
    QObjectSeries = []
    filterargs = Q()
    QObjectMiscAND =Q()
   
    if phase != "":
        QObjectMiscAND = (Q(**{'ProjectPhase__ProjectPhase':phase}))
      
    filters = blQobjectQueSeries(que) & QObjectMiscAND
    count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(filters)

    return count
def blphasegetActionreducedfieldsQ(reducedfields,phase=""):
    '''Filters actions by phase.If phase is empty it retrives all actions. Reduced field parameter  
    is used to return less data to html. Pass in list for reduced field e.g ['id','DueDate', 'QueSeries' etc]
    .It uses QObject'''
    count = 0
    dictofQueSeries ={}
    QObjectSeries = []
    filterargs = Q()
    QObjectMiscAND =Q()
   
    if phase != "":
        QObjectMiscAND = (Q(**{'ProjectPhase__ProjectPhase':phase}))
      
    #filters = blQobjectQueSeries(que) & QObjectMiscAND
    filters = QObjectMiscAND
    ActionsPhase =  ActionItems.mdlallActionItemsCount.mgr_GeneralItemsFiltersKwargsQReduced(filters,reducedfields)

    return ActionsPhase

def blphasegetrejectedactionsQ(revision,queseries,reducedfields,phase="",):
    '''this function gets all actions and or phases . Pass phase and only fields you want , this way returned data is less 
    and q series is not required as a filter just returns everything'''
    
    QObjectMiscAND =Q()
   
   #,{'Revision__gte':revision},
    if phase != "":
        QObjectMiscAND =    Q(**{'QueSeries':queseries,'Revision__gte':revision,'ProjectPhase__ProjectPhase':phase})
    else :
        QObjectMiscAND =    Q(**{'QueSeries':queseries,'Revision__gte':revision})
    #filters = blQobjectQueSeries(que) & QObjectMiscAND
    
    ActionsPhase =  ActionItems.mdlallActionItemsCount.mgr_GeneralItemsFiltersKwargsQReduced(QObjectMiscAND,reducedfields)
    
    return ActionsPhase

def blgetCompanyActionCountPhase(company,quelist,phase="") :

    count = 0

    QObjectMiscAND =Q()
    
    if phase!="":
        QObjectMiscAND = (Q(**{'Organisation':company,'ProjectPhase__ProjectPhase':phase}))
        #filters = {'Organisation':company, 'ProjectPhase__ProjectPhase':phase}
    else:
        QObjectMiscAND = (Q(**{'Organisation':company}))
        #filters = {'Organisation':company}

    filters = blQobjectQueSeries(quelist) & QObjectMiscAND
    count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(filters)

    return count

def blgetDiscSubActionCountPhase(discsuborg,quelist,phase=""):
    '''function for getting discipline open action count by phases. if phase is
     empty will just omit phase filter. USes Q Object for optimisation'''
    
    count = 0   
    
    QObjectMiscAND =Q()
    
    if phase!="":
        QObjectMiscAND = Q(**{'Disipline':discsuborg[0], 'Subdisipline': discsuborg[1], 
                        'ProjectPhase__ProjectPhase':phase})
    else:
        QObjectMiscAND = Q(**{'Disipline':discsuborg[0], 'Subdisipline': discsuborg[1],
                        })

    filters = blQobjectQueSeries(quelist) & QObjectMiscAND
    count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(filters)

   
    return count

def blallActionCountbyStudiesPhaseQ(studies,quelist,phase=""):
    '''Pass in StudyName and Que series list and phase to get count. If phase is empty it will search for all phases
    Uses Q Object For Optimisation'''
    count = 0
    QObjectMiscAND =Q()
   
    if phase!="":
        QObjectMiscAND =Q(**{'StudyName__StudyName':studies,'ProjectPhase__ProjectPhase':phase})
    else:
        QObjectMiscAND =Q(**{'StudyName__StudyName':studies})
    
    
    filters = blQobjectQueSeries(quelist) & QObjectMiscAND
    count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFiltersKwargsQ(filters)

   
    return count