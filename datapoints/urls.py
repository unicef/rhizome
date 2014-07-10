from django.conf.urls import url

from datapoints import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<datapoint_id>[0-9]+)/$', views.show, name='show'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    
]