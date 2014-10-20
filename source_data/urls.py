
from django.conf.urls import url
from source_data.views import *

urlpatterns = [
  url(r'^basic_document_form/$', basic_document_form, name='basic_document_form'),
  url(r'^pre_process_file/$', pre_process_file, name='pre_process_file'),


  url(r'^pre_process_file/(?P<pk>[0-9]+)/$', pre_process_file, name='pre_process_file'),

  url(r'^map_indicator/(?P<pk>[0-9]+)/$', IndicatorMapCreateView.as_view(),name='map_indicator'),
  url(r'^map_region/(?P<pk>[0-9]+)/$', RegionMapCreateView.as_view(),name='map_region'),
  url(r'^map_campaign/(?P<pk>[0-9]+)/$', CampaignMapCreateView.as_view(),name='map_campaign'),

  url(r'^to_map/$', ToMap.as_view(),name='to_map'),
  url(r'^refresh_master/$', refresh_master,name='refresh_master'),



  url(r'^source_indicator/(?P<pk>[0-9]+)/$', ShowSourceIndicator.as_view()),



]
