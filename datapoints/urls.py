from django.conf.urls import url
from datapoints import views

urlpatterns = [
    ## DATAPOINTS ##
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),   

    ## REGIONS ##
    url(r'^regions$', views.RegionIndexView.as_view(), name='region_index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.RegionDetailView.as_view(), name='region_detail'),
    # url(r'^regions/create_region/$', views.create_region, name='create_region'),  
]