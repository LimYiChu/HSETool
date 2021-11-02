
#edward created new parameter file 
from Trackem.settings import *
from .models import *
#url-links
cclist = ["ehstools@prism-ehstools.awsapps.com"]#cclist to send a copy of email to ehstools email since there is no record of sent mail for emails sent by system
#appurl = "https://sapuraphase4a.prism-ehstools.com"#for now, please change appurl for different clients
emailSender ="ehstools@prism-ehstools.awsapps.com"#used in views for email sender origin address
#urllist = ["http://test.prism-ehstools.com","https://sapuraphase3.prism-ehstools.com","https://sapuraphase4a.prism-ehstools.com","https://prism.prism-ehstools.com"]
#this is to enable different parameters to be provided for different hosts. This for loop is to specify the parameters in email headers & email message(emailreminders in views.py) based on different urls.
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
 

#Paramters to simply views.py . Commonly used parameters in Views.py to be parked here and standardised

 
QueOpen = [0,1,2,3,4,5,6,7,8,9]
QueClosed = [99]
YetToRespondQue =[0]
ApprovalQue = [1,2,3,4,5,6,7,8,9]
TotalQue = [0,1,2,3,4,5,6,7,8,9,99]
# discsuborg = ActionRoutes.mdlAllDiscSub.mgr_getDiscSubOrg()
# discsub = ActionRoutes.mdlAllDiscSub.mgr_getDiscSub()
# organisationnames = ActionRoutes.mdlAllCompany.mgr_getOrgnames()


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

# ***dataframes constants edward 20210804
dfallcolumns=['StudyActionNo','StudyName','Disipline','Recommendations', 'Response','DueDate','InitialRisk','RiskColour']
dfcompletecolumns=['StudyActionNo','StudyName','ProjectPhase','Facility','Guidewords','Deviation', 'Cause', 'Consequence', 'Safeguard','InitialRisk','ResidualRisk','Recommendations','DueDate', 'Response','FutureAction','Organisation','Disipline','Subdisipline','Actionee','Action with','Revision'] # 'RiskColour',
dfcompletecolumns2=['StudyActionNo','StudyName','ProjectPhase','Facility','Guidewords','Deviation', 'Cause', 'Consequence', 'Safeguard','InitialRisk','ResidualRisk','Recommendations','DueDate', 'Response','FutureAction','Organisation','Disipline','Subdisipline']
dfrejectedcolumns = ['StudyActionNo','StudyName','ProjectPhase','Facility','Cause','Safeguard','InitialRisk','ResidualRisk','Recommendations','Organisation','Disipline','Subdisipline','Guidewords','Revision','RiskColour']
dfindisummcolumns = ["User","Pending Submission","Pending Approval"]