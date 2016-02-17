from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from decorator_include import decorator_include
from tastypie.api import Api

from datapoints.api.resources import *
from datapoints.api.decorators import api_debug
from datapoints.views import manage_system, about

admin.autodiscover()

# TASTYPIE Endpoints
#---------------------------------------------------------------------------
v1_api = Api(api_name='v1')
v1_api.register(agg_refresh.AggRefreshResource())
v1_api.register(cache_meta.CacheMetaResource())
v1_api.register(calculated_indicator_component.CalculatedIndicatorComponentResource())
v1_api.register(campaign.CampaignResource())
v1_api.register(campaign_type.CampaignTypeResource())
v1_api.register(chart_type.ChartTypeResource())
v1_api.register(computed_datapoint.ComputedDataPointResource())
v1_api.register(custom_chart.CustomChartResource())
v1_api.register(custom_dashboard.CustomDashboardResource())
v1_api.register(datapoint.DatapointResource())
v1_api.register(datapoint_entry.DatapointEntryResource())
v1_api.register(doc_datapoint.DocDataPointResource())
v1_api.register(doc_detail_type.DocDetailTypeResource())
v1_api.register(doc_trans_form.DocTransFormResource())
v1_api.register(document.DocumentResource())
v1_api.register(document_detail.DocumentDetailResource())
v1_api.register(geo.GeoResource())
v1_api.register(group.GroupResource())
v1_api.register(homepage.HomePageResource())
v1_api.register(indicator.IndicatorResource())
v1_api.register(indicator_tag.IndicatorTagResource())
v1_api.register(indicator_to_tag.IndicatorToTagResource())
v1_api.register(location_permission.LocationPermissionResource())
v1_api.register(location.LocationResource())
v1_api.register(location_type.LocationTypeResource())
v1_api.register(office.OfficeResource())
v1_api.register(queue_process.QueueProcessResource())
v1_api.register(refresh_master.RefreshMasterResource())
v1_api.register(source_object_map.SourceObjectMapResource())
v1_api.register(source_submission.SourceSubmissionResource())
v1_api.register(sync_odk.SyncOdkResource())
v1_api.register(user_group.UserGroupResource())
v1_api.register(user.UserResource())

urlpatterns = patterns(
    '',

    # TASTYPIE API
    (r'^api/', include(v1_api.urls)),

    # HOME PAGE
    url(r'^$', login_required(TemplateView.as_view(template_name='homepage.html')), name='homepage'),

    # BASE DATPOINT FUNCTIONALITY ( see datapoints/urls )
    url(r'^datapoints/', decorator_include(login_required, 'datapoints.urls', namespace='datapoints')),

    # DASHBOARD WITH URL PARAMS
    url(r'^datapoints/dashboards/[-a-zA-Z0-9]+/$',
        decorator_include(login_required, 'datapoints.urls', namespace='datapoints')),
    url(r'^datapoints/dashboards/[-a-zA-Z]+/[^/]+/[0-9]{4}/[0-9]{2}/$',
        decorator_include(login_required, 'datapoints.urls', namespace='datapoints')),
    url(r'^datapoints/source-data/[-a-zA-Z]+/[0-9]{4}/[0-9]{2}/[-a-zA-Z]+/[0-9]+/',
        decorator_include(login_required, 'datapoints.urls', namespace='datapoints')),

    # ADMIN, LOG IN AND LOGOUT
    url(r'^admin/', decorator_include(login_required, admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    # MANAGE SYSTEM
    url(r'^manage_system/', manage_system, name='manage_system'),

    # ABOUT PAGE
    url(r'^about$', about, name='about'),

    # Waffle PATH
    url(r'^', include('waffle.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    # urlpatterns += patterns('',
    #     url(r'^debug/', include(debug_toolbar.urls)),
    urlpatterns += patterns(
        '',
        url(r'^api_debug/', api_debug),
    )

