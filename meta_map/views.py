from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from datapoints.mixins import PermissionRequiredMixin
from meta_map.models import IndicatorMap, RegionMap, CampaignMap
from meta_map.forms import IndicatorMapForm

# Create your views here.
class IndicatorMapCreateView(PermissionRequiredMixin, generic.CreateView):

    model=IndicatorMap
    success_url=reverse_lazy('datapoints:datapoint_index')
    template_name='map_indicator.html'
    # permission_required = 'datapoints.add_datapoint'

    form_class = IndicatorMapForm

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.mapped_by = self.request.user
        # obj.source_id = Source.objects.get(source_name='data entry').id
        obj.save()
        return HttpResponseRedirect(self.success_url)
