from django.conf.urls import url
from datapoints import views
from datapoints.models import DataPoint, Region, Indicator, ReportingPeriod

urlpatterns = [

        ################
        ## DATAPOINTS ##
        ################

    ## INDEX ##
    url(r'^$', views.IndexView.as_view(
        model=DataPoint,
        template_name = 'datapoints/index.html',
        context_object_name = 'latest_datapoints'),
    name='datapoint_index'),

    ## DETAIL ##
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=DataPoint,
        template_name='datapoints/detail.html'),
    name='datapoint_detail'),

    ## CREATE ##
    url(r'^create_datapoint/$', views.CreateView.as_view(
        model=DataPoint,
        success_url="/datapoints",
        template_name='datapoints/create_datapoint.html'),
    name='create_datapoint'),
    
        #############
        ## REGIONS ##
        #############

    ## INDEX ##
    url(r'^regions$', views.IndexView.as_view(
        model = Region,
        template_name = 'regions/index.html',
        context_object_name = 'top_regions'),
    name='region_index'),

    ## DETAIL ##
    url(r'^regions/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=Region,
        template_name='regions/detail.html'),
    name='region_detail'),

    ## CREATE ##
    url(r'^regions/create_region/$', views.CreateView.as_view(
        model=Region,
        success_url="/datapoints/regions",
        template_name='regions/create_region.html'),
    name='create_region'),


        ################
        ## INDICATORS ##
        ################

    ## INDEX ##
    url(r'^indicators$', views.IndexView.as_view(
        model=Indicator,
        template_name = 'indicators/index.html',
        context_object_name = 'top_indicators'),
    name='indicator_index'),

    ## DETAIL ##
    url(r'^indicators/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=Indicator,
        template_name='indicators/detail.html'),
    name='indicator_detail'),

    ## CREATE ##
    url(r'^indicators/create_indicator/$', views.CreateView.as_view(
        model=Indicator,
        success_url="/datapoints/indicators",
        template_name='indicators/create_indicator.html'),
    name='create_indicator'),


        #######################
        ## REPORTING PERIODS ##
        #######################

    ## INDEX ##
    url(r'^reporting_periods$', views.IndexView.as_view(
        model=ReportingPeriod,
        template_name = 'reporting_periods/index.html',
        context_object_name = 'top_reporting_periods'),
    name='reporting_period_index'),

    ## DETAIL ##
    url(r'^reporting_periods/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=ReportingPeriod,
        template_name='reporting_periods/detail.html'),
    name='reporting_period_detail'),

    ## CREATE ##
    url(r'^reporting_periods/create_reporting_period/$', views.CreateView.as_view(
        model=ReportingPeriod,
        success_url="/datapoints/reporting_periods",
        template_name='reporting_periods/create_reporting_period.html'),
    name='create_reporting_period'),


]
