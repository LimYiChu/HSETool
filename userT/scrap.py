#from Businee logic for emails content GUNA
# def blbuildApprovedemail(ID):
#     urlview = f"/pmtrepviewall/{ID}/view"
#     Content=[]
#     actionDetails = ActionItems.objects.filter(id=ID).values() # Since off the bat i did not pass any other information besides ID to rejection form i now have to information back for emails
#     studyActionNo =  actionDetails[0].get('StudyActionNo')
#     studyName = actionDetails[0].get('StudyName')
#     response = actionDetails[0].get('Response')

#     print ("studyActionNoXXX",studyActionNo)
#     Content.append(studyActionNo + " from " + studyName + " has been approved ")
    
#     Content.append("To view this, please go to " + paremailurl +urlview + " . To approve go to your dashboard/approver que, to approve this and other actions")#+ "...Response" + response) #this is the content of the email #passed the url here in the content
    
#     return Content
# edward end 20210708 building approved email since  content is slightly different
# def blbuildRejectionemail(ID,RejectReason):
#     urlview = f"/pmtrepviewall/{ID}/view"
#     Content=[]
#     actionDetails = ActionItems.objects.filter(id=ID).values() # Since off the bat i did not pass any other information besides ID to rejection form i now have to information back for emails
#     studyActionNo =  actionDetails[0].get('StudyActionNo')
#     studyName = actionDetails[0].get('StudyName')
#     response = actionDetails[0].get('Response')

#     Content.append(studyActionNo + " from " + studyName + " has been rejected ") #This is subject
#     #edward add-on for rejection url
#     Content.append("Rejection Reason : " + RejectReason + ". To attend to this, please go to " + paremailurl +urlview)#+ "...Response" + response) #this is the content of the email #passed the url here in the content
    
#     return Content

 # if not Approver:
    #     Content.append(studyActionNo + " from " + studyName + " has been submitted ") #This is subject
    
    # elif Approver :
    #     Content.append(studyActionNo + " from " + studyName + " has been approved ") #This is subject
    
    # elif RejectReason != "" :
    #     Content.append(studyActionNo + " from " + studyName + " has been rejected ")
    
    # Content.append("To view this, please go to " + paremailurl +urlview + " . To approve go to your dashboard/approver que, to approve this and other actions")
    # Content.append("Rejection Reason : " + RejectReason + ". To attend to this, please go to " + paremailurl +urlview)#+ "...Response" + response) #this is the content of the email #passed the url here in the content


#from views
#edward 20210820 pdf bulk the commented code to be deleted in one week time
# def closeoutprint1(request,**kwargs): #edward 20210820 duplicate of closeoutprint to build bulk upload

#     ID = (kwargs["id"])
#     lstclosed = ActionItems.objects.filter(QueSeries =99)
#     obj = ActionItems.objects.filter(id=ID).values() # one for passing into PDF
#     objFk =ActionItems.objects.get(id=ID) # this is for getting all attachments

#     ObjAttach = objFk.attachments_set.all()  #get attcahments from foreign key

#     obj1 = ActionItems.objects.values()

#     studyActionNo =  objFk.StudyActionNo
#     print(studyActionNo)
#     replacestudyActionNo= studyActionNo.replace("/","_") #emdr comments replacing slash with underscore since / is filepath
#     Filename = replacestudyActionNo  + ".pdf" #emdr comments, specifying type of file, in this case pdf
#     #edward new tempfolder from parameters
#     out_file = tempfolder + Filename #emdr comments, chucking it into tempfolder

#     data_dict=obj[0] # emdr comments extracting data dict from QS, use 0 since there is only data dict in the qs for each item

#     discsub = blgetDiscSubOrgfromID(ID) #emdr comments standard getting discsuborg from id
#     Signatories = blgetSignotories(discsub)  #emdr comments standard getting signatories from discsuborg


#     lstSignatoriesTimeStamp= blgettimestampuserdetails (ID, Signatories) #edward changed this to use new bl for signature 20210706
#     signatoriesdict = blconverttodictforpdf(lstSignatoriesTimeStamp) #emdr comments just converting signatories to dict since using kvp for pdf

#     newcloseouttemplate = blsetcloseouttemplate (ID) # emdr comments setting template depending on level of approvers

#     file = pdfgenerate(newcloseouttemplate,out_file,data_dict,signatoriesdict) #emdr comments using my pitstc pdfgenerator

#     in_memory = BytesIO()

#     zip = ZipFile(in_memory,mode="w") #emdr comments basic zip + bytesio formatting

#     for eachfile in ObjAttach: #emdr comments getting  corresponding attachments for each item
#         filename = os.path.basename(eachfile.Attachment.name)
#         zip.write (eachfile.Attachment.path, "Attach_"+filename)



#     closeoutname = os.path.basename(out_file)
#     zip.write (out_file, closeoutname)
#     zip.close()

#     response = HttpResponse(content_type="application/zip") #emdr comments getting the zip file
#     response["Content-Disposition"] = "attachment; filename=" + studyActionNo+ ".zip"

#     in_memory.seek(0)
#     response.write(in_memory.read())


#     #dont delete below as its a way to actualy read from memory can be used elsewhere
#     #response = HttpResponse(content_type='application/pdf')
#     #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#     #bufferfile = pdfsendtoclient ('atrtemplateautofontreadonly.pdf',data_dict)
#     #edward changed file location to parameters

#    #return FileResponse(bufferfile, as_attachment=True, filename=out_file)

#     return response

# edward 20210823 pdf bulk back to main

    # for field in ActionItems._meta.fields:
    #     if field.get_internal_type() == 'ForeignKey':
    #         print (field.name)

    

    # # context['XYZ'] = json.dumps(forpie)
    # # json.dumps(forpie)
    #print ("CONTEXTFORPIE", forpie)
    # print ("FORPIEafter",context['forpie'])
    # lstbyDueDate    = blaggregatebydate(ActionItems.objects.all())
    # #print (lstbyDueDate)

    # lstplanned          = blprepareGoogleChartsfromDict(lstbyDueDate)

    # print (lstplanned)
    # lstactual           = blgetActualRunDown(lstplanned)
    # newlist             = blformulateRundown(lstplanned,lstactual)

    # for items in lstbyDueDate:

    #     x=items.get('DueDate')

    # subtotal =[]

    # for items in lstbyDueDate:
    #    subtotal.append(items['count']) #how to access dictionary object by

    # content1 =  newlist


    # content2= [['2021-01-10', 136, 136],
    #             ['2021-02-10', 133, 136],
    #             ['2021-04-18', 124, 136],
    #             ['2021-04-29', 113, 136],
    #             ['2021-05-01', 110, 136],
    #             ['2021-05-08', 80, 136],
    #             ['2021-06-03', 77, 133],
    #             ['2021-07-09', 70, 131],
    #             ['2021-07-13', 69, ],
    #             ['2021-07-15', 67, ],
    #             ['2021-07-16', 66, ],
    #             ['2021-07-23', 63, ],
    #             ['2021-07-30', 15, ],
    #             ['2021-08-26', 14, ],
    #             ['2021-10-10', 13, ],
    #             ['2021-10-15', 10, ],
    #             ['2021-10-16', 8, ],
    #             ['2021-10-17', 0, ]]