from django import forms
from datapoints.models import Location,   Indicator, Campaign


from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
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
        fields = ('username','first_name','last_name','email')
