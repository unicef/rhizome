from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from datapoints.models import DataPoint

def index(request):
    latest_datapoints = DataPoint.objects.order_by('-created_at')[:5]
    template = loader.get_template('datapoints/index.html')
    context = RequestContext(request, {
            'latest_datapoints': latest_datapoints,
        })

    return HttpResponse(template.render(context))


def show(request, datapoint_id):
    return HttpResponse("You're looking at datapoint %s." % datapoint_id)