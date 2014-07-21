from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db import connection

from datapoints.models import DataPoint,Region,Indicator
from datapoints.forms import RegionForm,IndicatorForm,DataPointForm


class IndexView(generic.ListView):

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

class DataPointUpdateView(generic.UpdateView):
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


class DashBoardView(generic.ListView):
 
    def get_queryset(self):
        cursor = connection.cursor()

        raw_sql = '''select 
                d.value / d2.value as pct
                ,i.name
                ,reg.full_name
            from datapoint d
            inner join region reg
                on d.region_id = reg.id
            inner join indicator i
                on d.indicator_id = i.id
            inner join indicator_relationship r 
                on i.id = r.indicator_0_id
            inner join indicator_relationship_type rt
                on r.indicator_relationship_type_id = rt.id
                and rt.display_name = 'Part to whole'
            inner join datapoint d2
                on 1=1
                and d2.indicator_id = r.indicator_1_id;
            -- and region_id = region_id
            -- and reporting period = reporting period'''
        
        cursor.execute(raw_sql)

        rows = cursor.fetchall()

        for r in rows:
            print r[0]
        return rows

        # return DataPoint.objects.order_by('-created_at')[:1]


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



