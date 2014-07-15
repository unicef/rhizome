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
        context_object_name = 'top_datapoints'),
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


        #############################
        ## INDICATOR RELATIONSHIPS ##
        #############################

    ## INDEX ##
    url(r'^indicator_relationships$', views.IndexView.as_view(
        model=IndicatorRelationship,
        template_name = 'indicator_relationships/index.html',
        context_object_name = 'top_indicator_relationships'),
    name='indicator_relationship_index'),

    ## DETAIL ##
    url(r'^indicator_relationships/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=IndicatorRelationship,
        template_name='indicator_relationships/detail.html'),
    name='indicator_relationship_detail'),

    ## CREATE ##
    url(r'^indicator_relationships/create/$', views.CreateView.as_view(
        model=IndicatorRelationship,
        success_url="/datapoints/indicators",
        template_name='indicator_relationships/create.html'),
    name='create_indicator_relationship'),

    ## REL TYPE INDEX ##
    url(r'^indicator_relationship_types$', views.IndexView.as_view(
        model=IndicatorRelationshipType,
        template_name = 'indicator_relationships/type_index.html',
        context_object_name = 'top_indicator_relationship_types'),
    name='indicator_relationship_type_index'),

    ## REL TYPE CREATE ##
    url(r'^indicator_relationship_types/create/$', views.CreateView.as_view(
        model=IndicatorRelationshipType,
        success_url="/datapoints/indicators",
        template_name='indicator_relationships/type_create.html'),
    name='create_indicator_relationship_type'),

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


]
