from django import forms
from datapoints.models import Region, Indicator, Campaign, RegionPermission


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = ['source','source_region']

class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator
        exclude = ['created_at']

class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        exclude = ['created_at']

class RegionPermissionForm(forms.ModelForm):

    class Meta:
        model = RegionPermission
        exclude = ['created_at']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name')
