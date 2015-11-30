from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from datapoints.models import Location, LocationType, Indicator, Campaign,\
    UserAdminLevelPermission


class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        exclude = ['created_at']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['location_type']=forms.ModelChoiceField(queryset=LocationType.objects.all())

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.fields['location_type']=forms.ModelChoiceField(queryset=LocationType.objects.all())
