import pdfrw
from reportlab.pdfgen import canvas
import io
# 20211122 edward stitchingpdf
from pdfrw import PdfWriter,PdfReader,PdfName
import os
from .businesslogic import *

def pdfgenerate(input_pdf_path, output_pdf_path, data_dict,signatories):
    """ 
    This function gets the data from the Action Items + Signatories in the form of data dictionary & prints them onto the form fields in the pdf template
    This is primarily used for closeoutsheets once the Action is closed
    """
    template_pdf = pdfrw.PdfReader(input_pdf_path) # Read Input PDF
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))# Set Appearences ( Make Text field visible )
    # Loop all Annotations (edward added another for loop to print on all pages)
    for page in template_pdf.pages: #[0]['/Annots']:#loop over all pages in pdf, and for each page, loop over all ediatble fields called annots, for each page all annotations stored in 'Annots/' 
        annotations=page['/Annots']
        for annotation in annotations:
            if annotation['/Subtype'] == '/Widget' and annotation['/T']:  # all key names for each field stored in'/T'
                key = annotation['/T'][1:-1] # Remove parentheses
                if key in data_dict.keys():
                    annotation.update( pdfrw.PdfDict(V=f'{data_dict[key]}')) #takes the data from models with [key], printing key returns all key field from models (along with pdf details such as font type,etc)
                if key in signatories.keys():
                    annotation.update( pdfrw.PdfDict(V=f'{signatories[key]}'))
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def pdfsendtoclient(input_pdf_path, data_dict):
    """ 
    This function gets the data from the Action Items in the form of data dictionary & prints them onto the form fields in the pdf template
    This is primarily used for the Generate PDF function in pmtrepviewall page
    """
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    
    template_pdf = pdfrw.PdfReader(input_pdf_path) # Read Input PDF
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))# Set Appearences ( Make Text field visible )
    # Loop all Annotations (edward added another for loop to print on all pages)
    for page in template_pdf.pages: #[0]['/Annots']:#loop over all pages in pdf, and for each page, loop over all ediatble fields called annots, for each page all annotations stored in 'Annots/' 
        annotations=page['/Annots']
        for annotation in annotations:
            if annotation['/Subtype'] == '/Widget' and annotation['/T']:  # all key names for each field stored in'/T'
                key = annotation['/T'][1:-1] # Remove parentheses
                if key in data_dict.keys():
                    page = annotation.update( pdfrw.PdfDict(V=f'{data_dict[key]}')) #takes the data from models with [key], printing key returns all key field from models (along with pdf details such as font type,etc)
        
    pdfrw.PdfWriter().write(buffer, template_pdf)
    buffer.seek(0)

    return buffer          
    # 
    # pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

#20211122 edward stitchpdf
def pdfcloseoutwithattachments(objactionitemsfk):
    """
    This Function generates all the closeout reports with attachments into a single folder. 
    It starts by getting all the actions that are closed (passed in as Que Series = 99 from (objactionitemsfk) & prints each of them into each corresponding closeoutsheet & puts all of them into a folder.
    It then also  gets the attachment for each Action from the media folder & attaches the Action Item name in front of the attachments filename & then puts all of them into the folder that contains the closeoutsheets (refer to the above line) .
    """
    for items in objactionitemsfk: #objactionitems

        #This section to be deleted once confirmed start
        # closed = (items['QueSeries'] == 99) 
        # closed = True
        # if closed == True :
        # This section to be deleted once confirmed end

        #The following snippet gets all the actions that are closed (passed in as Que Series = 99 from (objactionitemsfk) & prints each of them into each corresponding closeoutsheet & puts all of them into a folder)
        items['StudyActionNo'] = items['StudyActionNo'].replace("/","_")
        newcloseouttemplate = blsetcloseouttemplate (items['id'])
        data_dict=items
        discsub = blgetDiscSubOrgfromID(items['id']) 
        Signatories = blgetSignotories(discsub) 
        lstSignatoriesTimeStamp= blgettimestampuserdetails (items['id'], Signatories) 
        studyactno = items["StudyActionNo"] # i renamed to studyactno
        studyactnopdf = (studyactno + '.pdf')
        signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp)
        out_file = os.path.join("static/test/",studyactnopdf)
        file = pdfgenerate(newcloseouttemplate,out_file,data_dict,signatoriesdict)
        objFk =ActionItems.objects.get(id = items['id']) 
        ObjAttach = objFk.attachments_set.all()
        
        # The following snippet gets the attachment for each Action from the media folder & attaches the Action Item name in front of the attachments filename & then puts it into the folder that contains the closeoutsheets
        for eachfile in ObjAttach: 
            filename = os.path.basename(eachfile.Attachment.name)
            attachmentorigin= bulkdlattachments + filename
            attachment_name = studyactno + "_" + filename
            shutil.copy(attachmentorigin ,"static/test/" + attachment_name)

    pdfpath = "static/test/"

    return pdfpath
    
# 20211122 edward stitchingpdf
def stitchingpdf(pdf_list_onlypdf,pdfpath):

    """
    Keeps the PDF AcroNodes intact while looping over all the PDFs that are generated
    This is a temporary solution until we move to Adobe PDF API .
    
    """
    output = PdfWriter()
    num = 0
    output_acroform = None
    for pdf in pdf_list_onlypdf:
        fullpath = os.path.join(pdfpath,pdf)
        input = PdfReader(fullpath,verbose=False)
        output.addpages(input.pages)
        if PdfName('AcroForm') in input[PdfName('Root')].keys():  # Not all PDFs have an AcroForm node
            source_acroform = input[PdfName('Root')][PdfName('AcroForm')]
            if PdfName('Fields') in source_acroform:
                output_formfields = source_acroform[PdfName('Fields')]
            else:
                output_formfields = []
            num2 = 0
            for form_field in output_formfields:
                key = PdfName('T')
                old_name = form_field[key].replace('(','').replace(')','')  # Field names are in the "(name)" format
                form_field[key] = 'FILE_{n}_FIELD_{m}_{on}'.format(n=num, m=num2, on=old_name)
                num2 += 1
            if output_acroform == None:
                # copy the first AcroForm node
                output_acroform = source_acroform
            else:
                for key in source_acroform.keys():
                    acroform_key = output_acroform[key]
                    # Add new AcroForms keys if output_acroform already existing
                    if key not in output_acroform:
                        output_acroform[key] = source_acroform[key]
                # Add missing font entries in /DR node of source file
                if (PdfName('DR') in source_acroform.keys()) and (PdfName('Font') in source_acroform[PdfName('DR')].keys()):
                    #if PdfName('Font') not in output_acroform[PdfName('DR')].keys():
                        # if output_acroform is missing entirely the /Font node under an existing /DR, simply add it
                    output_acroform[PdfName('DR')][PdfName('Font')] = source_acroform[PdfName('DR')][PdfName('Font')]
                # else:
                ## COMMENTED THIS OUT BUT DO NOT REMOVE, client uploading attachment with acro form nodes not printed to pdf which has adverse effects on the keys (eg : pdf files not printed & in editable form)
                #         # else add new fonts only
                #     for font_key in source_acroform[PdfName('DR')][PdfName('Font')].keys():
                #             if font_key not in output_acroform[PdfName('DR')][PdfName('Font')]:
                #                 output_acroform[PdfName('DR')][PdfName('Font')][font_key] = source_acroform[PdfName('DR')][PdfName('Font')][font_key]
            if PdfName('Fields') not in output_acroform:
                output_acroform[PdfName('Fields')] = output_formfields[PdfName('Fields')]
            else:
                # Add new fields
                output_formfields
        num +=1
    output.trailer[PdfName('Root')][PdfName('AcroForm')] = output_acroform
    final_output = output.write("static/test/mergepdffolder/testingmerge.pdf")

    return final_output



# def pdfgenerate(input_pdf_path, output_pdf_path, data_dict):
#     template_pdf = pdfrw.PdfReader(input_pdf_path) # Read Input PDF
#     template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))# Set Apparences ( Make Text field visible )
#     # Loop all Annotations
#     for annotation in template_pdf.pages[0]['/Annots']:#loop over all pages in pdf, and for each page, loop over all ediatble fields called annots, for each page all annotations stored in 'Annots/' 
#         print(annotation)
#         if annotation['/Subtype'] == '/Widget' and annotation['/T']:  # all key names for each field stored in'/T'
#             key = annotation['/T'][1:-1] # Remove parentheses
#             if key in data_dict.keys():
#                 #print(key)
#                  #annotation.update(pdfrw.PdfDict(Ff=1))#locks fillable field
#                 annotation.update( pdfrw.PdfDict(V=f'{data_dict[key]}')) #takes the data from models with [key], printing key returns all field from models 
#     #        annotation.update(pdfrw.PdfDict(Ff=1))#locks fillable field
#     # pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
  
    # N = 1 #N=1  can be returned directly in str(N)
    # annotations = template_pdf.pages[0]['/Annots'] # Only annotations that are Widgets Text
    # for annotation in annotations:
    #     if annotation['/Subtype'] == '/Widget':
    #         if annotation['/T']:
    #             key = annotation['/T'][1:-1] # Remove parentheses
    #             if key in data_dict.keys():
    #                 annotation.update(
    #                     pdfrw.PdfDict(T="{}".format(key + str(N))) #this one not sure yet
    #                 )
    #                 annotation.update(
    #                     pdfrw.PdfDict(V="{}".format(data_dict[key])) #takes the data from models with[key]
    #                 )
    #     #annotation.update(pdfrw.PdfDict(Ff=1))
    # N += 1
    #pdfrw.PdfWriter().write(output_pdf_path, template_pdf)