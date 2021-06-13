from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
CustomUser = get_user_model()

class CustomUserSignature(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserSignature, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        #self.helper.add_input(Submit('Upload', 'Upload File & Confirm', css_class='btn btn-outline-dark float-right col-md-2'))
        #self.helper.add_input(Submit('Cancel', 'Cancel', css_class='btn btn-outline-dark float-right col-md-1'))
        
        
        self.helper.layout = Layout(

            Div(
            Div (Field('signature' ), css_class='col-md-12'), 
            Div (Field('email',id="email")),
            Div()
            ),
        )
    
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_active', 'admin'] # third change

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


    
#Testing for send email
class Subscribe(forms.Form):
    Email = forms.EmailField()

    def __str__(self):
        return self.Email

class EmailReminderDiscipline(forms.Form):
    Discipline = forms.CharField(label='Discipline')

    def __str__(self):
        return self.Discipline
