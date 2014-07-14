from django.http import HttpResponse,HttpResponseRedirect


def home(request):
    return HttpResponseRedirect('/datapoints')
