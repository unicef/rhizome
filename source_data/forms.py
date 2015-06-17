from django.forms import forms, CharField, ModelForm
from source_data.models import *

class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )
