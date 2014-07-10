from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from datapoints.models import DataPoint
import pprint as pp


class IndexView(generic.ListView):
    template_name = 'datapoints/index.html'
    context_object_name = 'latest_datapoints'

    def get_queryset(self):
        pp.pprint(DataPoint.objects.order_by('-created_at')[:5])
        return DataPoint.objects.order_by('-created_at')[:5]  


class DetailView(generic.DetailView):
    model = DataPoint
    template_name = 'datapoints/detail.html'