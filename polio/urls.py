from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from decorator_include import decorator_include

from datapoints.api.meta_data import *
from datapoints.api.datapoint import DataPointResource, DataPointEntryResource
from datapoints.api.base import debug
from datapoints import views

from source_data.api import EtlResource
from source_data.views import api_document_review, api_map_meta
from tastypie.api import Api

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(DataPointResource())
v1_api.register(DataPointEntryResource())
v1_api.register(UserResource())
v1_api.register(EtlResource())
v1_api.register(RegionPolygonResource())
# v1_api.register(CampaignResource())
# v1_api.register(IndicatorResource())
# v1_api.register(RegionResource())


urlpatterns = patterns('',

    ## CUSTOM V1 API ##
    url(r'^api/v1/campaign/$', views.api_campaign, name='campaign'),
    url(r'^api/v1/region/$', views.api_region, name='region'),
    url(r'^api/v1/indicator/$', views.api_indicator, name='indicator'),
    url(r'^api/v1/source_data/document_review/$', \
        api_document_review, name='api_document_review'),
    url(r'^api/v1/api_map_meta/$', api_map_meta, name='api_map_meta'),

    ## V2 API
    url(r'^api/v2/get/(?P<content_type>\w+)/$', views.meta_api_GET, name='meta_api_GET'),
    url(r'^api/v2/post/(?P<content_type>\w+)/$', views.meta_api_POST, name='meta_api_POST'),

    ## Entity Api ##
    url(r'api/v1/entity/', decorator_include(login_required, 'entity.app_urls.urls', namespace='entity')),

    ## TASTYPIE API ##
    (r'^api/', include(v1_api.urls)),

    ## HOME PAGE
    url(r'^$', RedirectView.as_view(url='/datapoints', permanent=False), name='index'),

    ## BASE DATPOINT FUNCTINOALITY ( see datapoints/urls )
    url(r'^datapoints/', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),

    ## DASHBOARD WITH URL PARAMS ##
    url(r'^datapoints/[-a-zA-Z]+/[^/]+/[0-9]{4}/[0-9]{2}/$', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),

    ## CORE SOURCE DATA FUNCTINOALITY
    url(r'^source_data/', decorator_include(login_required,'source_data.urls', namespace="source_data")),

    ## ADMIN, LOG IN AND LOGOUT
    url(r'^admin/', decorator_include(login_required,admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    ## NOT SURE WHAT THIS IS ##
    (r'^upload/', decorator_include(login_required,'source_data.urls', namespace="upload")),
        ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^debug/', debug),
    )
