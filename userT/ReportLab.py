import io
import pdfrw
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, SimpleDocTemplate
from reportlab.platypus.flowables import Flowable
from UploadExcel.models import ActionItems




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
    #pdf.drawString(x=376, y=447, text='') #21 #710 #psd is 10 pts(Y-AXIS) starting from bottom of P , Y IS INVERTED START FROM TOP 0, whole page is 840 on y measured using point in pdf(pixel)
    
    #draw frames for boxes e.g. Cause, consequence etc.
    
    #required for frames

    flow_obj=[]
    styles=getSampleStyleSheet()
    
    #Study Action No
    x=ActionItems.objects.filter(pk__iexact=20)
    y=x.values('StudyActionNo')
    text=y
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameStudyActionNo=Frame(210,804,80,25, showBoundary=0)
    frameStudyActionNo.addFromList(flow_obj,pdf)

    #Date 
    text='''
    DDMMYYYY
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameDate=Frame(535,804,80,25, showBoundary=0)
    frameDate.addFromList(flow_obj,pdf)
    
    #Workshops/Studies
    text='''
    CRA/ HAZID
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameWorkshop=Frame(130,789,80,25, showBoundary=0)
    frameWorkshop.addFromList(flow_obj,pdf)

     #Cause Box
    text='''
    HUC1
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameCause=Frame(400,520,80,25, showBoundary=0)
    frameCause.addFromList(flow_obj,pdf)

     #Cause Box
    text='''
    DDMMYY
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameCause2=Frame(510,520,80,25, showBoundary=0)
    frameCause2.addFromList(flow_obj,pdf)

    #Cause Box
    text='''
    Cause ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    very long cause ------------------------------------
    too long the cause
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameCause3=Frame(20,720,590,60, showBoundary=0)
    frameCause3.addFromList(flow_obj,pdf)
   
    #consqeuence
   
    text='''
    this time its a very long consequence.................equence...........this time its a very long consequence..........................................................................................................................................................................................this time its a very long consequence....................this time its a very long consequence............................................................................................................................................................................................................................................................. 
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameConsequence=Frame(20,640,590,60, showBoundary=0)
    frameConsequence.addFromList(flow_obj,pdf)
    
    #Recommendations
    text='''
    Long Recommendations
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameRecommendations=Frame(20,545,590,75, showBoundary=0)
    frameRecommendations.addFromList(flow_obj,pdf)
    
    #Action Response
    text='''
    Yet another long responses
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameActionResponse=Frame(20,390,590,130, showBoundary=0)
    frameActionResponse.addFromList(flow_obj,pdf)
    
 
    #Future Actions
    text='''
    Future Actions here
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameFutureActions=Frame(20,105,590,50, showBoundary=0)
    frameFutureActions.addFromList(flow_obj,pdf)

    #Attachments
    text='''
    Total 5 attachments
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameAttachments=Frame(20,44,590,45, showBoundary=0)
    frameAttachments.addFromList(flow_obj,pdf)

    #Approver 1
    text='''
    Approver 1
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameApprover1=Frame(20,350,150,25, showBoundary=0)
    frameApprover1.addFromList(flow_obj,pdf)

    #Approver 1 Signature
    text='''
    Name (Position); DDMMYYYY XXYYY
    '''
    p_text=Paragraph(text,style=styles["Normal"])
    flow_obj.append(p_text)
    frameApprover1Sig=Frame(200,350,400,25, showBoundary=0)
    frameApprover1Sig.addFromList(flow_obj,pdf)

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