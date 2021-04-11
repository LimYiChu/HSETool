from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    Company = forms.CharField(label='COMPANY Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
#Testing for send email
class Subscribe(forms.Form):
    Email = forms.EmailField()

    def __str__(self):
        return self.Email

class EmailReminderDiscipline(forms.Form):
    Discipline = forms.CharField(label='Discipline')

    def __str__(self):
        return self.Discipline
