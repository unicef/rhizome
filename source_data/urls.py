
from django.conf.urls import url
from source_data.views import *

urlpatterns = [
  url(r'^file_upload/$', file_upload, name='file_upload'),
  url(r'^pre_process_file/(?P<pk>[0-9]+)/$', pre_process_file, name='pre_process_file'),
  url(r'^map_indicator/(?P<pk>[0-9]+)/$', IndicatorMapCreateView.as_view(),name='map_indicator'),
  url(r'^map_region/(?P<pk>[0-9]+)/$', RegionMapCreateView.as_view(),name='map_region'),
  url(r'^map_campaign/(?P<pk>[0-9]+)/$', CampaignMapCreateView.as_view(),name='map_campaign'),
  url(r'^refresh_master/$', refresh_master,name='refresh_master'),
  url(r'^source_indicator/(?P<pk>[0-9]+)/$', ShowSourceIndicator.as_view()),
  url(r'^data_entry/$', data_entry, name='data_entry'),
  url(r'^review_sdps_by_document/(?P<document_id>[0-9]+)/$', review_sdps_by_document, name='review_sdps_by_document'),
  url(r'^refresh_master_by_document_id/(?P<document_id>[0-9]+)/$', refresh_master_by_document_id, name='refresh_master_by_document_id'),




]
