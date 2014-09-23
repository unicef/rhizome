
from django.conf.urls import url
from source_data.views import *

urlpatterns = [
  url(r'^file_upload/$', file_upload, name='file_upload'),
  url(r'^document_review/(?P<pk>[0-9]+)/$', document_review, name='document_review'),

  url(r'^map_indicator/$', IndicatorMapCreateView.as_view(),name='map_indicator'),
  url(r'^map_region/$', RegionMapCreateView.as_view(),name='map_region'),
  url(r'^map_campaign/$', CampaignMapCreateView.as_view(),name='map_campaign'),

  url(r'^to_map/$', ToMap.as_view(),name='to_map'),

]
