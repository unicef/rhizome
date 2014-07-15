from django.conf.urls import url
from datapoints import views
from datapoints.models import * 

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
    url(r'^create/$', views.CreateView.as_view(
        model=DataPoint,
        success_url="/datapoints",
        template_name='datapoints/create.html'),
    name='create_datapoint'),

    ## META DATA ##
    url(r'^metadata/$', views.IndexView.as_view(
        model=RegionRelationshipType,
        template_name = 'datapoints/metadata.html',
        context_object_name = 'top_metadata'),
    name='metadata_index'),

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
    url(r'^regions/create/$', views.CreateView.as_view(
        model=Region,
        success_url="/datapoints/region_relationships/create",
        template_name='regions/create.html'),
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
    url(r'^indicators/create/$', views.CreateView.as_view(
        model=Indicator,
        success_url="/datapoints/indicators",
        template_name='indicators/create.html'),
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
    url(r'^reporting_periods/create/$', views.CreateView.as_view(
        model=ReportingPeriod,
        success_url="/datapoints/reporting_periods",
        template_name='reporting_periods/create.html'),
    name='create_reporting_period'),

        ##########################
        ## REGION RELATIONSHIPS ##
        ##########################

    ## INDEX ##
    url(r'^region_relationships$', views.IndexView.as_view(
        model=RegionRelationship,
        template_name = 'region_relationships/index.html',
        context_object_name = 'top_region_relationships'),
    name='region_relationship_index'),

    ## DETAIL ##
    url(r'^region_relationships/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=RegionRelationship,
        template_name='region_relationships/detail.html'),
    name='region_relationship_detail'),

    ## CREATE ##
    url(r'^region_relationships/create/$', views.CreateView.as_view(
        model=RegionRelationship,
        success_url="/datapoints/regions",
        template_name='region_relationships/create.html'),
    name='create_region_relationship'),

    ## REL TYPE INDEX ##
    url(r'^region_relationship_types$', views.IndexView.as_view(
        model=RegionRelationshipType,
        template_name = 'region_relationships/type_index.html',
        context_object_name = 'top_region_relationship_types'),
    name='region_relationship_type_index'),

    ## REL TYPE CREATE ##
    url(r'^region_relationship_types/create/$', views.CreateView.as_view(
        model=RegionRelationshipType,
        success_url="/datapoints/regions",
        template_name='region_relationships/type_create.html'),
    name='create_region_relationship_type'),


## TO DO ## 
## -> Change URL from 
   ## region_relationships/create_region_relationship/
   #### to ####
   ## region_relationships/create/
   


]
