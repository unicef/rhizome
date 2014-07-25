from django.db import models
from django.forms import ModelForm, forms, ModelChoiceField
from datapoints.models import *
from django.contrib.auth.models import User

class RegionForm(ModelForm):

    class Meta:
        model = Region
        # fields = ['full_name','short_name']

class IndicatorForm(ModelForm):

    class Meta:
        model = Indicator

class DataPointForm(ModelForm):

    class Meta:
        model = DataPoint
        fields = ['indicator','region', 'campaign', 'value']

class CampaignForm(ModelForm):

    class Meta:
        model = Campaign

class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )

class DataPointSearchForm(forms.Form):
    region = ModelChoiceField(queryset=Region.objects.all())
    indicator = ModelChoiceField(queryset=Indicator.objects.all())
    campaign = ModelChoiceField(queryset=Campaign.objects.all())
    changed_by = ModelChoiceField(queryset=User.objects.all())
