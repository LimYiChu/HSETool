from .models import *
from UploadExcel.models import *
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

from django.conf import settings

def excelAllActions(lstAttributes,lstheaders,title,columremove=False):
    
    workbook = Workbook()       
    worksheet = workbook.active
    worksheet.title = title
    row_num = 1
    
    #formatting options
    ft = Font(bold=True)
    al = Alignment( wrap_text=True)
    bd = Border (bottom=Side(border_style="double", color='FF000000'))

    for col_numH, cell_valueH in enumerate(lstheaders,1):#that 1 just starts the index count at 1 which is required or openpyxl fails
        cell = worksheet.cell(row=row_num, column=col_numH)
        cell.value = cell_valueH
        #cell.style.alignment.wrap_text=True
        
        cell.font = ft
        cell.alignment = al
        cell.border = bd
        columnAlphapet = chr(ord('@')+col_numH) #just convert numbers to alphabet dont bother trying to figure it out
        worksheet.column_dimensions[columnAlphapet].width= 30 #- just flat out set the width for everything
    
    worksheet.row_dimensions[row_num].height= 30

    for lineitem in lstAttributes:
       
        row_num += 1
        
        for col_num, cell_value in enumerate(lineitem,1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            bd = Border (bottom=Side(border_style="thin", color='FF000000'))
            cell.alignment = al
            cell.border = bd
        
        worksheet.row_dimensions[row_num].height= 50
    if columremove:
        worksheet.delete_cols(columremove)
    return workbook

def createExcelReports(request,filename,**kwargs):
    
    allfields = [f.name for f in ActionItems._meta.get_fields()] 
    del allfields[0:2] # pop the first 2 in the list since it returns the foreign key
    
    allWorkshops = ActionItems.objects.all()
    
    #excel part - using from openpyxl import Workbook
    workbook = Workbook()       
    worksheet = workbook.active
    worksheet.title = 'Action Items'
            
    columns = allfields
    row_num = 1

    for col_num, column_title in enumerate(columns, 1): #just skips ID field in meta field , print allfields to see why
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = column_title
    row=[]

    for actions in allWorkshops:
           
            row_num += 1
            row=[]
            for field in allfields:
                    param = 'actions.'+ str(field)
                    row.append (eval(param))
                   
            for col_num, cell_value in enumerate(row, 1):
                    cell = worksheet.cell(row=row_num, column=col_num)
                    cell.value = cell_value

    
    #path = settings.MEDIA_ROOT     
    #workbook.save(path + filename)
    return workbook