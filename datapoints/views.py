from django.shortcuts import render
from django.http import HttpResponse
from datapoints.models import DataPoint

def index(request):
    latest_datapoints = DataPoint.objects.order_by('-created_at')[:5]
    output = ', '.join([str(d.value) for d in latest_datapoints])
    return HttpResponse(output)


def show(request, datapoint_id):
    return HttpResponse("You're looking at datapoint %s." % datapoint_id)