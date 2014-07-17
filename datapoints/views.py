from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from datapoints.models import DataPoint,Region,Indicator
from datapoints.forms import RegionForm,IndicatorForm,DataPointForm


class IndexView(generic.ListView):
    pass # template name and model passed via the URL.

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')[:10]  

class DetailView(generic.DetailView):
    pass # template name and model passed via the URL.

class CreateView(generic.CreateView):
    pass # template name and model passed via the URL.

class UpdateView(generic.UpdateView):
    pass # template name and model passed via the URL.

class DeleteView(generic.DeleteView):
    pass # template name and model passed via the URL.


class DataPointCreateView(CreateView):
    model=DataPoint
    success_url="/datapoints"
    template_name='datapoints/create.html'
    form_class=DataPointForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.success_url)