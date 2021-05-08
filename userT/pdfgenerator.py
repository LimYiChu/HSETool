import pdfrw
from UploadExcel. models import ActionItems

def pdfgenerate(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path) # Read Input PDF
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))# Set Apparences ( Make Text field visible )
    # # Loop all Annotations
    # for annotation in template_pdf.pages[0]['/Annots']:# Only annotations that are Widgets Text
    #     if annotation['/Subtype'] == '/Widget' and annotation['/T']: 
    #         key = annotation['/T'][1:-1] # Remove parentheses
    #         if key in data_dict.keys():
    #             #annotation.update(pdfrw.PdfDict(Ff=1))#locks fillable field
    #             annotation.update( pdfrw.PdfDict(V=f'{data_dict[key]}'))
    #         annotation.update(pdfrw.PdfDict(Ff=1))#locks fillable field
    # pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
  
    N = 1
    annotations = template_pdf.pages[0]['/Annots'] # Only annotations that are Widgets Text
    for annotation in annotations:
        if annotation['/Subtype'] == '/Widget':
            if annotation['/T']:
                key = annotation['/T'][1:-1] # Remove parentheses
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(T="{}".format(key + str(N))) #this one not sure yet
                    )
                    annotation.update(
                        pdfrw.PdfDict(V="{}".format(data_dict[key])) #takes the data from models with[key]
                    )
        #annotation.update(pdfrw.PdfDict(Ff=1))
    N += 1
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)