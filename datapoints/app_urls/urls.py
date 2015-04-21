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

        ###############
        ## CAMPAIGNS ##
        ###############

    ## INDEX ##
    url(r'^campaigns$', views.CampaignIndexView.as_view(),
        name='campaign_index'),

    ## CREATE ##
    url(r'^campaign/create/$',
        views.CampaignCreateView.as_view(),
        name='create_campaign'),

    ## UPDATE ##
    url(r'^campaign/update/(?P<pk>[0-9]+)/$', views.CampaignUpdateView.as_view(),
        name='update_campaign'),

        #############
        ## CACHING ##
        #############

    url(r'^transform_indicators/$', views.transform_indicators, name='transform_indicators'),
    url(r'^cache_control/$', views.cache_control, name='cache_control'),
    url(r'^refresh_cache/$', views.refresh_cache, name='refresh_cache'),

        #####################
        ## DATA VALIDATION ##
        #####################

    url(r'^populate_dummy_ngo_dash/$', views.populate_dummy_ngo_dash, name='populate_dummy_ngo_dash'),
    url(r'^qa_failed/(?P<indicator_id>[0-9]+)/(?P<region_id>[0-9]+)/(?P<campaign_id>[0-9]+)$', views.qa_failed, name='qa_failed'),
    url(r'^load_gdoc_data/$', views.load_gdoc_data, name='load_gdoc_data'),
    url(r'^test_data_coverage/$', views.test_data_coverage, name='test_data_coverage'),
    url(r'^bad_data/$', views.bad_data, name='bad_data'),
]
