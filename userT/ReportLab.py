import io
import pdfrw
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, SimpleDocTemplate
from reportlab.platypus.flowables import Flowable
from UploadExcel.models import *
from .models import *

def run():
    canvas_data = get_overlay_canvas()
    template_path='Sapura ATR Template.pdf'
    form = merge(canvas_data,template_path )
    save(form, filename='TestOutput.pdf') #this need to be looped and change name after each action.

def get_overlay_canvas() -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.setFont ("Helvetica",10)
    #drawstrings for non-box entries.
    #draw frames for boxes e.g. Cause, consequence etc.
    #required for frames
    flow_obj=[]
    textpdf =[]
    styles=getSampleStyleSheet()
    item=ActionItems.objects.all()
    #allfieldnames = ActionItems._meta.get_fields()
    #print (allfieldnames)
    print (item)
    #Study Action No
    for lineitem in item:
        

        textstudy = lineitem.StudyActionNo
        print(textstudy)
        flow_obj.append(Paragraph(textstudy,style=styles["Normal"]))
        framePlace=Frame(210,804,80,25, showBoundary=1)
        framePlace.addFromList(flow_obj,pdf)

        # framePlace=Frame(535,804,80,25, showBoundary=1)
        
        #     flow_obj.append(Paragraph(items,style=styles["Normal"]))
        #     framePlace=Frame(210,804,80,25, showBoundary=1)
        #     framePlace=Frame(535,804,80,25, showBoundary=1)
            
        # pdf.save()
        # data.seek(0)
        
       # textDate=str(attr.DueDate)
        # flow_obj.append(Paragraph(textDate,style=styles["Normal"]))
        # framePlace=Frame(535,804,80,25, showBoundary=1)
        # framePlace.addFromList(flow_obj,pdf)
      
    #Date 
    # for attr in item :  
    #    text=str(attr.DueDate)
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # framePlace=Frame(535,804,80,25, showBoundary=1)
    # framePlace.addFromList(flow_obj,pdf)
    #Workshops/Studies
    # for attr in item :
    #     text=str(attr.StudyName)
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameWorkshop=Frame(130,789,80,25, showBoundary=0)
    # frameWorkshop.addFromList(flow_obj,pdf)
    # #Cause Box
    # for attr in item :
    #     text=(attr.Cause)
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameCause=Frame(20,720,590,60, showBoundary=0)
    # frameCause.addFromList(flow_obj,pdf)
    # #consqeuence
    # for attr in item :
    #     text=(attr.Consequence)
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameConsequence=Frame(20,640,590,60, showBoundary=0)
    # frameConsequence.addFromList(flow_obj,pdf)
    # #Recommendations
    # for attr in item :
    #     text=(attr.Recommendations)
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameRecommendations=Frame(20,545,590,75, showBoundary=0)
    # frameRecommendations.addFromList(flow_obj,pdf)
    # #Action Response
    # for attr in item :
    #     text=attr.Response
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameActionResponse=Frame(20,390,590,130, showBoundary=0)
    # frameActionResponse.addFromList(flow_obj,pdf)
    # #Action Response
    # for attr in item :
    #     text=attr.Response
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameActionResponse=Frame(20,390,590,130, showBoundary=0)
    # frameActionResponse.addFromList(flow_obj,pdf)
    # #Future Actions
    # for attr in item :
    #     text=attr.FutureAction
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameFutureActions=Frame(20,105,590,50, showBoundary=0)
    # frameFutureActions.addFromList(flow_obj,pdf)
    # #DateResponded
    # text='''
    # DDMMYY
    # '''
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frameDate=Frame(510,520,80,25, showBoundary=0)
    # frameDate.addFromList(flow_obj,pdf)
    # #ActioneeName there is a problem here
    # item=ActionRoutes.objects.filter(pk__iexact=1)
    # for attr in item :  
    #     text=attr.Actionee 
    # p_text=Paragraph(text,style=styles["Normal"])
    # flow_obj.append(p_text)
    # frame=Frame(385,520,125,25, showBoundary=0)
    # frame.addFromList(flow_obj,pdf)

    pdf.save()
    data.seek(0)
    return data

def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form

def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())
if __name__ == '__main__':
    run()