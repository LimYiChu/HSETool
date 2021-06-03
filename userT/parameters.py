#edward created new parameter file 
from Trackem.settings import *
#url-links
cclist = ["ehstools@prism-ehstools.awsapps.com"]#cclist to send a copy of email to ehstools email since there is no record of sent mail for emails sent by system
appurl = "https://sapuraphase4a.prism-ehstools.com"#for now, please change appurl for different clients
emailSender ="ehstools@prism-ehstools.awsapps.com"#used in views for email sender origin address

#file directories
for items in ALLOWED_HOSTS :

    if items.find('.prism-ehstools.com') >= 0 : #it finds in list 
        tempfolder = '/opt/bitnami/projects/HSETool/static/media/temp/'#temp folder location (used for pdf closeoutprint & indiprint)
        staticmedia = '/opt/bitnami/projects/HSETool/static/media/'#static/media folder location (used for old pdf generate function in views called closeoutsheet)
        closeouttemplate = '/opt/bitnami/projects/HSETool/closeouttemplate.pdf'#closeouttemplate location (used for pdf closeoutprint & indiprint)
        atrtemplate = '/opt/bitnami/projects/HSETool/atrtemplateautofontreadonly.pdf'#atrtemplatelocation (used for old pdf generate function in views called closeoutsheet)

    else :
        tempfolder = 'static/media/temp/'
        staticmedia = 'static/media/'
        closeouttemplate = 'closeouttemplate.pdf'
        atrtemplate = 'atrtemplateautofontreadonly.pdf'

# for items in ALLOWED_HOSTS :

#     if items.find('.prism-ehstools.com') >= 0 :
#         tempfolder = '/opt/bitnami/projects/HSETool/static/media/temp/'#temp folder location (used for pdf closeoutprint & indiprint)
#         staticmedia = '/opt/bitnami/projects/HSETool/static/media/'#static/media folder location (used for old pdf generate function in views called closeoutsheet)
#         closeouttemplate = '/opt/bitnami/projects/HSETool/closeouttemplate.pdf'#closeouttemplate location (used for pdf closeoutprint & indiprint)
#         atrtemplate = '/opt/bitnami/projects/HSETool/atrtemplateautofontreadonly.pdf'#atrtemplatelocation (used for old pdf generate function in views called closeoutsheet)
#     elif items.find('host') >= 0 :
#         tempfolder = 'static/media/temp/'
#         staticmedia = 'static/media/'
#         closeouttemplate = 'closeouttemplate.pdf'
#         atrtemplate = 'atrtemplateautofontreadonly.pdf'

# #static/media folder location (used for old pdf generate function in views called closeoutsheet)
# staticmedia = 'opt/bitnami/projects/HSETool/static/media/'
# staticmedia = 'static/media/'

# #closeouttemplate location (used for pdf closeoutprint & indiprint)
# closeouttemplate = '/opt/bitnami/projects/HSETool/closeouttemplate.pdf'
# closeouttemplate = 'closeouttemplate.pdf'

# #atrtemplatelocation (used for old pdf generate function in views called closeoutsheet)
# atrtemplate = '/opt/bitnami/projects/HSETool/atrtemplateautofontreadonly.pdf'
# atrtemplate = 'atrtemplateautofontreadonly.pdf'

#closeoutsheet test for one page location
#closeoutest = 'closeoutsheet.pdf' #commented because did not want to push single page template back to main (could result in mistake setting pdf to print to this template instead)
#get host name from where it comes from inside settings
