from django.conf.urls import patterns,url
from datapoints import views
from datapoints.models import *
from django.views.generic import TemplateView

urlpatterns = [

        ################
        ## DATAPOINTS ##
        ################

    ## INDEX ##
    url(r'^$', views.DataPointIndexView.as_view(),name='datapoint_index'),

     ## DASHBOARD ##
    url(r'^dashboard/$', views.DashBoardView.as_view(),name='dashboard'),

    ## CREATE ##
    url(r'^create/$', views.DataPointCreateView.as_view(),name='create_datapoint'),

    ## UPDATE ##
    url(r'^update/(?P<pk>[0-9]+)/$', views.DataPointUpdateView.as_view(),
        name='update_datapoint'),

    ## DELETE ##
    url(r'^delete/(?P<pk>[0-9]+)/$', views.DataPointDeleteView.as_view(),
        name='delete_datapoint'),

    ## SEARCH ##
    url(r'^search/$', views.search,name='search_datapoint'),

    ## META DATA ##
    url(r'^metadata/$', TemplateView.as_view(
        template_name = 'datapoints/metadata.html'),
        name='metadata_index'),

    ## PERMISSIONS NEEDED ##
    url(r'^permissions_needed/$', TemplateView.as_view(
        template_name='datapoints/permissions_needed.html'),
        name='permissions_needed'),


        #######################
        ## REPORTING PERIODS ##
        #######################

    ## INDEX ##
    url(r'^reporting_periods$', views.ReportingPeriodIndexView.as_view(),
        name='reporting_period_index'),

    ## CREATE ##
    url(r'^reporting_periods/create/$',
        views.ReportingPeriodCreateView.as_view(),
        name='create_reporting_period'),


]
