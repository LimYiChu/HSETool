from django import forms
from .models import *
from crispy_forms.helper import FormHelper
class UploadExlForm(forms.ModelForm):
    class Meta:
        model = UploadExl
        fields = '__all__'

class UpdateActioneeForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
    class Meta:
        model = ActionItems
        fields = '__all__'

        StudyActionNo = forms.CharField(disabled=True)