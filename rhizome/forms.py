from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from rhizome.simple_models import LocationType, Campaign


class CampaignForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['pct_complete'].widget = forms.HiddenInput()

    class Meta:
        model = Campaign
        exclude = ['created_at']


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email', 'is_superuser')
