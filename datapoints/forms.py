from django import forms
from datapoints.models import Location, Indicator, ResultStructure, LocationPermission


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        exclude = ['longitude','latitude']

class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator
        fields = ['name','short_name']


class ResultStructureForm(forms.ModelForm):

    class Meta:
        model = ResultStructure
        exclude = ['created_at']

class LocationPermissionForm(forms.ModelForm):

    class Meta:
        model = LocationPermission
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
