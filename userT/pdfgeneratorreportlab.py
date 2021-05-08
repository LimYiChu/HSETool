import io
import pdfrw
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, SimpleDocTemplate
from UploadExcel.models import *
from .models import *

def run():
    canvas_data = get_overlay_canvas()
    template_path='Sapura ATR Template.pdf'
    form = merge(canvas_data,template_path )
    #item=ActionItems.objects.all()
    #for attr in item:
    #    i = attr.StudyActionNo # specify +1 for each file so it does not overwrite one file 
    #    print(i) 
     #   j = (i + '.pdf') 
    #    save(form, filename=j)
    save(form, filename='new.pdf') #this need to be looped and change name after each action.

def get_overlay_canvas() -> io.BytesIO: #first function, get data from models and place according to coordinates on a blank pdf
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.setFont ("Helvetica",10)
    flow_obj=[]
    styles=getSampleStyleSheet()
    item=ActionItems.objects.all()
    
    for attr in item:
        textstudy = attr.StudyActionNo
        #print(textstudy)
        flow_obj.append(Paragraph(textstudy,style=styles["Normal"])) # append parapgraph back into a list that is flow obj[]
        framePlace=Frame(210,804,80,25, showBoundary=0)
        framePlace.addFromList(flow_obj,pdf) #flow_obj is reset and emptied at this line
        
        textDate=str(attr.DueDate)
        flow_obj.append(Paragraph(textDate,style=styles["Normal"]))
        framePlace=Frame(535,804,80,25, showBoundary=0)
        framePlace.addFromList(flow_obj,pdf)
        
        textStudyName=str(attr.StudyName)
        flow_obj.append(Paragraph(textStudyName,style=styles["Normal"]))
        frameWorkshop=Frame(130,789,80,25, showBoundary=0)
        frameWorkshop.addFromList(flow_obj,pdf)

        textCause=(attr.Cause)
        flow_obj.append(Paragraph(textCause,style=styles["Normal"]))
        frameCause=Frame(20,720,590,60, showBoundary=0)
        frameCause.addFromList(flow_obj,pdf)

        textConsequence=(attr.Consequence)
        flow_obj.append(Paragraph(textConsequence,style=styles["Normal"]))
        frameConsequence=Frame(20,640,590,60, showBoundary=0)
        frameConsequence.addFromList(flow_obj,pdf)
        
        textRecommendations=(attr.Recommendations)
        flow_obj.append(Paragraph(textRecommendations,style=styles["Normal"]))
        frameRecommendations=Frame(20,545,575,75, showBoundary=1)
        frameRecommendations.addFromList(flow_obj,pdf)

        #textActionResponse=attr.Response
        #flow_obj.append(Paragraph(textActionResponse,style=styles["Normal"]))
        #frameActionResponse=Frame(20,390,590,130, showBoundary=0)
        #frameActionResponse.addFromList(flow_obj,pdf)

        textFutureAction=attr.FutureAction
        flow_obj.append(Paragraph(textFutureAction,style=styles["Normal"]))
        frameFutureActions=Frame(20,105,590,50, showBoundary=0)
        frameFutureActions.addFromList(flow_obj,pdf)

        pdf.showPage()
        
    pdf.save()
    data.seek(0)
    print(data)
    return data

def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO: #second function is to combine a predefined template & pdf from function no.1 
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form

def save(form: io.BytesIO, filename: str): #save combined file
    with open(filename, 'wb') as f:
        f.write(form.read())
if __name__ == '__main__':
    run() #  returns to top to start
