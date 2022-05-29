#20220225 grom businesslogic.py


    #20211208 Ishna first box
    # riskrankingsummary = blaggregateby(ActioneeActionsrisk,"RiskRanking")
    # for QSeries, ApproRoutes in Approver_R.items():
    #     ApproverActions = blallactionscomdissubQ(ApproRoutes,QSeries,reducedfields)
    #     ApproverActionsrisk = bladdriskelements(list(ApproverActions))
    #     riskrankingapproverraw = blaggregateby(ApproverActionsrisk,"RiskRanking")
    #     if riskrankingapproverraw is not None:
    #         newcounter = Counter(riskrankingapproverraw) + Counter(newcounter)
    #         riskrankingapprover = newcounter
    #         riskrankingactionee = Counter(riskrankingsummary)
    #         riskrankingsummary = riskrankingapprover + riskrankingactionee
    #20211208 Ishna first box

# #20211122 edward stitchpdf
# def blexceltopdf(pdfpath,pdf_list_onlyexcel):
#     """This function converts .xlxs to .pdf files using xlwings library. This library only works on windows or macOS machines """

#     for items in pdf_list_onlyexcel:
#         fullpathexcel = os.path.join(pdfpath,items)
#         pdf_filename_test = os.path.splitext(items)[0]+'.pdf'
#         test = xw.Book(fullpathexcel)
#         exceltopdf = test.to_pdf(pdfpath + pdf_filename_test)
#         closeexceltopdf = test.close()

#     return exceltopdf



# 20220225 from views.py


# def googlecharts(request):
    
#     content1 = [['By Studies', '///Open Actions by Organisation:::'], ['RWP', 13], 
#                 ['HESS', 20], ['SFSB', 2], ['MMHE', 28]]

#     context = {

#          'content' : content1,
#     #     'charttitles' : "XYZ"


#      }
#     context['XYZ'] = json.dumps([{

#                     "data" : [[{
#                                 "Feature1" : "Open Action by organisation",
#                                 "Feature2" : "No: Open"},
#                                 {
#                                 "Feature1" : "MMHE","Feature2" : 28
#                                 },{
#                                 "Feature1" : "SFSB","Feature2" : 2
#                                 },{
#                                     "Feature1" : "HESS","Feature2": 20
#                                 },
#                                 {
#                                     "Feature1" : "RWP","Feature2": 20
#                                 }],[
#                                     {
#                                 "Feature1" : "Open/Closed Actions", "Feature2" : "Open Closed"},
#                                 {
#                                 "Feature1" : "Open",
#                                 "Feature2" : 192
#                                 },

#                                 {
#                                 "Feature1" : "Closed",
#                                 "Feature2" : 12
#                                 },
#                                 ]
#                             ]
#                 }])
    
#     data=  [[['By Studies', '///Open/Closed Actions:::'], ['Open', 220], ['Closed', 12]], 
#             [['By Studies', '///Open Actions by Organisation:::'], ['HESS', 20], ['MMHE', 28], ['RWP', 13], ['SFSB', 2]],
#             [['By Studies', '///Submitted Actions by Organisation:::'], ['HESS', 12], ['MMHE', 16], ['RWP', 6], ['SFSB', 0]],
#             [['By Studies', '///Open Actions by Discipline:::'], ['HUC', 19], ['Operations', 7], ['Drilling', 7], ['EHS', 1], ['EHS', 1], ['Safety', 9], ['Marine', 6], ['Electrical', 71], ['Commissioning', 3], ['Mechanical', 2], ['MARINE', 6], ['EHS', 0]],
#             [['By Studies', '///Open Actions by Studies:::'], ['MRU Barge Campaign Post Shutdown - Phase3', 34], ['HAZID', 19], ['HAZOP', 2], ['CRA-DPDSV/PRECOMM', 0], ['Environmental Impact Identification (ENVID)', 0], ['Hazard Identification (HAZID) Study', 0], ['Hazard and Operability (HAZOP) Study', 0], ['SAFOP Report', 75], ['NMB Phase 4A Concept Definition - HAZID Report', 28], ['NMB Phase 4A Concept Definition', 34]]]

#     featuresfields = ["Feature1", "Feature2"]
#     data2=[]
#     data3 =[]
#     #for items in data:
#         # for xyz in items:
#         #     data1 = dict(zip(featuresfields,xyz))
#         #     data2.append(data1)

#         # data2= [dict(zip(featuresfields,pies)) for pies in items]
        
#         # data3.append(data2)
#         # data2=[]
#     data3 = blmakelistforjson(data,featuresfields)
    
#     context['XYZ'] = json.dumps([{"data":data3}])
 
       
#     return render(request, 'userT/googlecharts.html',context) 

# edward 20210713 new chart

    #dont delete below as its a way to actualy read from memory
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #bufferfile = pdfsendtoclient ('atrtemplateautofontreadonly.pdf',data_dict)
#this annotate function needs to first because it doesnt like addtional items added to query set

    # for itemPair in discsub:

    #     routesfortheDiscpline = ActionRoutes.mdlgetActioneeAppr.mgr_getActApp(itemPair)



    #     for items in routesfortheDiscpline:


    #         listofPairActioneeCount.append(blgetDiscSubActionCount ('Y',itemPair,[0]))
    #         listofPairApproverCount.append(blgetDiscSubActionCount ('Y',itemPair,ApproverQList))
    #         listofPairNameCount.append(items.Actionee)
    #
    #         listoflist.append(listofPairNameCount)
    #         listofPairNameCount = []

# def loadajax (request):

#     if (request.is_ajax ()):
#         #ID= form2.instance.id
#         print (request.GET.get('button_text'))
#         t=time()
#         print ("INHEREERERERE")
#         return JsonResponse({'seconds':t},status=200)
#     else :

#         return render(request, 'userT/loadajax.html')
 
# 20220225 from urls.py
         # path('loadajax/', login_required(UserView.loadajax), name='loadajax' ),
        #20220217 edward commented bcs moved loadajax 2 & 3 to scrap -- tp be deleted a week from now
        # path('loadajax2/', login_required(UserView.loadajax2), name='loadajax2' ),
        # path('loadajax3/', login_required(UserView.loadajax3), name='loadajax3' ),
 
 #20220217 edward from views.py 

 # def loadajax2 (request):

   

#     if (request.is_ajax ()):
#         #ID= form2.instance.id
#         print (request.GET.get('button_text'))
#         t=50
#         print ("INHEREERERERE22222222222")

        
#         return JsonResponse({'buttontext': "Hi i am new"},status=200)
#     else :

#         return render(request, 'userT/loadajax.html')

# def loadajax3 (request):

   

#     if (request.is_ajax ()):
#         #ID= form2.instance.id
#         print (request.GET.get('button_text'))
       
#         context =   {
#                     'abc':"abc",
#                     'xyz' : "xyz"
#                     }
#         return JsonResponse({'context':context},status=200)
#     else :

#         return render(request, 'userT/loadajax.html')
 # def studiesjs(request):

#     if request.is_ajax and request.method == "GET":
#         data = request.GET.get("data", None)
#         print(data)
#         all_actions =   ActionItems.objects.all().values()
#         all_actionwithfk = blannotatefktomodel(all_actions)
#         dfalllist = blgetActionStuckAtdict(all_actionwithfk) # getting a list of everything
#         dfall = pd.DataFrame.from_dict(dfalllist) #puts it into df columns format
#         dfallnestedstudysorted = blsortdataframes(dfall,dfstudiescolumns) # sort dfall
#         dfsortbystudy = dfallnestedstudysorted[dfallnestedstudysorted["StudyName"] == data ] #this value should be modular like phases, need to look up ajax more to get this to work

#         dfstudieslist = dfsortbystudy.values.tolist()
#         dfstudiesdict = dfsortbystudy.to_dict()
        
#         nestedheader = ['Study Action No', 'Study Name' ,'Action With','Action Link']
#         context =   {
#                     'dflist':dfstudieslist,
#                     'nestedheader' : nestedheader,
#                     'dfstudiesdict': dfstudiesdict
#                     }
     
#         return JsonResponse(context,status=200)
#     else:
#         return render(request, 'userT/inclnestedstudytable.html')

 #20220124
 # if form_class :
    #     newcloseouttemplate = f'{closeouttemplate}{form_class}{ApproverLevel}{".pdf"}' if ApproverLevel == 5 or ApproverLevel == 7  else  f'{closeouttemplate}{form_class}{".pdf"}'  
    # else: 
    #     newcloseouttemplate = f'{closeouttemplate}{ApproverLevel}{".pdf"}' if ApproverLevel == 5 or ApproverLevel == 7 else  f'{closeouttemplate}{".pdf"}' 
    
# 20220121 edward from views.py
#closeoutprint
    #dont delete below as its a way to actualy read from memory can be used elsewhere 
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #bufferfile = pdfsendtoclient ('atrtemplateautofontreadonly.pdf',data_dict)
    #edward changed file location to parameters

   #return FileResponse(bufferfile, as_attachment=True, filename=out_file)


#20211229 edward from forms.py

#20211229 edward using Inheritance on hold 

# class frmtestBase(forms.ModelForm):
    
#     def __init__(self, *args, **kwargs):
#         super(frmtestBase, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_show_labels = True
#         self.fields['FutureAction'].label = strFutActApprNotes
#         self.helper.form_method = 'POST'
#         self.fields['Response'].required = True 
#         #self.helper.add_input(Submit('Upload', 'Next...', css_class='btn btn-outline-dark float-right col-md-1'))
#         #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn btn-outline-dark float-right col-md-1'))

#         self.helper.layout = Layout(
        
        
#         Div(
#             Div(Field('StudyActionNo',readonly=True),   css_class='col-md-2'), #style="font-family: Dancing Script",
#             Div (Field('StudyName',readonly=True,disabled=True),  css_class='col-md-3 read-only'),
#             Div (Field('ProjectPhase', readonly=True,disabled=True), css_class='col-md-3'), #,disabled=True
#             Div (Field('InitialRisk', readonly=True), css_class='col-md-2'),
#             Div (Field('ResidualRisk', readonly=True), css_class='col-md-2'),
#             Div (Field('StudyName',readonly=True,type="hidden")),
#             Div (Field('ProjectPhase',readonly=True,type="hidden")),
#             css_class='row',
                      
#            ),)
#     class Meta:
#         model = ActionItems
#         fields = '__all__'

# class frmtestUpgradedBase(frmtestBase):
#     def __init__(self, *args, **kwargs):
#         super(frmtestUpgradedBase,self).__init__(*args,**kwargs)
        
#         self.helper = FormHelper()

#20211227 edward from businesslogic.py 
#20211122 edward stitchpdf
# import xlwings as xw
#20211202 edward commented out this import because there is a problem with img2pdf library on linux
# import img2pdf
# from PIL import Image

#this was the image to pdf converter which was causing errors in linux
#20211202 edward commented out this function because there is a problem with img2pdf library on linux
#20211122 edward stitchpdf
# def blimagetopdf(pdfpath,pdf_list_onlyjpg):
#     """This function converts .jpg image to .pdf files using the img2pdf library"""
    
#     for jpgs in pdf_list_onlyjpg:
#         fullpath_jpgs = os.path.join(pdfpath,jpgs)
#         image = Image.open(fullpath_jpgs)
#         pdf_bytes = img2pdf.convert(image.filename)
#         pdf_filename = pdfpath + image.filename
#         pdf_filename_test = os.path.splitext(jpgs)[0]+'.pdf'
#         file = open(pdfpath + pdf_filename_test, "wb")
#         filewrite = file.write(pdf_bytes)
#         closeimage = image.close()
#         finalfileclose = file.close()
        
#     return finalfileclose 

#this was taken from bltotalholdtime for Actionee
    # #Actionee
    # for items in ActioneeActions:
    #     dictactualhistory = ActionItems.history.filter(id=items["id"]).filter(QueSeries=queActionee).order_by('-history_date').values()
    #     historyrecentimeactionee = dictactualhistory[0].get('history_date')
        
    #     # for item in dictactualhistory:
    #     timeinbasket = timezonenow - historyrecentimeactionee
    #     blanklist.append(timeinbasket)
    # dfdates = pd.DataFrame(blanklist)
    # print(dfdates)

    # if not dfdates.empty : 
        
    #     dfdatessum = dfdates.sum(axis=0)
        
    #     dftodict = dfdatessum.to_dict()
    #     new_key = "total"
    #     old_key = 0
    #     dftodict[new_key] = dftodict.pop(old_key)
    #     strdays = str(dftodict['total'].days)
        

        #20211207 edward current holding time ends here

#this was taken from blexceedholdtime for Actionee
    # #Actionee Actions 
    # for items in ActioneeActions:
    #     dictactualhistory = ActionItems.history.filter(id=items["id"]).filter(QueSeries=queActionee).order_by('-history_date').values()
    #     print('dacthistory',dictactualhistory)
    #     historyrecentimeactionee = dictactualhistory[0].get('history_date')
    #     # print('test',test)
    #     # for item in dictactualhistory:
            
    #     #     # todays date minus the last date that this item was in the history date field
    #     timeinbasket = timezonenow - historyrecentimeactionee
    #     #print('timeinbasketoutsideforloop',item["id"],timeinbasket)
    #     #if timeinbasket more than seven then append that item id to a list 
    #     if timeinbasket > sevendays :
    #         oneweeklist.append(items["id"])
    #     #if timeinbasket more than fourteen then append that item id to a list 
    #     if timeinbasket > fourteendays :
    #         twoweeklist.append(items["id"])

#20211221 from businesslogic.py edward 1
#20211221 edward rejected actions count for Actionee by going through custom user
# def blActrejectedactionscount (usersemail):
#     lstUserSeries =  CustomUser.objects.filter(email=usersemail).values()
#     discsuborglist=[]
#     for items in lstUserSeries:
#         discsuborglist.append(items['disipline'])
#         discsuborglist.append(items['subdisipline'])
#         discsuborglist.append(items['organisation'])
#     # print(discsuborglist)
#     rejectedactionscount = blnewgetrejecteditemsQcount(discsuborglist,1,phase="")
#     # print(rejectedactionscount)
#     return rejectedactionscount

#20211206 from views.py reppmtexcel edward
    # #for workshop based view
    # #20211201 edward
    # # if phase == "":
    # #     ActionItem = ActionItems.objects.values('StudyName')
    # # else:
    # #     ActionItem= ActionItems.objects.filter(ProjectPhase__ProjectPhase=phase).values('StudyName')
    # # dfactionitem = pd.DataFrame(ActionItem)
    # # dfactionitemfilter = dfactionitem.drop_duplicates()
    
    # # dfactionitemlist = dfactionitemfilter.values.tolist()

    # #20211203 edward
    # studiesattributes =['StudyName','ProjectPhase']
    # phasestudies =  blphasegetStudyreducedfieldsQ(studiesattributes,phase)
    # #print(phasestudies)
    # # blankstudy=[]
    # # for item in phasestudies:
    # #     teststudies = (item['StudyName'])
    # #     print(teststudies)
    
#20211206 from manager.py edward

#20211206 edward get studies by phase
# def mgr_GeneralItemsFiltersKwargsQReducedStudies(self,FiltersKwargs,ReducedValuesArgs):
#     """This class is used just for getting Studies by phases"""
#     return self.get_queryset().get_GeneralActionsKwargsQArgsValuesStudies(FiltersKwargs,ReducedValuesArgs)

# #20211203 edward
# def get_GeneralActionsKwargsQArgsValuesStudies(self,FilterKwargs,ArgsValues):
#     """ This function is used to look in the Studies table, filter & select the values in the ProjectPhase_id column"""
#     #print(ArgsValues)
#     return self.filter(FilterKwargs).select_related("ProjectPhase").values(*ArgsValues)
# #20211203 edward

# #20211203 edward
# class mgrallActionCountStudies(models.Manager):
#     """This class is used just for getting Studies by phases"""
#     def get_queryset (self):
#         return QuerySet(self.model, using=self._db)
#     def mgr_GeneralItemsFiltersKwargsQReducedStudies(self,FiltersKwargs,ReducedValuesArgs):
#         return self.get_queryset().get_GeneralActionsKwargsQArgsValuesStudies(FiltersKwargs,ReducedValuesArgs)
# #20211203 edward


#20211202 from views.py edward
# def repPMTExcel (request,phase=""):
#     """This is the original function called when user selects PMT Reporting from menu
#     It dumps all actions into this function """
    
#     #added for phases - Get all phases from Phases table for Html
#     listofPhases= Phases.mdlSetGetField.mgrGetAllActionsAndFields()
#     #20211202 edward previous discsuborg was looping through the AR table, changed to temporarily use dfdiscsuborgphase which uses DF to sort actions by phase
#     discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() 
#     discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
    
#     organisationnames = ActionRoutes.mdlAllCompany.mgr_getOrgnames()

#     #20211201 edward this one replaces discsuborg
#     dfdiscsuborgphase = bldfdiscsuborgphase(phase)

#     #1st Pie Overall Actions Open/Closed
#     forpie=[]
#     PhaseOpenActions= blallphasegetAction(QueOpen,phase)
#     PhaseClosedActions = blallphasegetAction(QueClosed,phase)
#     labelpie =['Open', 'Closed']
#     titlepie = "Open/Closed Actions"
#     googlechartlistoverphase= blprepGoogChartsbyStudies(labelpie,[PhaseOpenActions,PhaseClosedActions],titlepie )
#     forpie.append(googlechartlistoverphase)
    
#     #2nd Pie Open action by organisation
#     countorg =[] 
#     titleorg = "Open Actions by Organisation"          
#     for items in organisationnames:
#             countorg.append(blgetCompanyActionCountPhase (items,QueOpen,phase))
#     googlechartlistorganisation = blprepGoogChartsbyStudies(organisationnames,countorg,titleorg)
#     forpie.append(googlechartlistorganisation)

#    #3rd Pie Submitted actions by organisation
#     titlesubmitted = "Submitted Actions by Organisation" 
#     countsubmitted =[]         
#     for items in organisationnames:
#             countsubmitted.append(blgetCompanyActionCountPhase (items,ApprovalQue,phase))
#     googlechartlistsubmitted = blprepGoogChartsbyStudies(organisationnames,countsubmitted,titlesubmitted)
#     forpie.append(googlechartlistsubmitted)

#     #4th Pie Open Actions for discipline
#     countdiscsub= []
#     labelsDisc =[]
#     titledisc = "Open Actions by Discipline"
    
#     for itemPair in discsub:
#         countdiscsub.append(blgetDiscSubActionCountPhase (itemPair,QueOpen,phase))
#         labelsDisc.append(str(itemPair[0]))#+"/"+str(itemPair[1]))
#     googlechartlistdiscipline = blprepGoogChartsbyStudies(labelsDisc,countdiscsub,titledisc)
#     forpie.append(googlechartlistdiscipline) 

#     #5th Pie  Overall Open actions by Studies
#     labelsworkshop = Studies.objects.all()        
#     countstudies = []
#     labelsstudies = []
#     titlestudies = "Open Actions by Studies"

#     for study in labelsworkshop:
#         countstudies.append(blallActionCountbyStudiesPhaseQ(study.StudyName,QueOpen,phase))
#         labelsstudies.append(study.StudyName)
#     googlechartliststudies = blprepGoogChartsbyStudies(labelsstudies,countstudies,titlestudies)
#     forpie.append(googlechartliststudies)
#     #***End Pie Guna

    
#     # added phase here in Indisets to get phase specific items
#     #20211201 edward remove discsuborg here because using discsuborg in bl
#     # Indisets = blgetIndiResponseCount2(discsuborg,QueOpen,QueClosed,phase) 
#     Indisets = blgetIndiResponseCount2(dfdiscsuborgphase,QueOpen,QueClosed,phase) 
    
                
#     # tableindiheader = ['User','Role','Organisation Route','Yet-to-Respond','Yet-to-Approve','Closed', 'Open Actions']
#     tableindiheader = ['User','Role','Organisation Route','Pending Submission','Pending Approval','Closed', 'Open Actions'] #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
    
    
#     #edited by edward 20210706 to only show yet to approve & yet to respond
   
#     listaggregatedindi,listaggregatedindiheader=blgroupbyaggsum(Indisets,tableindiheader,'User', ['Pending Submission','Pending Approval']) #this has been changed by edward 20210706, used to be Yet-to-Respond & Yet-to-Approve
#     #print(listaggregatedindi)
#     # allactions = ActionItems.objects.all()
#     tableallheader = ['id','StudyActionNo','StudyName', 'ProjectPhase','Disipline' ,'Recommendations', 'Response','DueDate','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
#     # lstofallactions = blgetActionStuckAt(allactions, tableallheader) #basically you feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
#     tableallheadermodified = ['Study Action No','Study Name', 'Project Phase','Discipline' ,'Recommendations', 'Response','Due Date','Initial Risk']
    
#     #All actions and actions by Phases
#     justenoughattributes =  ['id','StudyActionNo','Disipline' ,'Recommendations', 'QueSeries', 'Response','DueDate','InitialRisk']
#     #phasesactions =  ActionItems.mdlgetField.mgrGetAllActionswithPhases(True,justenoughattributes) #Todelete old code

#     phasesactions =  blphasegetActionreducedfieldsQ(justenoughattributes,phase)
#     #this annotate function needs to first because it doesnt like addtional items added to query set
#     dictofallactions    = blannotatefktomodel(phasesactions)
#     #this sequence is important otherwise doesnt work
#     phaseswithrisk = bladdriskelements(dictofallactions)
#     dictofallactions    = blgetdictActionStuckAt(phaseswithrisk)
    
#     # # # edward 20210803 dataframes excel
#     # all_actions =   ActionItems.objects.all().values()#'StudyActionNo','StudyName','ProjectPhase', 'Facility','Guidewords', 'Deviation', 'Cause', 'Consequence', 'Safeguard','InitialRisk','ResidualRisk', 'Disipline' ,'Recommendations','DueDate', 'Response','FutureAction')
#     # rem_list2 = ['QueSeries','QueSeriesTarget','DateCreated'] #OPtimising data to be removed
#     # blank=[]
#     # all_actionsopt = bladdriskelements(all_actions, blank)
#     # dfall1 = pd.DataFrame.from_dict(all_actionsopt) # sort dfall
#     # dfall = blsortdataframes(dfall1,dfallcolumns)

    
#     # # # edward end 20210803 dataframes excel

#     #RejectDetails - gonna use a different way same way as actionne list
#     #just using revision way to get all rejected actions
    
#     #edward 20211001 pd allactions
#     all_actions =   ActionItems.objects.all().values()
#     all_actionsannotate = blannotatefktomodel(all_actions)
#     blank=[]
#     all_actionsopt = bladdriskelements(all_actionsannotate)
#     dfall1 = pd.DataFrame.from_dict(all_actionsopt) # sort dfall
#     dfall = blsortdataframes(dfall1,dfallcolumns)
#     #edward 20211001 pd rejected excel 
   
#     revisiongte = 1
#     queseriesrejected = 0
   

#     #Rejected details using Q Object
#     rejectedactions = blphasegetrejectedactionsQ (revisiongte,queseriesrejected,justenoughattributes,phase)
#     rejecteddictofallactions    = blannotatefktomodel(rejectedactions)
#     #this sequence is important otherwise doesnt work
#     rejectedallactionitems = bladdriskelements(rejecteddictofallactions)
#     dfrejection = pd.DataFrame.from_dict(rejectedallactionitems)
    
#     #for Disipline based view
#     #20211201 edward 
#     tabledischeader = ['Discipline', 'Yet to Respond' ,'Approval Stage', 'Closed','Open Actions','Total Actions']
#     lstbyDisc= blaggregatebyDisc(dfdiscsuborgphase,  YetToRespondQue, ApprovalQue,QueClosed,QueOpen,TotalQue)


#     #get rejected summary actions get Reject Table
#     tablerheaderejected = ['Discipline', 'Rejected Count']
#     listofrejecteditems = blgetrejectedcount(dfdiscsuborgphase,1) #Pass revision number => than whats required


#     #for workshop based view
#     #20211201 edward
#     if phase == "":
#         ActionItem = ActionItems.objects.values('StudyName')
#     else:
#         ActionItem= ActionItems.objects.filter(ProjectPhase__ProjectPhase=phase).values('StudyName')
#     dfactionitem = pd.DataFrame(ActionItem)
#     dfactionitemfilter = dfactionitem.drop_duplicates()
    
#     dfactionitemlist = dfactionitemfilter.values.tolist()
#     print('df',dfactionitem)

#     allstudies = Studies.objects.all()
    
#     tablestudiesheader = ['Studies', 'Yet to Respond' ,'Approval Stage','Closed','Open Actions', 'Total Actions']

#     lstbyWorkshop = blgetbyStdudiesCount(allstudies,YetToRespondQue,ApprovalQue,QueClosed,QueOpen,TotalQue)
    
    
#     #Changed to Q function and Phases
#     tableduedateheader = ['Due Date','Actions to Close by']
#     fieldsrequired = ['id','StudyActionNo', 'DueDate','QueSeries']
#     actionitemsbyphase = blphasegetActionreducedfieldsQ(fieldsrequired,phase)
#     lstbyDueDate= blaggregatebydate(blphasegetActionreducedfieldsQ(fieldsrequired,phase))
   
#     #20211021 edward rundown by phase 
#     closed=99
#     closeditems = actionitemsbyphase.filter(QueSeries=closed)
#     totalactions = (len(actionitemsbyphase))
#     closedactions = (len(closeditems))
    
#     subtotal =[]
#     for items in lstbyDueDate:
#        subtotal.append(items['count']) #how to access dictionary object by

#     totalallDueDate = sum(subtotal)
    
#     lstplanned         =  blprepareGoogleChartsfromDict(lstbyDueDate)
#     lstactual      = blgetActualRunDown(lstplanned,closeditems) # shows how many closed pass in here 
    
#     newlist = blformulateRundown(lstplanned,lstactual)
#     #edward 20210727 rundown, 20211021 edward updated
#     newliststop = blstopcharttoday(newlist,totalactions,closedactions)
#     #edward end 20210727 rundown, 20211021 edward updated
#     #20211021 edward rundown by phase 

#     if request.method == 'POST':

#         if (request.POST.get('allActions')):

#             #edward 20210803 dataframes excel

#             # all_actions =   ActionItems.objects.all().values()
#             # all_actionsannotate = blannotatefktomodel(all_actions)
#             # blank=[]
#             # all_actionsopt = bladdriskelements(all_actionsannotate, blank)
#             # dfall1 = pd.DataFrame.from_dict(all_actionsopt) # sort dfall
#             # dfall = blsortdataframes(dfall1,dfallcolumns)

#             in_memory = BytesIO()
#             #workbook = dfall.to_excel(in_memory)

#             #tableallheader.append("Current Actionee/Approver") #appends the last column that the list spits out #yhs changed from tableallheader to tableallheadermodified
#             #workbook = excelAllActions(lstofallactions,tableallheader,"All Action Items",1) #optional parameter passed to remove excel columns if required
#             response = HttpResponse(content_type='application/ms-excel') #
#             response['Content-Disposition'] = 'attachment; filename=byAllActions.xlsx'
#             #workbook.save(response) # odd  way but it works - took too long to figure out as no resource on the web
        
#             with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
#                 dfall.to_excel(writer, sheet_name='All Actions',engine='xlsxwriter',header=None,startrow=1)
#                 workbook = writer.book #gives excelwriter access to workbook
#                 worksheet = writer.sheets['All Actions'] #gives excelwriter access to worksheet
#                 formattedexcel = blexcelformat(dfall,workbook,worksheet)

#             in_memory.seek(0)
#             response.write(in_memory.read())
#             #edward end 20210928 dataframes excel

#             return response
#         elif (request.POST.get('rejectedactions')):

#             in_memory = BytesIO()
#             drejectedsorted = blsortdataframes(dfrejection,dfrejectedcolumns)

#             with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
#                 drejectedsorted.to_excel(writer, sheet_name='Rejected Actions',engine='xlsxwriter',header=False,startrow=1)
#                 workbook = writer.book #gives excelwriter access to workbook
#                 worksheet = writer.sheets['Rejected Actions'] #gives excelwriter access to worksheet
#                 formattedexcel = blexcelformat(drejectedsorted,workbook,worksheet)
#            # workbook = dfrejection.to_excel(in_memory)
#             #just use memory and workbook is redundant
#             response = HttpResponse(content_type='application/ms-excel') #
#             response['Content-Disposition'] = 'attachment; filename=byRejectedActions.xlsx'
#             in_memory.seek(0)
#             response.write(in_memory.read())

#             return response

#         elif (request.POST.get('indisummary')):
            

#             workbook = excelAllActions(listaggregatedindi,listaggregatedindiheader,"Individual Summary")
#             # test = listaggregatedindi
            
#             # headers = ["User","Pending Submission","Pending Approval"]
#             # for items in listaggregatedindi:
#             #         test = dict(zip(headers, items))
#             #         dfindisumm = pd.DataFrame.from_dict([test])
#             #         in_memory = BytesIO()
#             #         dfindisummsorted = blsortdataframes(dfindisumm,dfindisummcolumns)

#             #         with pd.ExcelWriter(in_memory)as writer: #using excelwriter library to edit worksheet
#             #             dfindisummsorted.to_excel(writer, sheet_name='Individual Summary',engine='xlsxwriter',header=False,startrow=1)
#             #             workbook = writer.book #gives excelwriter access to workbook
#             #             worksheet = writer.sheets['Individual Summary'] #gives excelwriter access to worksheet
#             #             formattedexcel = blexcelformat(dfindisummsorted,workbook,worksheet)
#             #             print(dfindisummsorted)

#             #         response = HttpResponse(content_type='application/ms-excel') #
#             #         response['Content-Disposition'] = 'attachment; filename=byIndividualSummary.xlsx'
#             #         in_memory.seek(0)
#             #         response.write(in_memory.read())

#             response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
#             response['Content-Disposition'] = 'attachment; filename=byIndividualSummary.xlsx'
#             workbook.save(response)
#             return response

#         elif (request.POST.get('indiActions')):


#             workbook = excelAllActions(Indisets,tableindiheader,"Individual Actions")

#             response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
#             response['Content-Disposition'] = 'attachment; filename=byIndividual.xlsx'
#             workbook.save(response)
#             return response

#         elif (request.POST.get('allStudies')):

#             workbook = excelAllActions(lstbyWorkshop,tablestudiesheader,"Workshop Actions")

#             response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
#             response['Content-Disposition'] = 'attachment; filename=byStudies.xlsx'
#             workbook.save(response)
#             return response

#         elif (request.POST.get('bydiscipline')):


#             workbook = excelAllActions(lstbyDisc,tabledischeader,"Discipline Actions")

#             response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
#             response['Content-Disposition'] = 'attachment; filename=byDiscipline.xlsx'
#             workbook.save(response)
#             return response

#         elif (request.POST.get('byDueDate')):

#             reallstDuedate = blquerysetdicttolist(lstbyDueDate) #need a list
#             workbook = excelAllActions(reallstDuedate,tableduedateheader,"DueDates")

#             response = HttpResponse(content_type='application/ms-excel') # mimetype is replaced by content_type for django 1.7
#             response['Content-Disposition'] = 'attachment; filename=byDueDates.xlsx'
#             workbook.save(response) # odd way but it works - took too long to figure out as no resource on the web
#             return response    
     
    
#     #This needs to be worked on more as there are other problems now if risk matrix is not loaded
#     #riskmatrix = blgetRiskMatrixAvailable()
#     context = {
        
#         'riskmatrix' : True,
#         #'forpie' : forpie, #commented out Guna
#         'lstbyDueDate' : lstbyDueDate,
#         'tableduedateheader' : tableduedateheader,
#         'totalallDueDate' : totalallDueDate, 
#         #'rundowncontent': newliststop, #edward 20210727 rundown#commented out Guna
#         'lstbyDisc' : lstbyDisc,
#         'lstbyWorkshop' : lstbyWorkshop,
#         'Indisets' : Indisets,
#         #'lstofallactions' : lstofallactions,
#         #dict of all actions
#         "dictofallactions" : dictofallactions,
#         'tableindiheader' : tableindiheader,
#         'tablestudiesheader' : tablestudiesheader,
#         'tabledischeader' : tabledischeader ,
#         'tableallheader' : tableallheadermodified,
#         'listaggregatedindi':listaggregatedindi,
#         'listaggregatedindiheader':listaggregatedindiheader,
#         'listofrejectedheader': tablerheaderejected,
#         'listofrejecteditems': listofrejecteditems,
#         "rejectedactions": rejectedallactionitems,
#         "listofPhases": listofPhases,
#         "phase": phase,
#         "piechartsjson" : json.dumps([{"data":forpie}])
#     }
#     #moving tojson 26/09/2021 - Guna. Moving to json enables cleaner javascript and data passing between python and html and javascript
    
#     # #1st approach lace the dictionary wih features
#     #featuresfields = ["Feature1", "Feature2"]
#     #data3 = blmakelistforjson(forpie,featuresfields)
#     # context["piechartsjson"]= json.dumps([{"data":data3}])
    
#     #Test for lineshart
#     #dataforrundown = blmakelistforjson(newliststop,featuresfields)
#     #2nd approach should have done it like this in the first place simple stratight. Leaving the above to see how to lace and extract
#     context["rundownchartsjson"] = json.dumps([{"data":newliststop}]) #one line, going to leave the above approach so that it could be used elsewhere
#     #end Json changes

#     return render(request, 'userT/reppmtexcel.html', context)
#20211130 from views.py edward
#Todelete if not used
# def getActionDetails(request, id=None):
#     Items = get_object_or_404(ActionItems,id=id)
#     context = {
#             "Items":Items

#     }
#     return render(request, "userT/detailactions.html", context) #ok checked by yhs in terms of capital letters.

#20211125 from views.py edward
#from reppmt
 #edward 20210804 original excel commented out bcs replacing with dfexcel
    # workbook = excelCompleteReport(request)
    # response = HttpResponse(content_type='application/ms-excel') #
    # response['Content-Disposition'] = 'attachment; filename=AllActionDetails.xlsx'
    # workbook.save(response) # odd  way but it works - took too long to figure out as no resource on the web
    #edward end 20210804 original excel commented out bcs replacing with dfexcel

#20211125 from parameters.py edward
#edward - old
# new parameter file 
#url-links
# cclist = ["ehstools@prism-ehstools.awsapps.com"]#cclist to send a copy of email to ehstools email since there is no record of sent mail for emails sent by system
# appurl = "https://sapuraphase4a.prism-ehstools.com"#for now, please change appurl for different clients
# emailSender ="ehstools@prism-ehstools.awsapps.com"#used in views for email sender origin address

# #file directories
# #temp folder location (used for pdf closeoutprint & indiprint)
# tempfolder = 'opt/bitnami/projects/HSETool/static/media/temp/'
# tempfolder = 'static/media/temp/'

# #static/media folder location (used for old pdf generate function in views called closeoutsheet)
# staticmedia = 'opt/bitnami/projects/HSETool/static/media/'
# staticmedia = 'static/media/'

# #closeouttemplate location (used for pdf closeoutprint & indiprint)
# closeouttemplate = '/opt/bitnami/projects/HSETool/closeouttemplate' # Guna same reason removed pdf since want to add approver level
# closeouttemplate = 'closeouttemplate' # Guna Removed .pdf since i want too add approver level to it

# #atrtemplatelocation (used for old pdf generate function in views called closeoutsheet)
# atrtemplate = '/opt/bitnami/projects/HSETool/atrtemplateautofontreadonly.pdf'
# atrtemplate = 'atrtemplateautofontreadonly.pdf'

#closeoutsheet test for one page location
#closeoutest = 'closeoutsheet.pdf' #commented because did not want to push single page template back to main (could result in mistake setting pdf to print to this template instead)
#get host name from where it comes from inside settings

#20211125 from Trackem/urls.py
        #pdf path
        #path('GeneratePDF/',login_required(UserView.pdftest),name='GeneratePDF'),
        #path('ContactUs/',UserView.ContactUs,name='ContactUs'),
        #Guna Commented below to remove at some point
        #path('IndividualBreakdownByUsers/',login_required(UserView.IndividualBreakdownByUsers),name='IndividualBreakdownByUsers'),
        #tenant
        # path('our_team/', login_required(our_team), name='our_team'),
        #path('PDFtest/', UserView.PDFtest, name='PDFtest'),
        #edward added to enable clicking of all actions
        #edward scheduler url
        # path('scheduler/',login_required(UserView.scheduler),name='scheduler'),
        #20211124 commented by Edward because obsolete function moved from views to scrap
        #path('ReportingTable/',login_required(UserView.ReportingTable),name='ReportingTable'),
        #path('Profile/',login_required(UserView.Profile),name='Profile'),
        # path('emailreminders/',login_required(UserView.emailreminders),name='emailreminders'),
        # path('EmailReminderAttachment/',login_required(UserView.EmailReminderAttachment),name='EmailReminderAttachment'),
        #path('EmailReminder/',login_required(UserView.EmailReminder),name='EmailReminder'),


#20211124 from views Edward
# def ReportingTable(request): #edward 20211124 seems like an obselete function 
#     sub = Subscribe()
#     if request.method == 'POST':
#         #Msg=EmailMessage()
#         sub = Subscribe(request.POST)
#         subject = 'Test for sending email overview'
#         message = 'A summary table should present here'
#         recepient = str (sub ['Email'].value())
#         Msg=EmailMessage(subject, message, emailSender, [recepient])
#         Msg.content_subtype="html"
#         Msg.attach_file('C:\\Users\\yh_si\\Desktop\\HSETool-1\\static\\multiple.pdf')
#         Msg.send()
#         context ={
#           'form':sub
#         }
#         return render(request, 'userT/reportingtable.html',context) #yhs changed to small letters
#     return render (request, 'userT/reportingtable.html', {'form':sub}) #yhs changed to small letters


# def Profile (request): #edward 20211124 seems like an obselete function 
#     return render(request, 'userT/profile.html') #yhs changed to small letters
# #def EmailReminder (request):
# #    return render(request, 'userT/EmailReminder.html')

# def emailreminders(request): #edward 20211124 seems like an obselete function, this was moved to management commands where it is called from crontab
#     #sub = Subscribe()
#     emaillist =[]
#     #Get all Actions
#     allactions = ActionItems.objects.all()
#     if (request.POST.get('SendPending')):
#         QueOpen = [0,1,2,3,4,5,6,7,8,9]
#         QueClosed = [99]
#         discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub
#         Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)
#         subject = f"Pending Activities for {paremailphase} Risk Assessment Workshops"
#         content=f"You have Pending Actions in your Queue. Please go to {paremailurl} to attend to the actions."
#         for items in Indisets :
#             if items[3]>0:
#                 emaillist.append(items[0])
#         blemailSendindividual(emailSender,emaillist,subject,content)
#         #below is for the overdue, it is linked to button, just waiting for overdue function
#     elif (request.POST.get('SendOverdue')):

#         subject = f"Pending Activities for {paremailphase} Assessment Workshops"
#         content=f"You have Overdue Actions in your Queue. Please go to {paremailurl} to attend to the actions."
#         blemailSendindividual(emailSender,emaillist,subject,content)

#         return render (request, 'userT/emailreminders.html')
#     return render (request, 'userT/emailreminders.html')

# def EmailReminder(request): #edward 20211124 seems like an obselete function 
#     sub = Subscribe()
#     if request.method == 'POST':

#          #send email, the xyz is dummy data and not used


#         sub = Subscribe(request.POST)
#         recepient = str (sub ['Email'].value())

#         dict_allRou = blgetuserRoutes(recepient)
#         Actionee_R =    dict_allRou.get('Actionee_Routes')
#         ActionCount = blfuncActionCount(Actionee_R,0)

#         totalaction=sum(ActionCount)

#         #Msg=EmailMessage()
#         sub = Subscribe(request.POST)
#         subject = 'Template for Action Pending Responses'
#         message = 'Clients template. Your pending responses are ' + str(totalaction) + ' actions.'

#         Msg=EmailMessage(subject, message, emailSender, [recepient])
#         Msg.content_subtype="html"
#         Msg.send()
#         context ={
#           'form':sub
#         }
#         return render(request, 'userT/EmailReminder.html',context)  #edward to check this.....
#     return render (request, 'userT/emailreminders.html', {'form':sub})

# def EmailReminderAttachment(request): # edward 20211124 this one seems like obselete function since it is attaching some file from HS computer
#     sub = Subscribe()
#     if request.method == 'POST':
#         #Msg=EmailMessage()
#         sub = Subscribe(request.POST)
#         subject = 'Template for sending out weekly report'
#         message = 'Clients weekly report template & attachment.'
#         recepient = str (sub ['Email'].value())
#         Msg=EmailMessage(subject, message, emailSender, [recepient])
#         Msg.content_subtype="html"
#         Msg.attach_file('C:\\Users\yh_si\Desktop\HSETool-1\static\weeklyreporttemplate.pdf')
#         Msg.send()
#         context ={
#           'form':sub
#         }
#         return render(request, 'userT/EmailReminder.html',context)
#     return render (request, 'userT/EmailReminder.html', {'form':sub}) #edward to check this

#20211124 from views Edward

#20211122 from views Edward
# def blallphasegetAction(que,phase=""):
#     '''this function gets all actions and or phases . Pass phase and QueSeries to get count 
#     of items in a list of QueSeries[open,closed etc]'''
#     count = 0

#     for eachQs in que:
#         if phase!="":
#             filters = {'QueSeries':eachQs,'ProjectPhase__ProjectPhase':phase}
#         else:
#             filters = {'QueSeries':eachQs}

#         count += ActionItems.mdlallActionItemsCount.mgr_GeneralItemsCountbyFilters(filters) 
   

#     return count

#obsolete code commented by edward on 20210707 after adding signature field & creating new bl function, to be deleted in one month
# def blgettimestampuserdetails (id, Signatories): 
#         #pass in all Signatories and ID of action
#         #return Signatories with Time Stamp
        
#         #firstgetcurrentqueseries
        
#         lstDictQueSeries = ActionItems.objects.filter(id=id).values('QueSeries')
#         currentQueSeries = lstDictQueSeries[0].get('QueSeries')
        
#         #next get all history that has got to do with ID from history tables
#         #thinking that if you order by decending then you are done by getting latest first
#         lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=currentQueSeries).order_by('-history_date').values()
        
#         finallstoflst = []                                   
#         for index, items in enumerate(Signatories):
            
#             #get each user detail first
#             objuser = CustomUser.objects.filter(email=items[1]).values()
           
#             if objuser:
#                 fullname =   objuser[0].get('fullname')
#                 items.append(fullname)
#                 designation =  objuser[0].get('designation')
#                 items.append(designation)

#             else:
                    
#                 items.append("No User Defined")
            
#             if index < currentQueSeries: 
#                 #get all time stamps for all que series
#                 #index basically denominates Que series level. if Current que series =2 then only actionee = 0 and Approver 1 has signed
#                 lstdictHistory = ActionItems.history.filter(id=id).filter(QueSeries=index).order_by('-history_date').values()
                
#                 if lstdictHistory: #to fix testing bug
#                     timestamp = lstdictHistory[0].get('history_date') # get just the first record assume decending is the way togo
#                 else:
#                     timestamp = []

#                 items.append(timestamp)
                
#                 finallstoflst.append(items)
                
#                 items =[]
            
#             else:
#                 #this simply says that i will give a time stamp for rest of levels to 0- no date and time
                
#                 items.append(0)
#                 finallstoflst.append(items)
#                 items =[]
        
    
#           #que series will decide number of people whom have signed +1 because actionee is 0- Need a matching list index
        
#         return finallstoflst

#edward new signatories for closeoutpreint 20210706
# def blfkattachment(ObjAttach,attachments):

#     for eachfile in ObjAttach: 
#         filename = os.path.basename(eachfile.Attachment.name)
#         attachmentorigin = attachments + filename

#         return attachmentorigin
#this function needs to be fixed
# def googlecharts88(request):


#     lstbyDueDate    = blaggregatebydate(ActionItems.objects.all())

#     lstplanned          = blprepareGoogleChartsfromDict(lstbyDueDate)
#     lstactual           = blgetActualRunDown(lstplanned)
#     newlist             = blformulateRundown(lstplanned,lstactual)

#     for items in lstbyDueDate:

#         x=items.get('DueDate')

#     subtotal =[]
#     for items in lstbyDueDate:
#        subtotal.append(items['count']) #how to access dictionary object by

#     content =  newlist
#     # print(content1)
#     # blstopcharttoday(content1)

# # edward 20210723 end new graphing to stop on current day
# # content2 using hardcoded data for testing
#     # content = [
#     #                 ['2021-06-08', 68, 68],
#     #                 ['2021-06-08', 68, 68],
#     #                 ['2021-07-08', 67, 68],
#     #                 # ['2021-07-09', 62, 65],
#     #                 # ['2021-07-15', 58, 58],
#     #                 # ['2021-07-16', 57, 58],
#     #                 # ['2021-07-20', 57, 58],
#     #                 # ['2021-07-24', 57, 58],
#     #                 ['2021-07-25', 54, 56],
#     #                 ['2021-07-30', 14, 20],
#     #                 # ['2021-08-26', 13, 14],
#     #                 # ['2021-10-15', 10, 12],
#     #                 # ['2021-10-16', 8, 10],
#     #                 # ['2021-10-17', 0, 5]
#     #             ]
#     content1 = blstopcharttoday(content)

#     # strtoday = dt.today().strftime('%Y-%m-%d') #todays date as string
#     # today= dt.today()#.strftime('%Y-%m-%d') #todays date as string
#     # closed =(len(ActionItems.objects.filter(QueSeries=99))) #closed items
#     # TotalActionItems = (len(ActionItems.objects.all())) #total items
#     # actual = (TotalActionItems-closed) # use this to append the actual data
#     # currentdate = [today,' ',actual]
#     # empty=[]

#     # for items in content:
#     #     items[0] = datetime.datetime.strptime(items[0], '%Y-%m-%d').date() # datetime obj has problems bcs comparing down to the minute

#     # if not any(today in items for items in content) :
#     #     content.insert(0,currentdate)
#     #     print("InsertedDate", content)
#     # else :
#     #     content
#     # sortedcontent = sorted(content, key=itemgetter(0)) # itemgetter(0) sorts by first entry inside list of list (date in this case)
#     # print(sortedcontent)

#     # for items in sortedcontent:
#     #     items[0]=items[0].strftime('%Y-%m-%d')
#     #     if items[0]> strtoday:
#     #         items.pop(2)

#     # content = sortedcontent




#     context = {

#         # 'contentplanned' :contentplanned,
#         # 'contentactual' : contentactual
#         'content' : content1




#     }
#     #return JsonResponse()
#     return render(request, 'userT/googlecharts88.html',context) #ok checked by yhs

#Guna using History Form Mixin - Need to delete below
# class HistoryFormApprover(ApproveItemsMixin):

#     template_name = "userT/historyformapprover.html"
#     form_class = frmApproverConfirmation
#     success_url = '/HistoryList/'

#     def get_context_data(self,**kwargs):
#         id = self.object.id #its actually the id and used as foreign key

#         context = super().get_context_data(**kwargs)

#         discsuborg = blgetDiscSubOrgfromID(id)
#         ApproverLevel = blgetApproverLevel(discsuborg)

#         # #sets the signatory directly in getting timestamp
#         Signatories = blgetSignotories(discsuborg)
#         #edward 20210707 trying to use consolidated version blgettimestampuserdetails
#         lstSignatoriesTimeStamp= blgettimestampuserdetails (id, Signatories)
#         object_list = self.object.attachments_set.all()

#         context['object_list'] = object_list
#         context['Rejectcomments'] = Comments.mdlComments.mgrCommentsbyFK(id)
#         context['Approver'] = False
#         context ['ApproverLevel'] = ApproverLevel
#         context ['Signatories'] = lstSignatoriesTimeStamp

#         return context
#     def form_valid(self,form):

#         if (self.request.POST.get('Pullback')):

#             return super().form_valid(form)

#         if (self.request.POST.get('Cancel')):
# #
#            return HttpResponseRedirect('/HistoryList/')

#     def get_success_url(self):
#         return reverse ('HistoryConfirm', kwargs={'id': self.object.id })

# def GeneratePDF (request):
#     filename = [] # for appending filename place before for loop
#     if (request.POST.get('GeneratePDF')):
#         x=ActionItems.objects.all()  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
#         y= x.values()
#         for item in y :
#             i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file
#             j = (i + '.pdf')  # easier to breakdown j
#             del item["id"]
#             data_dict=item
#             x = 'static/multiple.pdf'
#             out_file = 'static/media/' + j   # sending file to media folder inside static folder
#             generated_pdf = pypdftk.fill_form(
#                 pdf_path = x,
#                 datas = data_dict,
#                 out_file = out_file,
#             )
#             filename.append(str(generated_pdf)) #can only append str
#             context={
#                  'filename' : filename,
#                  'table': True
#             }

#         return render(request, 'userT/GeneratePDF.html', context)
#     return render(request, 'userT/GeneratePDF.html')
#20211122 from views Edward

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

#20211027 edward   
# def closeoutsheet(request):
#     filename = [] # for appending filename place before for loop
#     if (request.POST.get('GeneratePDF')):
#         x=ActionItems.objects.filter(StudyName='HAZID')  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')
#         y= x.values()
#         for item in y :
#             i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file
#             j = (i + '.pdf')  # easier to breakdown j
#             del item["id"]
#             data_dict=item
#             out_file = 'static/media/' + j
#             pdfgenerate('atrtemplateautofontreadonly.pdf',out_file,data_dict)
#             filename.append(out_file) #can only append str
#             context={
#                 'filename' : filename,
#                 'table': True
#             }
#             #return HttpResponse('TEST')
#         #     return render(request, 'userT/closeoutsheet.html', context)
#         # return render(request, 'userT/closeoutsheet.html')
#         return render(request, 'userT/closeoutsheet.html', context)
#     return render(request, 'userT/closeoutsheet.html')


# for  making view all actions clickable & obtain the id using update view

#20211027 edward  
# def closeoutsheet1(request):  #edward 20210820 duplicate of closeoutsheet to build bulk upload
#     QueOpen = [0,1,2,3,4,5,6,7,8,9]
#     QueClosed = [99]
#     YetToRespondQue =[0]
#     ApprovalQue = [1,2,3,4,5,6,7,8,9]
#     TotalQue = [0,1,2,3,4,5,6,7,8,9,99]
#     allstudies = Studies.objects.all()

#     tablestudiesheader = ['Studies', 'Yet to Respond' ,'Approval Stage','Closed','Open Actions', 'Total Actions']



#     lstbyWorkshop = blgetbyStdudiesCount(allstudies,YetToRespondQue,ApprovalQue,QueClosed,QueOpen,TotalQue)

#     allactions = ActionItems.objects.all()
#     tableallheader = ['StudyActionNo','StudyName', 'Disipline' ,'Recommendations','Response','InitialRisk'] # Warning donnt change this as this item needs to map against the MODEL
#     lstofallactions = blgetActionStuckAt(allactions, tableallheader) #basically you feed in any sort of actions with tables you want and it will send you back where the actions are stuck at
#     tableallheadermodified =  ['Study Action No','Study Name', 'Discipline' ,'Recommendations','Response','Initial Risk']
#     filename = [] # for appending filename place before for loop

#     #Guna

#     lstclosed = ActionItems.objects.filter(QueSeries =99)

#     if (request.POST.get('GeneratePDF')):
#         x=ActionItems.objects.all()  #the row shall not contain "." because conflicting with .pdf output(typcially in header) /previously used .filter(StudyActionNo__icontains='PSD')

#         y= x.values()
#         for item in y :
#             i = item["StudyActionNo"] # specify +1 for each file so it does not overwrite one file
#             j = (i + '.pdf')  # easier to breakdown j & to append further on
#             del item["id"]
#             data_dict=item
#             out_file = staticmedia + j
#             pdfgenerate(atrtemplate,out_file,data_dict)#returns from pdfgenerator #edward added atrtemplate location in parameters
#             filename.append(j) #can only append str, appending j shows the filename for userview instead of whole location
#             context1={
#                 'filename' : filename,
#                 'table': True,
#                 'lstbyWorkshop' : lstbyWorkshop,
#                 'lstofallactions' : lstofallactions,
#             }
#         return render(request, 'userT/closeoutsheet.html', context1)


#     context = {
#         'lstclosed' : lstclosed,
#         'lstbyWorkshop' : lstbyWorkshop,
#         'lstofallactions' : lstofallactions,
#         'tablestudiesheader' : tablestudiesheader,

#     }

#     return render(request, 'userT/closeoutsheet.html', context)
#edward end 20210820 pdf bulk

#20211027 edward  
#-commented below to remove
# def IndividualBreakdownByUsers(request):
#     #Need to do some maths here  most of the functions have been charted out just need to remap back to individual
#     # 2 functions need to merge
#     discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg() #get all disc sub

#     #Signatories =

#     QueOpen = [0,1,2,3,4,5,6,7,8,9]
#     QueClosed = [99]
#     Indisets = blgetIndiResponseCount(discsuborg,QueOpen,QueClosed)

#     context = {

#         'Indisets' : Indisets,

#     }

#     return render(request, 'userT/indibreakbyuser.html',context) #yhs changed to all small letters