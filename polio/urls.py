from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from polio.views import UserCreateView
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
from datapoints.api.simple import *
from datapoints.api.aggregate import AggregateResource
from source_data.api import EtlResource
from tastypie.api import Api

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(RegionResource())
v1_api.register(DataPointResource())
v1_api.register(IndicatorResource())
v1_api.register(CampaignResource())
v1_api.register(UserResource())
v1_api.register(OfficeResource())
v1_api.register(AggregateResource())
v1_api.register(EtlResource())


urlpatterns = patterns('',
    ##
    (r'^api/', include(v1_api.urls)),
    ##
    url(r'^$', 'polio.views.home', name='home'),
    ##
    url(r'^datapoints/', include('datapoints.app_urls.urls', namespace="datapoints")),
    url(r'^datapoints/indicators/', include('datapoints.app_urls.indicator_urls', namespace="indicators")),
    url(r'^datapoints/regions/', include('datapoints.app_urls.region_urls', namespace="regions")),
    ##
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/create/$', UserCreateView.as_view(), name='create_user'),

    ##
    url(r'^source_data/', include('source_data.urls', namespace="source_data")),

    ##
    (r'^upload/', include('source_data.urls', namespace="upload")),
        ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT

)
