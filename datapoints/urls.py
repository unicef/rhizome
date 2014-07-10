from django.conf.urls import url

from datapoints import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<datapoint_id>[0-9]+)/$', views.show, name='show'),
]