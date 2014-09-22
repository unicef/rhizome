
from django.conf.urls import url
from meta_map.views import IndicatorMapCreateView,RegionMapCreateView, \
    CampaignMapCreateView

from source_data.views import document_review


urlpatterns = [
## CREATE ##
    url(r'^map_indicator/$', IndicatorMapCreateView.as_view(),name='map_indicator'),
    url(r'^map_region/$', RegionMapCreateView.as_view(),name='map_region'),
    url(r'^map_campaign/$', CampaignMapCreateView.as_view(),name='map_campaign'),

    # url(r'^document_review/(?P<pk>[0-9]+)/$', document_review(),name='document_review'),



]
