from django.conf.urls import url
from datapoints import views

urlpatterns = [
    ## DATAPOINTS ##
    url(r'^$', views.DataPointIndexView.as_view(), name='datapoint_index'),
    url(r'^create_datapoint/$', views.create_datapoint, name='create_datapoint'),
    url(r'^(?P<pk>[0-9]+)/$', views.DataPointDetailView.as_view(), name='datapoint_detail'),   

    ## REGIONS ##
    url(r'^regions$', views.RegionIndexView.as_view(), name='region_index'),
    url(r'^regions/create_region/$', views.create_region, name='create_region'),
    url(r'^regions/(?P<pk>[0-9]+)/$',views.RegionDetailView.as_view(), name='region_detail'),

    ## INDICATORS ##
    url(r'^indicators$', views.IndicatorIndexView.as_view(), name='indicator_index'),
    url(r'^indicators/create_indicator/$', views.create_indicator, name='create_indicator'),
    url(r'^indicators/(?P<pk>[0-9]+)/$',views.IndicatorDetailView.as_view(), name='indicator_detail'),

]