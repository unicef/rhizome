from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from decorator_include import decorator_include

from datapoints.api.geo import GeoResource
from datapoints.api.meta_data import *
from datapoints.api.datapoint import DataPointResource, DataPointEntryResource
from datapoints.api.base import api_debug
from datapoints.views import manage_system

from tastypie.api import Api

admin.autodiscover()

## tastypie endpoints - ##
v1_api = Api(api_name='v1')
v1_api.register(DataPointResource())
v1_api.register(DataPointEntryResource())
v1_api.register(GeoResource())
v1_api.register(CampaignResource())
v1_api.register(LocationResource())
v1_api.register(IndicatorResource())
v1_api.register(OfficeResource())
v1_api.register(CampaignTypeResource())
v1_api.register(LocationTypeResource())
v1_api.register(IndicatorTagResource())
v1_api.register(IndicatorToTagResource())
v1_api.register(CustomDashboardResource())
v1_api.register(CustomChartResource())
v1_api.register(DocumentResource())
v1_api.register(GroupResource())
v1_api.register(UserGroupResource())
v1_api.register(LocationResponsibilityResource())
v1_api.register(GroupPermissionResource())
v1_api.register(DocumentReviewResource())
v1_api.register(SourceObjectMapResource())
v1_api.register(UserResource())
v1_api.register(SourceSubmissionResource())
v1_api.register(DocumentDetailResource())
v1_api.register(DocDataPointResource())
v1_api.register(ComputedDataPointResource())
v1_api.register(RefreshMasterResource())
v1_api.register(QueueProcessResource())
v1_api.register(CacheMetaResource())
v1_api.register(DocDetailTypeResource())
v1_api.register(ChartTypeTypeResource())
v1_api.register(DocTransFormResource())
v1_api.register(CalculatedIndicatorComponentResource())
v1_api.register(AggRefreshResource())

urlpatterns = patterns('',

    ## TASTYPIE API ##
    (r'^api/', include(v1_api.urls)),

    ## HOME PAGE
    url(r'^$', login_required(TemplateView.as_view(template_name="homepage.html")), name='homepage'),

    ## BASE DATPOINT FUNCTINOALITY ( see datapoints/urls )
    url(r'^datapoints/', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),

    ## DASHBOARD WITH URL PARAMS ##
    url(r'^datapoints/[-a-zA-Z0-9]+/$', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),
    url(r'^datapoints/[-a-zA-Z]+/[^/]+/[0-9]{4}/[0-9]{2}/$', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),
    url(r'^datapoints/source-data/[-a-zA-Z]+/[0-9]{4}/[0-9]{2}/[-a-zA-Z]+/[0-9]+/', decorator_include(login_required,'datapoints.urls', namespace="datapoints")),


    ## ADMIN, LOG IN AND LOGOUT
    url(r'^admin/', decorator_include(login_required,admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    ## MANAGE SYSTEM ##
    url(r'^manage_system/', manage_system, name='manage_system'),

    ## ABOUT PAGE ##
    url(r'^about$', TemplateView.as_view(template_name="about.html"), name='about'),

    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls import include, patterns, url

if settings.DEBUG:
    import debug_toolbar
    # urlpatterns += patterns('',
    #     url(r'^debug/', include(debug_toolbar.urls)),
    urlpatterns += patterns('',
            url(r'^api_debug/', api_debug),
    )
