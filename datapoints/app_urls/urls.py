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
    url(r'^cache_control/$', views.cache_control, name='cache_control'),
    url(r'^agg_datapoint/$', views.agg_datapoint, name='agg_datapoint'),
    url(r'^calc_datapoint/$', views.calc_datapoint, name='calc_datapoint'),
    url(r'^pivot_datapoint/$', views.pivot_datapoint, name='pivot_datapoint'),
    url(r'^populate_dummy_ngo_dash/$', views.populate_dummy_ngo_dash, name='populate_dummy_ngo_dash'),
    url(r'^gdoc_qa/$', views.gdoc_qa, name='gdoc_qa'),
]
