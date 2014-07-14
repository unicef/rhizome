from django.conf.urls import url
from datapoints import views
from datapoints.models import DataPoint, Region, Indicator

urlpatterns = [
    ## DATAPOINTS ##
    url(r'^$', views.DataPointIndexView.as_view(), name='datapoint_index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DataPointDetailView.as_view(), name='datapoint_detail'),
    url(r'^create_datapoint/$', views.CreateView.as_view
        (model=DataPoint
        ,success_url="/datapoints"
        ,template_name='datapoints/create_datapoint.html')
        , name='create_datapoint'),
    


    ## REGIONS ##
    url(r'^regions$', views.RegionIndexView.as_view(), name='region_index'),
    url(r'^regions/(?P<pk>[0-9]+)/$',views.RegionDetailView.as_view(), name='region_detail'),
    url(r'^regions/create_region/$', views.CreateView.as_view
        (model=Region
        ,success_url="/datapoints/regions"
        ,template_name='regions/create_region.html')
        , name='create_region'),


    ## INDICATORS ##
    url(r'^indicators$', views.IndicatorIndexView.as_view(), name='indicator_index'),
    url(r'^indicators/(?P<pk>[0-9]+)/$',views.IndicatorDetailView.as_view(), name='indicator_detail'),
    url(r'^indicators/create_indicator/$', views.CreateView.as_view
        (model=Indicator
        ,success_url="/datapoints/indicators"
        ,template_name='indicators/create_indicator.html')
        , name='create_indicator'),




]