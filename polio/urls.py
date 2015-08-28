from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from decorator_include import decorator_include

from datapoints.api.meta_data import *
from datapoints.api.datapoint import DataPointResource, DataPointEntryResource
from datapoints.api.base import debug
from datapoints import views

from source_data.api import EtlResource
from tastypie.api import Api

admin.autodiscover()

## tastypie endpoints - ##
v1_api = Api(api_name='v1')
v1_api.register(DataPointResource())
v1_api.register(DataPointEntryResource())
v1_api.register(EtlResource())
v1_api.register(RegionPolygonResource())

urlpatterns = patterns('',

    ## V2 API ##
    url(r'^api/v2/(?P<content_type>\w+)/$', login_required(views.v2_api), name='v2_api'),
    url(r'^api/v2/(?P<content_type>\w+)/metadata/$', login_required(views.v2_meta_api),
        name='v2_meta_api'),

    ## TASTYPIE API ##
    (r'^api/', include(v1_api.urls)),

    ## HOME PAGE
    url(r'^$', login_required(TemplateView.as_view(template_name="index.html")), name='index'),

    ## BASE DATPOINT FUNCTINOALITY ( see datapoints/urls )
    url(r'^datapoints/', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),

    ## DASHBOARD WITH URL PARAMS ##
    url(r'^datapoints/[-a-zA-Z]+/$', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),
    url(r'^datapoints/[-a-zA-Z]+/[^/]+/[0-9]{4}/[0-9]{2}/$', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),
    url(r'^datapoints/source-data/[-a-zA-Z]+/[0-9]{4}/[0-9]{2}/[-a-zA-Z]+/[0-9]+/', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),


    ## CORE SOURCE DATA FUNCTINOALITY
    url(r'^source_data/', decorator_include(login_required,'source_data.urls', namespace="source_data")),

    ## ADMIN, LOG IN AND LOGOUT
    url(r'^admin/', decorator_include(login_required,admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    ## UFADMIN ##
    url(r'^ufadmin/', login_required(TemplateView.as_view(template_name='ufadmin.html')), name='ufadmin'),

    ## DOCUMENT_REVIEW ##
    url(r'^doc_review/', TemplateView.as_view(template_name="doc_review.html"), name='doc_review'),

    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^debug/', debug),
    )
