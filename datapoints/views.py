from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from datapoints.models import DataPoint,Region
from datapoints.forms import RegionForm

import pprint as pp

class IndexView(generic.ListView):
    template_name = 'datapoints/index.html'
    context_object_name = 'latest_datapoints'

    def get_queryset(self):
        return DataPoint.objects.order_by('-created_at')[:10]  


class DetailView(generic.DetailView):
    model = DataPoint
    template_name = 'datapoints/detail.html'

            ###### REGIONS ######

## -> Can I subclass these so i dont repeat myself

class RegionIndexView(generic.ListView):
    template_name = 'regions/index.html'
    context_object_name = 'top_regions'


    def get_queryset(self):
        return Region.objects.order_by('-created_at')[:10]  


class RegionDetailView(generic.DetailView):
    model = Region
    template_name = 'regions/detail.html'


def create_region(request):
    if request.method == 'GET':
        form = RegionForm()
    else:
        form = RegionForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data
            region = Region.objects.create(**content)

            return HttpResponseRedirect('/datapoints/regions')

    return render(request, 'regions/create_region.html',{'form':form,})



