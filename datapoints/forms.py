from django.db import models
from django.forms import ModelForm, forms
from datapoints.models import *

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
        fields = ['indicator','region', 'reporting_period', 'value']


class ReportingPeriodForm(ModelForm):
    class Meta:
        model = ReportingPeriod

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )
