from django import forms
from datapoints.models import Region, Indicator, Campaign, RegionPermission


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = ['source','source_region']

class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator

class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign

class RegionPermissionForm(forms.ModelForm):

    class Meta:
        model = RegionPermission

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserEditForm(UserChangeForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        # fields = ("username", "email", "first_name", "last_name")
