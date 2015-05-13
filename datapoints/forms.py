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

    # def save(self, commit=True):
    #
    #     print 'TRYING TO SAVE'
    #
    #     user = super(UserCreateForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user
    #
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.save()
    #     return super(UserCreateForm, self).form_valid(form)
