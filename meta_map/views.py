from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from datapoints.mixins import PermissionRequiredMixin
from meta_map.models import IndicatorMap, RegionMap, CampaignMap
from meta_map.forms import *


# Create your views here.

class CreateMap(PermissionRequiredMixin, generic.CreateView):

    template_name='map.html'
    success_url=reverse_lazy('datapoints:datapoint_index')
    # permission_required = 'datapoints.add_datapoint'

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.mapped_by = self.request.user
        # obj.source_id = Source.objects.get(source_name='data entry').id
        obj.save()
        return HttpResponseRedirect(self.success_url)


class IndicatorMapCreateView(CreateMap):

    model=IndicatorMap
    form_class = IndicatorMapForm


class RegionMapCreateView(CreateMap):

    model=RegionMap
    form_class = RegionMapForm


class CampaignMapCreateView(CreateMap):

    model=CampaignMap
    form_class = CampaignMapForm
