from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404

from datapoints.models import DataPoint


def index(request):
    latest_datapoints = DataPoint.objects.order_by('-created_at')[:5]
    context = {'latest_datapoints': latest_datapoints}
    return render(request, 'datapoints/index.html',context)


def show(request, datapoint_id):
    datapoint = get_object_or_404(DataPoint, pk=datapoint_id)
    return render(request, 'datapoints/show.html', {'datapoint':datapoint})