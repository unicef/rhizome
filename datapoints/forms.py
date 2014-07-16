from django.db import models
from django.forms import ModelForm
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


