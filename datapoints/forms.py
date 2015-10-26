from django import forms
from datapoints.models import Location,   Indicator, Campaign, LocationPermission


from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        exclude = ['longitude','latitude']

class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator
        fields = ['name','short_name']


class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        exclude = ['created_at']

class LocationPermissionForm(forms.ModelForm):

    class Meta:
        model = LocationPermission
        exclude = ['created_at']

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name')

