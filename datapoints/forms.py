from django.db import models
from django.forms import ModelForm
from datapoints.models import Region, Indicator


class RegionForm(ModelForm):
    class Meta:
        model = Region
        # fields = ['full_name','short_name']

class IndicatorForm(ModelForm):
    class Meta:
        model = Indicator
