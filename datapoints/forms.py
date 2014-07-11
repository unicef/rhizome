from django.db import models
from django.forms import ModelForm
from datapoints.models import Region


class RegionForm(ModelForm):
    class Meta:
        model = Region
        fields = ['full_name']

# python manage.py shell
# from datapoints.forms import RegionForm
# f = RegionForm({'full_name': 'nigeria'})
# f.save()