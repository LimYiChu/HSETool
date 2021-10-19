#New Business logic to centralise the new Way with Q Object
from django.db.models import Q
from functools import reduce
import operator
from UploadExcel.models import ActionItems
from .models import *

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