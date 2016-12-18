from django import forms
from django.forms import ModelForm
from .models import EoooStudent, EoooDistributedto, EoooFapackage
from .choices import *
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100)

'''class DistributePackageForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    package_id = forms.IntegerField(required=True)
    amount = forms.DecimalField(required=True)
    grant_type = forms.ChoiceField(choices=PACKAGE_OPTIONS,required=True)
    date = forms.DateField(required=True)
'''
class LoginUserForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=30, widget=forms.PasswordInput)

class DistributePackageForm(ModelForm):
    class Meta:
        model = EoooDistributedto
        fields = [
        'studentid', 'fapackageid', 'ddate'
        ]
        widgets = {
        'student_id':forms.NumberInput(attrs={'class':'student_id'}),
        'package_id':forms.NumberInput(attrs={'class':'package_id'}),
        'date':forms.DateTimeInput(attrs={'class':'date'}),
        }
        labels = {
        'studentid':_('Student I.D.'),
        'fapackageid':_('Package I.D.'),
        'ddate':_('Distribution Date'),
        }


        '''model = EoooFapackage
        fields = [
        'packageid', 'ptype', 'amount']
        widgets = {
        'packageid':forms.NumberInput(attrs={'class':'package_id'}),
        'ptype':forms.TextInput(attrs={'class':'package_type'}),
        'amount':forms.NumberInput(attrs={'class':'amount'}),
        }'''
class AddStudentForm(ModelForm):
    class Meta:
        model = EoooStudent
        fields = [
         'ssn', 'academic_standing', 'fname',
         'lname','street','city','state','zip','phone_number',
         'sex','income_status']
        widgets = {
        #'student_id':forms.NumberInput(attrs={'class':'student_id'}),
        'ssn':forms.NumberInput(attrs={'class':'ssn'}),
        'academic_standing':forms.TextInput(attrs={'class':'academic_standing'}),
        'fname':forms.TextInput(attrs={'class':'fname'}),
        #'mname':forms.TextInput(attrs={'class':'mname'}),
        'lname':forms.TextInput(attrs={'class':'lname'}),
        'street':forms.TextInput(attrs={'class':'street'}),
        'city':forms.TextInput(attrs={'class':'city'}),
        'state':forms.TextInput(attrs={'class':'state'}),
        'zip':forms.NumberInput(attrs={'class':'zip'}),
        'phone_number':forms.NumberInput(attrs={'class':'phone_number'}),
        'sex':forms.TextInput(attrs={'class':'sex'}),
        'income_status':forms.TextInput(attrs={'class':'income_status'}),
        }
        labels = {
        #'student_id':_('ID'),
        'ssn':_('SSN'),
        'academic_standing':_('Standing'),
        'fname':_('First'),
        'lname':_('Last'),
        'street':_('Street'),
        'city':_('City'),
        'state':_('State'),
        'zip':_('Zip'),
        'phone_number':_('Phone'),
        'sex':_('Sex'),
        'income_status':_('Income Status'),

        }
