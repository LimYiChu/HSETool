from django.core.mail import EmailMessage

def emailSendindividual(sender,recipient, subject,content):

    subject = subject
    message = content
   
    Msg=EmailMessage(subject, message,sender, recipient)
    Msg.content_subtype="html"
    
    Msg.send()