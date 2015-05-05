from django.conf.urls import url
from datapoints import views
from datapoints.models import *
from django.views.generic import TemplateView

urlpatterns = [

        ################
        ## DATAPOINTS ##
        ################

    ## DASHBOARD ##
    url(r'^$', views.DashBoardView.as_view(),name='dashboard'),

    ## Data Table ##
    url(r'^table/$', views.DataPointIndexView.as_view(),name='datapoint_index'),

    ## Data Entry Form ##
    url(r'^entry/$', views.DataEntryView.as_view(),name='datapoint_entry'),


    ## PERMISSIONS NEEDED ##
    url(r'^permissions_needed/$', TemplateView.as_view(
        template_name='datapoints/permissions_needed.html'),
        name='permissions_needed'),

        ###############
        ## CAMPAIGNS ##
        ###############

    ## INDEX ##
    url(r'^campaigns/$', views.CampaignIndexView.as_view(),
        name='campaign_index'),

    ## CREATE ##
    url(r'^campaigns/create/$',
        views.CampaignCreateView.as_view(),
        name='create_campaign'),

    ## UPDATE ##
    url(r'^campaigns/update/(?P<pk>[0-9]+)/$', views.CampaignUpdateView.as_view(),
        name='update_campaign'),


        #############
        ## REGIONS ##
        #############

    ## INDEX ##
    url(r'^regions/$', views.RegionIndexView.as_view(),
        name='region_index'),

    ## CREATE ##
    url(r'^regions/create/$', views.RegionCreateView.as_view(),
        name='create_region'),

    ## UPDATE ##
    url(r'^regions/update/(?P<pk>[0-9]+)/$', views.RegionUpdateView.as_view(),
        name='update_region'),


        ################
        ## INDICATORS ##
        ################

    ## INDEX ##
    url(r'^indicators/$', views.IndicatorIndexView.as_view(),
        name='indicator_index'),

    ## CREATE ##
    url(r'^indicators/create/$', views.IndicatorCreateView.as_view(),
        name='create_indicator'),

    ## UPDATE ##
    url(r'^indicators/update/(?P<pk>[0-9]+)/$', views.IndicatorUpdateView.as_view(),
        name='update_indicator'),


        #############
        ## CACHING ##
        #############

    url(r'^transform_indicators/$', views.transform_indicators, name='transform_indicators'),
    url(r'^cache_control/$', views.cache_control, name='cache_control'),
    url(r'^refresh_cache/$', views.refresh_cache, name='refresh_cache'),

        #####################
        ## DATA VALIDATION ##
        #####################

    url(r'^qa_failed/(?P<indicator_id>[0-9]+)/(?P<region_id>[0-9]+)/(?P<campaign_id>[0-9]+)$', views.qa_failed, name='qa_failed'),
    url(r'^test_data_coverage/$', views.test_data_coverage, name='test_data_coverage'),
    url(r'^bad_data/$', views.bad_data, name='bad_data'),
]
