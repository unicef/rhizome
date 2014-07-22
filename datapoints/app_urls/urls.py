from django.conf.urls import patterns,url
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

     ## DASHBOARD ##
    url(r'^dashboard/$', views.DashBoardView.as_view(
        template_name = 'dashboard/index.html',
        context_object_name = 'user_dashboard'),
    name='dashboard'),

    ## DETAIL ##
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=DataPoint,
        template_name='datapoints/detail.html'),
    name='datapoint_detail'),

    ## CREATE ##
    url(r'^create/$', views.DataPointCreateView.as_view(),name='create_datapoint'),

    ## META DATA ##
    url(r'^metadata/$', views.IndexView.as_view(
        model=RegionRelationshipType,
        template_name = 'datapoints/metadata.html',
        context_object_name = 'top_metadata'),
    name='metadata_index'),

    ## UPDATE ##
    url(r'^update/(?P<pk>[0-9]+)/$', views.DataPointUpdateView.as_view(
        model=DataPoint,
        success_url="/datapoints",
        template_name='datapoints/update.html'),
    name='update_datapoint'),

    ## DELETE ##
    url(r'^delete/(?P<pk>[0-9]+)/$', views.DataPointDeleteView.as_view(),
      name='delete_datapoint'),

    ## SEARCH ##
    url(r'^search/$', views.search,name='search_datapoint'),

    ## PERMISSIONS NEEDED ##
    url(r'^permissions_needed/$', views.TemplateView.as_view(
        template_name='datapoints/permissions_needed.html'),
        name='permissions_needed'),


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
