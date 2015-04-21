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
from tastypie.api import Api

admin.autodiscover()

v1_api = Api(api_name='v1')
# v1_api.register(RegionResource())
v1_api.register(DataPointResource())
v1_api.register(DataPointEntryResource())
# v1_api.register(IndicatorResource())
v1_api.register(UserResource())
v1_api.register(EtlResource())
v1_api.register(RegionPolygonResource())
# v1_api.register(CampaignResource())


urlpatterns = patterns('',
    ## CUSTOM API ##
    url(r'^api/v1/campaign/$', views.api_campaign, name='campaign'),
    url(r'^api/v1/region/$', views.api_region, name='region'),
    url(r'^api/v1/indicator/$', views.api_indicator, name='indicator'),
    #TODO: add permissions decorator
    url(r'^api/v1/entity/users/metadata/', views.api_user_mock, name='user_mock'),
    url(r'^api/v1/entity/users/', views.api_user, name='user'),
    # http://localhost:8000/api/v1/campaign_from_vw/?region__in=12907

    ## TASTYPIE API ##
    (r'^api/', include(v1_api.urls)),

    ##
    url(r'^$', RedirectView.as_view(url='/datapoints', permanent=False), name='index'),
    ##
    url(r'^datapoints/', decorator_include(login_required,'datapoints.app_urls.urls', namespace="datapoints")),
    url(r'^datapoints/[-a-zA-Z]+/[^/]+/[0-9]{4}/[0-9]{2}/$', decorator_include(login_required,'datapoints.app_urls.urls', namespace="datapoints")),
    url(r'^datapoints/indicators/', decorator_include(login_required,'datapoints.app_urls.indicator_urls', namespace="indicators")),
    url(r'^datapoints/regions/', decorator_include(login_required,'datapoints.app_urls.region_urls', namespace="regions")),
    ##
    url(r'^admin/', decorator_include(login_required,admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    ##
    url(r'^source_data/', decorator_include(login_required,'source_data.urls', namespace="source_data")),
    ##
    (r'^upload/', decorator_include(login_required,'source_data.urls', namespace="upload")),
        ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^debug/', debug),
    )
