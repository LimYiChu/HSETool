from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
class UploadExlForm(forms.ModelForm):
    class Meta:
        model = UploadExl
        fields = '__all__'

class UpdateActioneeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateActioneeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit Now', css_class='btn-primary '))

        self.helper.layout = Layout(
        Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-3'), 
            Div (Field('StudyName',readonly=True),  css_class='col-md-3'),
            Div (Field('ProjectPhase', readonly=True), css_class='col-md-3'),
            Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
          
             
           ),
        Div (
            Div (Field('Cause', readonly=True), css_class='col-md-9'),
            Div (Field('Safeguard', readonly=True), css_class='col-md-9'),
            Div (Field('Consequence', readonly=True), css_class='col-md-9'),
            Div (Field('Recomendations', readonly=True), css_class='col-md-9'),
            css_class='row',
            
            ),
        Div (
                
            Div ('Response', css_class='col-md-9'),
            Div ('Attachment', css_class='col-md-9'),
            Div ('FutureAction', css_class='col-md-9'),
            # testing using cryspy formDiv ('email', css_class='col-md-9'),
            css_class='row',

            ),

        Div (
                
            Div (Field('Facility', type="hidden")),
            Div (Field('InitialRisk', type="hidden")),
            Div (Field('ResidualRisk', type="hidden")),
            Div (Field('Disipline', type="hidden")),
            Div (Field('Subdisipline', type="hidden")),
            Div (Field('Organisation', type="hidden")),
           Div (Field('QueSeries', type="hidden")),
    
      
            
            )
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

        #StudyActionNo = forms.CharField(disabled=True)

class ApproverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApproverForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Approve Now', css_class='btn-primary'))

        self.helper.layout = Layout(
        Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-3'), 
            Div (Field('StudyName',readonly=True),  css_class='col-md-3'),
            Div (Field('ProjectPhase', readonly=True), css_class='col-md-3'),
            Div (Field('QueSeries', readonly=True), css_class='col-md-3'),
           #-somehow not working Div (Field('DueDate', readonly=True), css_class='col-md-2'),
            css_class='row',
          
             
           ),
        Div (
            Div (Field('Cause', readonly=True), css_class='col-md-9'),
            Div (Field('Safeguard', readonly=True), css_class='col-md-9'),
            Div (Field('Consequence', readonly=True), css_class='col-md-9'),
            Div (Field('Recomendations', readonly=True), css_class='col-md-9'),
            css_class='row',
            
            ),
        Div (
                
            Div ('Response', css_class='col-md-9'),
            Div ('Attachment', css_class='col-md-9'),
            Div ('FutureAction', css_class='col-md-9'),
            css_class='row',
            ),

     
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

        #StudyActionNo = forms.CharField(disabled=True)