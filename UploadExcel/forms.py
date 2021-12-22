from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
strFutActApprNotes = "Future Actions (Actionee)"

class UploadExlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadExlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        #self.helper.add_input(Submit('Upload', 'Upload File & Confirm', css_class='btn btn-outline-dark float-right col-md-2'))
        #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn btn-outline-dark float-right col-md-1'))
        
        
        self.helper.layout = Layout(

            Div(
            Div (Field('Filename', type="file" ,size="50", id="filename", name="filename", ), css_class='col-md-12'), 
            Div (Field('Username', type="hidden")),
            Div()
            ),
        )
    
    class Meta:
        model = UploadExl
        fields = '__all__'

class UploadField(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadField, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        #self.helper.add_input(Submit('Upload', 'Upload File & Confirm', css_class='btn btn-outline-dark float-right col-md-2'))
        #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn btn-outline-dark float-right col-md-1'))
        
        
        self.helper.layout = Layout(

            Div(
            Div (Field('Field', type="file" ,size="50", id="filename", name="filename", ), css_class='col-md-12'), 
            Div (Field('Username', type="hidden")),
            Div()
            ),
        )

class CommonLayout (Layout):
    
    def __init__(self, *args, **kwargs):
        super().__init__(
            
            Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-2'), #style="font-family: Dancing Script",
            Div (Field('StudyName',readonly=True,disabled=True),  css_class='col-md-3 read-only'),
            Div (Field('ProjectPhase', readonly=True,disabled=True), css_class='col-md-3'), #,disabled=True
            Div (Field('InitialRisk', readonly=True), css_class='col-md-2'),
            Div (Field('ResidualRisk', readonly=True), css_class='col-md-2'),
            Div (Field('StudyName',readonly=True,type="hidden")),
            Div (Field('ProjectPhase',readonly=True,type="hidden")),
            #Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
                      
           ),
            Div (
            Div (Field('Guidewords', rows=1 ,readonly=True), css_class='col-md-5'),
            Div (Field('Deviation', rows=1 ,readonly=True), css_class='col-md-5'),
            Div (Field('Revision', rows=1 ,readonly=True), css_class='col-md-2'),
            Div (Field('Cause', rows=8 ,readonly=True), css_class='col-md-12'),
            Div (Field('Safeguard', rows=8, readonly=True), css_class='col-md-12'),
            #Div (Field('Consequence',rows=8, readonly=True,  style="font-family: Great Vibes;font-size: 60px"),  css_class='col-md-12'), #- Left this commented as it shows how to add style to text box directly
            Div (Field('Consequence',rows=8, readonly=True), css_class='col-md-12'),
            Div (Field('Recommendations',rows=8, readonly=True), css_class='col-md-12'),
            css_class='row',# aligns to left
            
            ),
        
            Div (
                
            Div (Field('Facility', type="hidden")),
            Div (Field('DueDate', type="hidden")), 
            Div (Field('Disipline', type="hidden")),
            Div (Field('Subdisipline', type="hidden")),
            Div (Field('Organisation', type="hidden")),
            Div (Field('StudyName_backup', type="hidden")),
           Div (Field('QueSeries', type="hidden")),
    
            ),
        )
class frmBase (forms.ModelForm):
    def __init__(self, *args, **kwargs):
     super().__init__(
            
            Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-2'), #style="font-family: Dancing Script",
            Div (Field('StudyName',readonly=True,disabled=True),  css_class='col-md-3 read-only'),
            Div (Field('ProjectPhase', readonly=True,disabled=True), css_class='col-md-3'), #,disabled=True
            Div (Field('InitialRisk', readonly=True), css_class='col-md-2'),
            Div (Field('ResidualRisk', readonly=True), css_class='col-md-2'),
            Div (Field('StudyName',readonly=True,type="hidden")),
            Div (Field('ProjectPhase',readonly=True,type="hidden")),
            css_class='row',
                      
           ),)

class frmActioneeGeneral(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmActioneeGeneral, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.fields['FutureAction'].label = strFutActApprNotes
        self.helper.form_method = 'POST'
        self.fields['Response'].required = True 
        #self.helper.add_input(Submit('Upload', 'Next...', css_class='btn btn-outline-dark float-right col-md-1'))
        #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn btn-outline-dark float-right col-md-1'))

        self.helper.layout = Layout(
        CommonLayout(),
        
        Div (
                
            Div ('Response', required=True, css_class='col-md-12'),
            #Div ('Attachment', css_class='col-md-12'),
            Div ('FutureAction', css_class='col-md-12'), # - Leave it in here for now need to add to common layout if they agree
            css_class='row',
            ),
      
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

class frmApproverGeneral(frmActioneeGeneral):
    
    def __init__(self, *args, **kwargs):
        super(frmApproverGeneral, self).__init__(*args, **kwargs)
        self.fields['Response'].widget.attrs['readonly'] = True
        self.fields['FutureAction'].widget.attrs['readonly'] = True

class ApproverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApproverForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_enctype = 'multipart/form-data'
        self.fields['FutureAction'].label = strFutActApprNotes
        self.helper.form_method = 'POST'
        #self.helper.add_input(Submit('Reject', 'Reject', css_class='btn-primary float-right'))
        #self.helper.add_input(Submit('Approve', 'Approve & Sign', css_class='btn-primary float-right'))
        self.helper.layout = Layout(
        CommonLayout(),
        Div(
            Div (Field('Response',readonly=True) ,css_class='col-md-12'), 
            #Div (Field('Attachment',disable=True),  css_class='col-md-12'),
            Div (Field('FutureAction', readonly=True), css_class='col-md-12'),
            
            css_class='row',
          
           ),
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

class frmApproverConfirmation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmApproverConfirmation, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_method = 'POST'
        self.fields['FutureAction'].label = strFutActApprNotes
        #self.helper.add_input(Submit('Reject', 'Reject', css_class='btn-primary float-right'))
        #self.helper.add_input(Submit('Approve', 'Approve & Sign', css_class='btn-primary float-right'))
        self.helper.layout = Layout(
        Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-2'), 
            Div (Field('StudyName',readonly=True,disabled=True),  css_class='col-md-3'),
            Div (Field('ProjectPhase', readonly=True,disabled=True), css_class='col-md-3'),
            Div (Field('InitialRisk', readonly=True), css_class='col-md-2'),
            Div (Field('ResidualRisk', readonly=True), css_class='col-md-2'),
            Div (Field('StudyName',readonly=True,type="hidden")),
            Div (Field('ProjectPhase',readonly=True,type="hidden")),
            #Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
        ),
        Div(
            Div (Field('Recommendations',readonly=True) ,css_class='col-md-12'), 
            #Div (Field('Attachment',disable=True),  css_class='col-md-12'),
            Div (Field('Response', readonly=True), css_class='col-md-12'),
            Div (Field('FutureAction', readonly=True),css_class='col-md-12'),
            #Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
          
           ),
        Div (Field('Cause', type="hidden")),
         
         #Div (Field('DueDate', type="hidden")),
            Div (Field('Safeguard', type="hidden")),
            Div (Field('Consequence', type="hidden")),
             Div (Field('StudyName_backup', type="hidden")),
           #Div (Field('FutureAction', type="hidden")),
           Div (Field('Facility', type="hidden")),
            Div (Field('Disipline', type="hidden")),
            Div (Field('Subdisipline', type="hidden")),
            Div (Field('Organisation', type="hidden")),
            Div (Field('QueSeries', type="hidden")),
            Div (Field('DueDate', type="hidden")), #yhs added for testing disappearing duedates
            Div (Field('Guidewords', type="hidden")), #yhs added due to additional field from client
            Div (Field('Deviation', type="hidden")),
            Div (Field('Revision', type="hidden")), 
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

class frmAddRejectReason(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmAddRejectReason, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #self.fields['Reason'].required = True        #yhs added. 
        self.helper.form_method = 'POST'
        #self.helper.add_input(Submit('Reject', 'Reject with Comments', css_class='btn-primary float-right'))
        #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn-primary float-right'))
        self.helper.layout = Layout(

            Div(
            Div (Field('Reason'), required=True, css_class='col-md-12'),  
            Div (Field('Attachment'), required=True, css_class='col-md-12'),   #yhs added requierd =true
            Div (Field('Username', type="hidden")),
            
            ),
        )
    
    class Meta:
        model = Comments
        fields = ('Reason','Attachment','Username')

class frmMultipleFiles(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmMultipleFiles, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        #self.helper.add_input(Submit('Upload', 'Upload File & Confirm', css_class='btn btn-outline-dark float-right col-md-2'))
        #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn btn-outline-dark float-right col-md-1'))
        
        
        self.helper.layout = Layout(

            Div(
            Div (Field('Attachment', type="file" ,multiple="true",size="50", id="Attachment", onchange="javascript:updateList()"), css_class='col-md-12'), 
            Div (Field('Username', type="hidden")),
            Div()
            ),
        )
    
    class Meta:
        model = Attachments
        fields = ('Attachment','Username')

