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
        self.helper.form_read_only = True
        self.helper.layout = Layout(
        Div(
            Div(Field('StudyActionNo',readonly=True),   css_class='col-md-3'), 
            Div (Field('StudyName',readonly=True),  css_class='col-md-3'),
            Div (Field('ProjectPhase', readonly=True), css_class='col-md-3'),
            css_class='row',
          
             
           ),
        Div (
                
            Div (Field('Recomendations', readonly=True), css_class='col-md-9'),
            css_class='row',
            ),
        Div (
                
            Div ('Response', css_class='col-md-9'),
            css_class='row',
            )
        )
    class Meta:
        model = ActionItems
        fields = '__all__'

        StudyActionNo = forms.CharField(disabled=True)