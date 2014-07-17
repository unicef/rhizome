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
    form_class = DataPointForm

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.success_url)

class UpdateView(generic.UpdateView):
    model=DataPoint
    success_url="/datapoints"
    template_name='datapoints/update.html'
    form_class = DataPointForm

    def form_valid(self, form):
    # this sets the changed_by field to the user who made the update
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.success_url)

    ## NOTE ON AUDITING DELETES ##
    ## Right now i am not tracking who makes the delete
    ## the audit table will store the delete as the last person who 
    ## changed that record.  This will be difficult to code up because
    ## of the way that the audit trail works.

    ## the audit table creates one record for whatever is in the 
    ## database at the time the request is complete (or made in the 
    ## case of a delete)
    
    ## the reason this does not work is because, when the delete is made
    ## the changed by field will be whoever touched that row last NOT
    ## who made the delete.   Not horrible, but still wrong



