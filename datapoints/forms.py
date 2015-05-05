from django.forms import ModelForm
from datapoints.models import Region, Indicator, Campaign

class RegionForm(ModelForm):

    class Meta:
        model = Region
        exclude = ['source','source_region']

class IndicatorForm(ModelForm):

    class Meta:
        model = Indicator

class CampaignForm(ModelForm):

    class Meta:
        model = Campaign
