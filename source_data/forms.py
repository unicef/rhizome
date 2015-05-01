from django.forms import forms, CharField, ModelForm
from source_data.models import *

class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )
class IndicatorMapForm(ModelForm):

    class Meta:
        model = IndicatorMap
        fields = ['source_object','master_object']


class RegionMapForm(ModelForm):

    class Meta:
        model = RegionMap
        fields = ['source_object','master_object']


class CampaignMapForm(ModelForm):

    class Meta:
        model = CampaignMap
        fields = ['source_object','master_object']
