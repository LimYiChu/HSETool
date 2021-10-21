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
