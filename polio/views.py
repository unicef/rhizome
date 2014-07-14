from django.http import HttpResponse


def home(request):

    return HttpResponse("Hello Welcome to the Polio Management app!\n<ul><li><a href='/datapoints/'>dataoints  </a></li><li><a href='/regions/'>regions  </a></li></ul>")