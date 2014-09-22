# from django.db import models
from django.forms import ModelForm
from meta_map.models import *
from django.contrib.auth.models import User

class IndicatorMapForm(ModelForm):

    class Meta:
        model = IndicatorMap
        fields = ['master_indicator','source_indicator']
