
#edward created new parameter file 
from Trackem.settings import *
from .models import *
#url-links
cclist = ["ehstools@prism-ehstools.awsapps.com"]#cclist to send a copy of email to ehstools email since there is no record of sent mail for emails sent by system
#appurl = "https://sapuraphase4a.prism-ehstools.com"#for now, please change appurl for different clients
emailSender ="ehstools@prism-ehstools.awsapps.com"#used in views for email sender origin address
#urllist = ["http://test.prism-ehstools.com","https://sapuraphase3.prism-ehstools.com","https://sapuraphase4a.prism-ehstools.com","https://prism.prism-ehstools.com"]
#this is to enable different parameters to be provided for different hosts. This for loop is to specify the parameters in email headers & email message(emailreminders in views.py) based on different urls.
global urlglobal 
urlglobal ="Test12343"
for items in ALLOWED_HOSTS:
    if items.find('test')>=0 :
        paremailurl = "http://test.prism-ehstools.com"
        paremailphase ="test"
    elif items.find('sapuraphase3')>=0  :
        paremailurl = "https://sapuraphase3.prism-ehstools.com"
        paremailphase ="Phase 3"
    elif items.find('sapuraphase4a')>=0 :
        paremailurl = "https://sapuraphase4a.prism-ehstools.com"
        paremailphase ="Phase 4a"
    elif items.find('127.0.0.1')>=0:
        paremailurl = "127.0.0.1:8000"
        paremailphase ="localhost"
    else:
        paremailurl = "https://prism.prism-ehstools.com"
        paremailphase ="Prism"

#following parameters to differentiate between aws & localhost, hence not url sensitive
for items in ALLOWED_HOSTS :
    
    if items.find('.prism-ehstools.com') >= 0 : #it finds in list 
        tempfolder = '/opt/bitnami/projects/HSETool/static/media/temp/'#temp folder location (used for pdf closeoutprint & indiprint)
        staticmedia = '/opt/bitnami/projects/HSETool/static/media/'#static/media folder location (used for old pdf generate function in views called closeoutsheet)
        closeouttemplate = '/opt/bitnami/projects/HSETool/closeouttemplate'#closeouttemplate location (used for pdf closeoutprint & indiprint)
        atrtemplate = '/opt/bitnami/projects/HSETool/atrtemplateautofontreadonly.pdf'#atrtemplatelocation (used for old pdf generate function in views called closeoutsheet)
        # pdf bulk directory
        bulkpdfdir = "/opt/bitnami/projects/HSETool/static/media/temp/bulkpdf/"
        bulkpdfcreatezipfilename = "/opt/bitnami/projects/HSETool/static/media/temp/" + "bulkpdffiles"
        bulkdlattachments = '/opt/bitnami/projects/HSETool/media/attachments/'
        bulkpdfzip = '/opt/bitnami/projects/HSETool/static/media/temp/bulkpdffiles.zip'   
        stitchedpdf = '/opt/bitnami/projects/HSETool/static/test/mergepdffolder/testingmerge.pdf' 
        #20220120 edward
        hazidcloseouttemplate = '/opt/bitnami/projects/HSETool/hazidcloseouttemplate'#closeouttemplate location (used for pdf closeoutprint & indiprint)
        #20220517 Ying Ying
        # studytemp = '/opt/bitnami/projects/HSETool/static/media/studybulkpdfdir/' 
        # bystudypdfdir = "/opt/bitnami/projects/HSETool/static/media/studybulkpdfdir/studybulkpdf/" 
        # bystudypdfcreatezipfilename = "/opt/bitnami/projects/HSETool/static/media/studybulkpdfdir/" + "studypdffiles"
        # studypdfzip = '/opt/bitnami/projects/HSETool/static/media/studybulkpdfdir/studypdffiles.zip' 
        # blankzip = '/opt/bitnami/projects/HSETool/static/media/studybulkpdfdir/blank.zip'
        # blankzipdir = '/opt/bitnami/projects/HSETool/static/media/studybulkpdfdir/blank/' 
        # 20220608 Ying Ying
        pdfbystudy = '/opt/bitnami/projects/HSETool/static/media/pdfbystudy/' 
        paraOmitAdmin = 1    

    else :
        tempfolder = 'static/media/temp/'
        staticmedia = 'static/media/'
        closeouttemplate = 'closeouttemplate'
        atrtemplate = 'atrtemplateautofontreadonly.pdf'  
        # pdf bulk directory
        bulkpdfdir = "static/media/temp/bulkpdf/"
        bulkpdfcreatezipfilename = "static/media/temp/" + "bulkpdffiles" #can be just slash   
        bulkdlattachments = 'media/attachments/'  
        bulkpdfzip = 'static/media/temp/bulkpdffiles.zip'  
        stitchedpdf =  'static/test/mergepdffolder/testingmerge.pdf' 
        #20220120 edward
        hazidcloseouttemplate = 'hazidcloseouttemplate'   
        #20220517 Ying Ying
        # studytemp = 'static/media/studybulkpdfdir/' 
        # bystudypdfdir = "static/media/studybulkpdfdir/studybulkpdf/"   
        # bystudypdfcreatezipfilename = "static/media/studybulkpdfdir/" + "studypdffiles"  
        # studypdfzip = 'static/media/studybulkpdfdir/studypdffiles.zip'
        # blankzip = 'static/media/studybulkpdfdir/blank.zip'   
        # blankzipdir = 'static/media/studybulkpdfdir/blank/' 
        # 20220608 Ying Ying
        pdfbystudy = 'static/media/pdfbystudy/' 
        paraOmitAdmin = 99     #change according to local admin  

                                                                                                                                    
 

#Paramters to simply views.py . Commonly used parameters in Views.py to be parked here and standardised

 
QueOpen = [0,1,2,3,4,5,6,7,8,9]
QueClosed = [99]
YetToRespondQue =[0]
ApprovalQue = [1,2,3,4,5,6,7,8,9]
TotalQue = [0,1,2,3,4,5,6,7,8,9,99]

# ***dataframes constants edward 20210804
dfallcolumns=['StudyActionNo', 'StudyName', 'Disipline', 'Recommendations', 'Response', 'DueDate', 'InitialRisk', 'RiskColour']
dfcompletecolumns=['StudyActionNo', 'StudyName', 'ProjectPhase', 'Facility', 'Guidewords', 'Deviation', 'Cause', 'Consequence', 'Safeguard', 'InitialRisk', 'ResidualRisk', 'Recommendations', 'DueDate', 'Response', 'FutureAction', 'Organisation', 'Disipline', 'Subdisipline', 'Actionee', 'ActionAt', 'Revision'] # 'RiskColour',
dfcompletecolumns2=['StudyActionNo', 'StudyName', 'ProjectPhase', 'Facility', 'Guidewords', 'Deviation', 'Cause', 'Consequence', 'Safeguard', 'InitialRisk', 'ResidualRisk', 'Recommendations', 'DueDate', 'Response', 'FutureAction', 'Organisation', 'Disipline', 'Subdisipline']
dfrejectedcolumns = ['StudyActionNo', 'StudyName', 'ProjectPhase', 'Facility', 'Cause', 'Safeguard', 'InitialRisk', 'ResidualRisk', 'Recommendations', 'Organisation', 'Disipline', 'Subdisipline', 'Guidewords', 'Revision', 'RiskColour']
dfindisummcolumns = ["User", "Pending Submission", "Pending Approval"]
#20220120 edward 
dfstudiescolumns = ['StudyActionNo', 'DueDate', 'ActionAt', 'discsuborg', 'InitialRisk', 'id', 'RiskColour']
dfdisciplinecolumns = ['StudyActionNo', 'StudyName__StudyName', 'DueDate', 'ActionAt', 'InitialRisk', 'id']
dfindisummcolumns =  ['StudyActionNo', 'DueDate', 'StudyName__StudyName', 'ActionAt', 'InitialRisk', 'id', 'RiskColour']
#202220216 edward
dfdonutcolumns = ['Closed Action', 'Open Action']
#202220425 yingying
indisumm_parameter = ['Role', 'Organisation Route', 'Pending Submission', 'Pending Approval', 'Closed', 'Open Actions']
#06052022 yingying
dfrejectedexcelcolumns = ['StudyActionNo', 'StudyName', 'Org/Disc/Sub-Disc','Cause','Recommendations', 'DueDate', 'InitialRisk', 'RiskColour', 'Response','Revision']
dfallcolumnsupdate=['StudyActionNo', 'StudyName', 'ProjectPhase', 'Org/Disc/Sub-Disc', 'Recommendations', 'Response', 'DueDate', 'InitialRisk', 'RiskColour','ActionAt']