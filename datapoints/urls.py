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

    ## DASHBOARD LIST and BUILDER ##
    url(r'^dashboards/$', views.dashboard_list,name='dashboard_list'),
    url(r'^dashboards/edit$', views.dashboard_builder,name='dashboard_builder_no_params'),
     url(r'^dashboards/edit/(?P<dashboard_id>[0-9]+)/$', views.dashboard_builder,name='dashboard_builder'),
    ## DASHBOARD VISUALIZATION BUILDER ##
    url(r'^chart_builder/(?P<dashboard_id>[0-9]+)/', views.chart_builder,name='chart_builder'),

    ## Data Table ##
    url(r'^table/$', views.DataPointIndexView.as_view(),name='datapoint_index'),

    ## Data Entry Form ##
    url(r'^entry/$', views.data_entry,name='datapoint_entry'),

    ## PERMISSIONS NEEDED ##
    url(r'^permissions_needed/$', TemplateView.as_view(
        template_name='permissions_needed.html'),
        name='permissions_needed'),

        ###############
        ## CAMPAIGNS ##
        ###############

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

    ## CREATE ##
    url(r'^regions/create/$', views.RegionCreateView.as_view(),
        name='create_region'),

    ## UPDATE ##
    url(r'^regions/update/(?P<pk>[0-9]+)/$', views.RegionUpdateView.as_view(),
        name='update_region'),


        ################
        ## INDICATORS ##
        ################

    ## CREATE ##
    url(r'^indicators/create/$', views.upsert_indicator,name='create_indicator'),

    ## UPDATE ##
    url(r'^indicators/update/(?P<pk>[0-9]+)/$', views.upsert_indicator,
        name='update_indicator'),

        ###############
        #### USER  ####
        ###############

    ## CREATE ##
    url(r'^users/create/$', views.UserCreateView.as_view(),
        name='create_user'),

    ## UPDATE ##
    url(r'^users/update/(?P<pk>[0-9]+)/$', views.UserEditView.as_view(),
        name='user_update'),

        ###############
        #### GROUP  ####
        ###############

    ## CREATE ##
    url(r'^groups/create/$', views.GroupCreateView.as_view(),
        name='create_user'),

    # ## UPDATE ##
    url(r'^groups/update/(?P<pk>[0-9]+)/$', views.GroupEditView.as_view(),
        name='group_update'),


    ########################################
    ## CACHING VALIDATION AND PERMISSIONS ##
    ########################################

    url(r'^refresh_metadata/$', views.refresh_metadata, name='refresh_metadata'),
    url(r'^cache_control/$', views.cache_control, name='cache_control'),
    url(r'^refresh_cache/$', views.refresh_cache, name='refresh_cache'),

    url(r'^qa_failed/(?P<indicator_id>[0-9]+)/(?P<region_id>[0-9]+)/(?P<campaign_id>[0-9]+)$', views.qa_failed, name='qa_failed'),
    url(r'^test_data_coverage/$', views.test_data_coverage, name='test_data_coverage'),

]
