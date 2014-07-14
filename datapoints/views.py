from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from datapoints.models import DataPoint,Region
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

            ###### REGIONS ######

## -> Can I subclass these so i dont repeat myself

class RegionIndexView(generic.ListView):
    template_name = 'regions/index.html'
    context_object_name = 'top_regions'


    def get_queryset(self):
        pp.pprint(Region.objects.order_by('-created_at')[:5])
        return Region.objects.order_by('-created_at')[:5]  


class RegionDetailView(generic.DetailView):
    model = Region
    template_name = 'regions/detail.html'


def create_region(request):
    if request.method == 'GET':
        return render(request, 'regions/create_region.html/', {})
    elif request.method == 'POST':
        user_input = request.POST['content']
        # region = Region.objects.create(**user_input_dict)
        region = Region.objects.create(short_name=user_input,full_name=user_input)
        # # No need to call post.save() at this point -- it's already saved.
        return HttpResponseRedirect('/datapoints/regions')



