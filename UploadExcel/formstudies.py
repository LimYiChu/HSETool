from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *


#20211222 edward using Layout
class layoutheader(Layout):
    def __init__(self, *args, **kwargs):
        #self.fields['FutureAction'].label = strFutActApprNotes
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
            ),)

class layoutoriginal(Layout):
    def __init__(self, *args, **kwargs):
        #self.fields['FutureAction'].label = strFutActApprNotes
        
        super().__init__( 
            
            Div (
            
            Div (Field('Cause', rows=8 ,readonly=True), css_class='col-md-12'),
            Div (Field('Safeguard', rows=8, readonly=True), css_class='col-md-12'),
            Div (Field('Consequence',rows=8, readonly=True), css_class='col-md-12'),
            Div (Field('Recommendations',rows=8, readonly=True), css_class='col-md-12'),
            Div ('Response', required=True, css_class='col-md-12'),
            Div ('FutureAction', css_class='col-md-12'), # - Leave it in here for now need to add to common layout if they agree
            css_class='row',# aligns to left
            ),
            )
        

class layouthazid(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(
            Div (
            Div (Field('NodeNo', rows=1 ,readonly=True), css_class='col-md-2'),
            Div (Field('NodeDescription', rows=1 ,readonly=True), css_class='col-md-2'),
            Div (Field('PreventiveSafeguard', rows=1 ,readonly=True), css_class='col-md-4'),
            Div (Field('MitigativeSafeguard', rows=1 ,readonly=True), css_class='col-md-4'),
            css_class='row',# aligns to left
            ),)



class frmheader(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmheader, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
        layoutheader())
        
    class Meta:
        model = ActionItems
        fields = '__all__'

class frmoriginalbase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmoriginalbase, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
        layoutheader(),layoutoriginal())
        
    class Meta:
        model = ActionItems
        fields = '__all__'

class frmhazid(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(frmhazid, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
        layoutheader(),layouthazid(),layoutoriginal())

    class Meta:
        model = ActionItems
        fields = '__all__'

class frmhazidapprover(frmhazid):
    
    def __init__(self, *args, **kwargs):
        super(frmhazidapprover, self).__init__(*args, **kwargs)
        self.fields['Response'].widget.attrs['readonly'] = True
        self.fields['FutureAction'].widget.attrs['readonly'] = True

class frmoriginalbaseapprover(frmoriginalbase):
    
    def __init__(self, *args, **kwargs):
        super(frmoriginalbaseapprover, self).__init__(*args, **kwargs)
        self.fields['Response'].widget.attrs['readonly'] = True
        self.fields['FutureAction'].widget.attrs['readonly'] = True
     
