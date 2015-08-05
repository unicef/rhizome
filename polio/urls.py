from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

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

    ## TASTYPIE API ##
    (r'^api/', include(v1_api.urls)),

    ## V2 API ##
    url(r'^api/v2/(?P<content_type>\w+)/$', login_required(views.v2_api), name='v2_api'),
    url(r'^api/v2/(?P<content_type>\w+)/metadata/$', login_required(views.v2_meta_api),
        name='v2_meta_api'),

    ## HOME PAGE
    url(r'^$', login_required(TemplateView.as_view(template_name="index.html")), name='index'),

    ## BASE DATPOINT FUNCTINOALITY ( see datapoints/urls )
    url(r'^datapoints/', login_required('datapoints.urls', namespace="datapoints")),

    ## DASHBOARD WITH URL PARAMS ##
    url(r'^datapoints/[-a-zA-Z]+/$', login_required('datapoints.urls', namespace="datapoints")),
    url(r'^datapoints/[-a-zA-Z]+/[^/]+/[0-9]{4}/[0-9]{2}/$', login_required('datapoints.urls', namespace="datapoints")),

    ## CORE SOURCE DATA FUNCTINOALITY
    url(r'^source_data/', login_required('source_data.urls', namespace="source_data")),

    ## ADMIN, LOG IN AND LOGOUT
    url(r'^admin/', login_required,admin.site.urls),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    ## ADMIN PAGES HITTING ENTITY API
    url(r'^ufadmin/$', login_required(views.UFAdminView.as_view()), name='ufadmin'),
    url(r'^ufadmin/', login_required(views.UFAdminView.as_view()), name='ufadmin'),

    ## NOT SURE WHAT THIS IS ##
    (r'^upload/', login_required('source_data.urls', namespace="upload")),
        ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^debug/', debug),
    )
