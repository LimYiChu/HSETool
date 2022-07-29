from dataclasses import dataclass
from distutils.log import info
from unittest import result
from django.http.response import JsonResponse
from django.shortcuts import render
from matplotlib import testing
from matplotlib.font_manager import json_dump

# from HSETool.userT.views import flatten
from itertools import groupby

from userT.views import actionlist
from .forms import *
from UploadExcel.forms import *
from .businesslogic import *
from .businesslogicQ import *
from .tableheader import *
from .excelReports import *
from .models import *
from UploadExcel.models import *
from .reports import *
import pandas as pd
from userT.pdfgenerator import *
from io import BytesIO
from UploadExcel.forms import *
from userT.parameters import *
from UploadExcel.formstudies import *
import re


def dynamictable(request, dynamictable=""):
    """
    This function gets the all the data for use by the googlecharts & datatables in the dynamictable pop out tab
    """
    raw_data = request.GET.get("data", None)
    dynamictable = request.GET.get("dynamictable", None)

    if dynamictable == 'dynamicdiscipline':
        data_split = re.split('\[|, |\'|\]', raw_data)
        data = [x for x in data_split if x!='']
    else:
        data = raw_data

    info = {'dynamicdiscipline': [{'Disipline': data[0], 'Subdisipline': data[1], 'Organisation': data[2]},
                                    ['id', 'StudyActionNo', 'QueSeries', 'DueDate', 'Disipline','Subdisipline', 'InitialRisk', 'Organisation', 'StudyName__StudyName'],
                                    ['Study Action No', 'Study Name', 'Due Date', 'Action At'],
                                    bldynamicstudiesactionformat],

            'dynamicstudies': [{'StudyName__StudyName': data}, 
                                ['id', 'StudyActionNo', 'QueSeries', 'DueDate', 'Disipline', 'Subdisipline', 'InitialRisk', 'Organisation','StudyName__StudyName'],
                                ['Study Action No', 'DueDate', 'Action At', 'Discipline', 'Initial Risk'],
                                bldynamicstudiesactionformat],
            'dynamicindisumm': [data, 
                                ['User', 'Role', 'Organisation Route', 'Pending Submission', 'Pending Approval', 'Closed', 'Open Actions'], 
                                indisumm_parameter,
                                bldynamicindisummactionformat]}

    headerlst = info[dynamictable][2]
    actions = info[dynamictable][3](info[dynamictable][0], info[dynamictable][1]) 
    dfall = pd.DataFrame.from_dict(actions)                          
    if dynamictable == 'dynamicindisumm':
        discheaderlst = None
        disclst = None
    else :
        dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation'] 
        discmultilist = bldynamicstudiesdisc(data,actions)    #YingYing change on 20220722
        # discmultilist = bldynamicstudiesdisc(actions) 　          
        discheaderlst = discmultilist[0]                            
        disclst = discmultilist[1]                                  
        dfdisc = pd.DataFrame(disclst)  
        dictheader = {0: 'Discipline', 1: 'Pending Submission', 2: 'Submitted', 3: 'Closed', 4: 'Open Actions', 5: 'Total Actions'} 
        dfdisc.rename(columns=dictheader,inplace=True) 
    
    dftablecolumns = {'dynamicstudies': dfstudiescolumns,
                    'dynamicdiscipline': dfdisciplinecolumns,
                    'dynamicindisumm': indisumm_parameter}
    dftablecolumns = dftablecolumns[dynamictable]
    dfalldynamictablesorted = blsortdataframes(dfall, dftablecolumns)
    dftablelst = dfalldynamictablesorted.values.tolist()

    chart = {'dynamicstudies': [bldynamicchart, bldynamicchartopen],
            'dynamicdiscipline': [bldynamicchart, bldynamicchartopen],
            'dynamicindisumm': [bldynamicindisummchart, bldynamicindisummpend]}
    openclose = chart[dynamictable][0](dfalldynamictablesorted)
    pending = chart[dynamictable][1](dfalldynamictablesorted)

    countclosed = openclose[0]                               
    countopen = openclose[1]                                   
    headeropenclose = ['\\\Status(Open/Closed):::', 'Number']
    openclose.insert(0,headeropenclose)                             
    multilst = [openclose, pending]  
                       
    context = {
            'multilst': multilst,
            'dflist': dftablelst,
            'headerlist': headerlst,
            'donutclose': countclosed,
            'donutopen': countopen,
            'dfstuckatlst': pending,
            'discheaderlst': discheaderlst,
            'disclst': disclst,
            'data': data
            }      

    return JsonResponse(context,status=200)
 

# def dynamicindisumm(request):
#     """
#     This function gets the all the data for use by the googlecharts & datatables in the dynamic individual pop out tab
#     """

#     data = request.GET.get("data", None)
#     dynamictable = request.GET.get("dynamictable", None)
#     filteredstring = data                                                                     
#     reducedfields = ['User','Role','Organisation Route','Pending Submission','Pending Approval','Closed','Open Actions']
#     headerlist = ['Role','Organisation Route','Pending Submission','Pending Approval','Closed','Open Actions']                               
#     actionsamount = bldynamicindisummactionformat(filteredstring,reducedfields)  
#     dfall = pd.DataFrame.from_dict(actionsamount)                                                                                             
#     dfalldynamicindisummsorted = blsortdataframes(dfall,indisumm_parameter)                                                
#     dfindisummlst = dfalldynamicindisummsorted.values.tolist()                                                            
#     lstofcount = bldynamicindisummchart(dfalldynamicindisummsorted)                                        
#     pendinglst = bldynamicindisummpend(dfalldynamicindisummsorted)  

#     countclosed = lstofcount[0]                               
#     countopen = lstofcount[1]                                   
#     headeropenclose = ['\\\Status(Open/Closed):::', 'Number']
#     lstofcount.insert(0,headeropenclose)                             
#     multilst = [lstofcount,pendinglst]

#     context =   {
#                 'multilst':multilst,
#                 'dflist': dfindisummlst,
#                 'headerlist' : headerlist,
#                 'donutclose' : countclosed,
#                 'donutopen' : countopen,
#                 'dfstuckatlst':pendinglst,
#                 'data':data,
#                 }
    
#     return JsonResponse(context,status=200)


# def dynamicstudies(request):
#     """
#     This function gets the all the data for use by the googlecharts & datatables in the dynamic studies pop out tab
#     """
#     dyanamictable = request.GET.get("dynamictable", None)
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        
#         data = request.GET.get("data", None)                                                                                
#         filteredstring = {'StudyName__StudyName': data}                                                                     
#         reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation']  
#         headerlst = ['Study Action No', 'DueDate' ,'Action At','Discipline','Initial Risk']                                
        
#         actionsstuckat = bldynamicstudiesactionformat(filteredstring,reducedfields)  

#         dfall = pd.DataFrame.from_dict(actionsstuckat)                                                                      
#         dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation']                          
#         dfalldynamicstudiessorted = blsortdataframes(dfall,dfstudiescolumns)                                                
#         dfstudieslst = dfalldynamicstudiessorted.values.tolist()                                                            
        
#         lstofcount = bldynamicchart(dfalldynamicstudiessorted)     
#         countclosed = lstofcount[0]                               
#         countopen = lstofcount[1]                                   
#         dfstuckatlst=bldynamicchartopen(dfalldynamicstudiessorted)  
#         headeropenclose = ['\\\Status:::', 'Number']
#         lstofcount.insert(0,headeropenclose)                            
#         multilst = [lstofcount,dfstuckatlst]                        
#         discmultilist = bldynamicstudiesdisc(actionsstuckat)
#         discheaderlst = discmultilist[0]                            
#         disclst = discmultilist[1]                                  
#         dfdisc = pd.DataFrame(disclst)                             
#         dictheader = {0:'Discipline',1:'Pending Submission',2:'Submitted',3:'Closed',4:'Open Actions',5:'Total Actions'} 
#         dfdisc.rename(columns=dictheader,inplace=True)               

#         context = {
#         'multilst':multilst,
#         'dflist':dfstudieslst,
#         'headerlist' : headerlst,
#         'donutclose' : countclosed,
#         'donutopen' : countopen,
#         'dfstuckatlst':dfstuckatlst,
#         'discheaderlst':discheaderlst,
#         'disclst':disclst,
#         'data':data
#         }


#         return JsonResponse(context,status=200)
#     else:
#         return render(request, 'userT/incldynamicstudies.html')


# def dynamicdiscipline(request):
#     """
#     This function gets the all the data for use by the googlecharts & datatables in the dynamic discipline pop out tab
#     """
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        
#         data = request.GET.get("data", None)
#         discsuborglst = bldiscstrmatch(data)
#         filteredstring = {'Disipline':discsuborglst[0],'Subdisipline':discsuborglst[1],'Organisation':discsuborglst[2]}
#         reducedfields=['id','StudyActionNo','QueSeries','DueDate','Disipline','Subdisipline','InitialRisk','Organisation','StudyName__StudyName']
#         headerlist = ['Study Action No', 'Study Name' ,'Due Date','Action At' ]
        
#         actionsbydisc = blgetsinglefilteractionsitemsQ(filteredstring,reducedfields) 
#         dfalllist = blgetdictActionStuckAt(actionsbydisc) # getting a list of everything
#         dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
       
#         dfalldynamicdisciplinesorted = blsortdataframes(dfall,dfdisciplinecolumns) # sort dfall  
#         dfdisclist =  dfalldynamicdisciplinesorted.values.tolist()

#         lstofcount = bldynamicchart(dfalldynamicdisciplinesorted)
#         countclosed = lstofcount[0]
#         countopen = lstofcount[1]
#         dfstuckatlst=bldynamicchartopen(dfalldynamicdisciplinesorted)
#         headeropenclose = ['\\\Status:::', 'Number']
#         lstofcount.insert(0,headeropenclose)  
#         multilst = [lstofcount,dfstuckatlst]
#         discmultilist = bldynamicstudiesdisc(actionsbydisc)
#         discheaderlst = discmultilist[0]
#         disclst = discmultilist[1]

#         context = {
#                     'multilst':multilst,
#                     'dflist':dfdisclist,
#                     'headerlist' : headerlist,
#                     'donutclose' : countclosed,
#                     'donutopen' : countopen,
#                     'dfstuckatlst':dfstuckatlst,
#                     'discheaderlst':discheaderlst,
#                     'disclst':disclst,
#                     'data' : data
#                     }
     
#         return JsonResponse(context,status=200)
#     else:
#         return render(request, 'userT/incldynamicdiscipline.html')


def dynamicindisummexcel(request,user=""):
    """
    This function download the excel of dynamic individual details from pop out table.
    """
    filteredstring = user                                                                     
    reducedfields = ['User','Role', 'Organisation Route', 'Pending Submission', 'Pending Approval', 'Closed', 'Open Actions']
    headerlist = ['Role', 'Organisation Route', 'Pending Submission', 'Pending Approval', 'Closed', 'Open Actions']                               
    actionsamount = bldynamicindisummactionformat(filteredstring, reducedfields)  
    dfall = pd.DataFrame(actionsamount)
    dfall.pop('User')
    dictheader = {0: 'Role', 1: 'Organisation Route', 2: 'Pending Submission', 3: 'Pending Approval', 4: 'Closed', 5: 'Open Actions'}
    dfall.rename(columns=dictheader, inplace=True)
    usersheetname = user[:31]

    in_memory = BytesIO()
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=IndividualSummary.xlsx'
    with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        dfall.to_excel(writer, sheet_name=usersheetname, engine='xlsxwriter', header=None, startrow=1)
        workbook = writer.book #gives excelwriter access to workbook
        worksheet = writer.sheets[usersheetname] #gives excelwriter access to worksheet
        formattedexcel = blexcelformat(dfall, workbook, worksheet)    
    in_memory.seek(0)
    response.write(in_memory.read())
    return response


def dynamicstudiesexcel(request,study=""):
    """
    This function gets the all the data for use by the googlecharts & datatables in the dynamic studies pop out tab
    """
    filteredstring = {'StudyName__StudyName': study}
    reducedfields = ['id', 'StudyActionNo', 'QueSeries', 'DueDate', 'Disipline', 'Subdisipline', 'InitialRisk', 'Organisation']
    actionsstuckat = bldynamicstudiesactionformat(filteredstring, reducedfields)
    dfall = pd.DataFrame.from_dict(actionsstuckat)                                                                      
    dfall['discsuborg']=dfall['Disipline']+'/'+dfall['Subdisipline']+'/'+dfall['Organisation']                          
    dfalldynamicstudiessorted = blsortdataframes(dfall, dfstudiescolumns) 
    dfalldynamicstudiessorted.pop("id")
    # dfalldynamicstudiessorted = dfalldynamicstudiessorted.iloc[:, :-1]
    dictheader = {'StudyActionNo': 'Study Action No', 'DueDate': 'Due Date', 'ActionAt': 'Action At', 'discsuborg': 'Discipline', 'InitialRisk': 'Initial Risk', 'RiskColour': 'Risk Colour'}
    dfalldynamicstudiessorted.rename(columns=dictheader, inplace=True)
    studysheetname = study[:31]

    in_memory = BytesIO()
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=DetailsStudies.xlsx'
    with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        dfalldynamicstudiessorted.to_excel(writer, sheet_name=studysheetname, engine='xlsxwriter', header = None, startrow=1)
        workbook = writer.book #gives excelwriter access to workbook
        worksheet = writer.sheets[studysheetname] #gives excelwriter access to worksheet
        formattedexcel = blexcelformat(dfalldynamicstudiessorted, workbook, worksheet)    
    in_memory.seek(0)
    response.write(in_memory.read())
    return response


def dynamicstudiesdiscexcel(request,study=""):
    """
    This function download the excel of discipline summary from pop out table in Studies/Workshops tab.
    """
    filteredstring = {'StudyName__StudyName': study}
    reducedfields=['id', 'StudyActionNo', 'QueSeries', 'DueDate', 'Disipline', 'Subdisipline', 'InitialRisk', 'Organisation']
    actionsstuckat = bldynamicstudiesactionformat(filteredstring, reducedfields)
    # discmultilist = bldynamicstudiesdisc(actionsstuckat)
    discmultilist = bldynamicstudiesdisc(study,actionsstuckat)    #YingYing change on 20220722
    disclst = discmultilist[1]
    dfdisc = pd.DataFrame(disclst)
    dictheader = {0: 'Discipline', 1: 'Pending Submission', 2: 'Submitted', 3: 'Closed', 4: 'Open Actions', 5: 'Total Actions'}
    dfdisc.rename(columns=dictheader, inplace=True)
    studydiscsheetname = study[:31]

    in_memory = BytesIO()
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=DisciplinebyStudies.xlsx'
    with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        dfdisc.to_excel(writer, sheet_name=studydiscsheetname, engine='xlsxwriter', header = None, startrow=1)
        workbook = writer.book #gives excelwriter access to workbook
        worksheet = writer.sheets[studydiscsheetname] #gives excelwriter access to worksheet
        formattedexcel = blexcelformat(dfdisc, workbook, worksheet)    
    in_memory.seek(0)
    response.write(in_memory.read())
    return response


def dynamicdisciplineexcel(request,discipline = ""):
    """
    This function download the excel of discipline from pop out table in Discipline tab.
    """ 
    discsuborglst = bldiscstrmatch(discipline)
    filteredstring = {'Disipline': discsuborglst[0], 'Subdisipline': discsuborglst[1], 'Organisation': discsuborglst[2]}
    reducedfields=['id', 'StudyActionNo', 'QueSeries', 'DueDate', 'Disipline', 'Subdisipline', 'InitialRisk', 'Organisation', 'StudyName__StudyName']
    actionsbydisc = blgetsinglefilteractionsitemsQ(filteredstring, reducedfields) 
    dfalllist = blgetdictActionStuckAt(actionsbydisc) # getting a list of everything
    dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
    dfalldynamicdisciplinesorted = blsortdataframes(dfall, dfdisciplinecolumns)
    dfalldynamicdisciplinesorted = dfalldynamicdisciplinesorted.iloc[: , :-2]
    dictheader = {'StudyActionNo': 'Study Action No', 'StudyName__StudyName': 'Study Name', 'DueDate': 'Due Date', 'ActionAt': 'Action At'}
    dfalldynamicdisciplinesorted.rename(columns=dictheader, inplace=True)
    dissubname = discsuborglst[0]+'-'+discsuborglst[1]
    dissubname = dissubname.replace('/','-')
    dissubnamesheetname = dissubname[:31]

    in_memory = BytesIO()
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=Discipline.xlsx'
    with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
        dfalldynamicdisciplinesorted.to_excel(writer, sheet_name=dissubnamesheetname, engine='xlsxwriter', header = None, startrow=1)
        workbook = writer.book #gives excelwriter access to workbook
        worksheet = writer.sheets[dissubnamesheetname] #gives excelwriter access to worksheet
        formattedexcel = blexcelformat(dfalldynamicdisciplinesorted, workbook, worksheet)    
    in_memory.seek(0)
    response.write(in_memory.read())
    return response