from django.forms import forms, ModelForm
from source_data.models import *
from django.contrib.auth.models import User

class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )


class IndicatorMapForm(ModelForm):

    class Meta:
        model = IndicatorMap
        fields = ['master_indicator','source_indicator']


class RegionMapForm(ModelForm):

    class Meta:
        model = RegionMap
        fields = ['master_region','source_region']

class CampaignMapForm(ModelForm):

    class Meta:
        model = CampaignMap
        fields = ['master_campaign','source_campaign']
