from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
class UploadExlForm(forms.ModelForm):
    class Meta:
        model = UploadExl
        fields = '__all__'

class CommonLayout (Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(

            Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-3'), 
            Div (Field('StudyName',readonly=True),  css_class='col-md-3'),
            Div (Field('ProjectPhase', readonly=True), css_class='col-md-6'),
            #Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
                      
           ),
            Div (
            Div (Field('Cause', readonly=True), css_class='col-md-12'),
            Div (Field('Safeguard', readonly=True), css_class='col-md-12'),
            Div (Field('Consequence', readonly=True), css_class='col-md-12'),
            Div (Field('Recomendations', readonly=True), css_class='col-md-12'),
            css_class='row',#-dont know why i have to put this in so it aligns to left
            
            ),
#needs these hidden fields otherwise it passes blank values into the model- need to see if can do some other way
            Div (
                
            Div (Field('Facility', type="hidden")),
            Div (Field('InitialRisk', type="hidden")),
            Div (Field('ResidualRisk', type="hidden")),
            Div (Field('Disipline', type="hidden")),
            Div (Field('Subdisipline', type="hidden")),
            Div (Field('Organisation', type="hidden")),
           Div (Field('QueSeries', type="hidden")),
    
            ),
        )
class UpdateActioneeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateActioneeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit for Approval', css_class='btn-primary float-right'))

        self.helper.layout = Layout(
        CommonLayout(),
        
        Div (
                
            Div ('Response', css_class='col-md-12'),
            Div ('Attachment', css_class='col-md-12'),
            Div ('FutureAction', css_class='col-md-12'),
            css_class='row',
            ),
      
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

class ApproverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApproverForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('Approve', 'Approve for Next Level', css_class='btn-primary float-right'))
        self.helper.add_input(Submit('Reject', 'Reject', css_class='btn-primary float-right'))
        self.helper.layout = Layout(
        CommonLayout(),
        Div(
            Div (Field('Response',readonly=True) ,css_class='col-md-12'), 
            Div (Field('Attachment',disable=True),  css_class='col-md-12'),
            Div (Field('FutureAction', readonly=True), css_class='col-md-12'),
            #Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
          
           ),
        )
    class Meta:
        model = ActionItems
        fields = '__all__'
    