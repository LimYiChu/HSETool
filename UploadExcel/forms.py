from django import forms
from .models import UploadExl

class UploadExlForm(forms.ModelForm):
    class Meta:
        model = UploadExl
        fields = '__all__'
