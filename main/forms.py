from django import forms
from main.models import DataBaseFile

class DataBaseFileForm(forms.ModelForm):
    '''
    Form to manage db files
    '''
    class Meta:
        model = DataBaseFile