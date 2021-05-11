import pdfrw

def pdfgenerate(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path) # Read Input PDF
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))# Set Appearences ( Make Text field visible )
    # Loop all Annotations
    for annotation in template_pdf.pages[0]['/Annots']:#loop over all pages in pdf, and for each page, loop over all ediatble fields called annots, for each page all annotations stored in 'Annots/' 
        if annotation['/Subtype'] == '/Widget' and annotation['/T']:  # all key names for each field stored in'/T'
            key = annotation['/T'][1:-1] # Remove parentheses
            if key in data_dict.keys():
                annotation.update( pdfrw.PdfDict(V=f'{data_dict[key]}')) #takes the data from models with [key], printing key returns all field from models 
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


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
  
    # N = 1
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