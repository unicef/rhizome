from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from decorator_include import decorator_include
from tastypie.api import Api

from rhizome.api.resources import *
from rhizome.api.decorators import api_debug
from rhizome import views

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


protected_patterns = [

    url(r'^$', RedirectView.as_view(url='dashboards/eoc-post-campaign/'), name='homepage-redirect'),

    url(r'^permissions_needed/$', TemplateView.as_view(template_name='permissions_needed.html'), name='permissions_needed'),
    url(r'^manage_system/', views.manage_system, name='manage_system'),
    url(r'^campaign/', views.update_campaign, name='update_campaign'), ## NEEDS TO BE MIGRATED OUT OF DJANGO INTO .js ##
    url(r'^export_file/?$', views.export_file, name='export_file'),
    url(r'^explore$', views.data_explorer, name='chart_create'),
    url(r'^entry/$', views.data_entry, name='datapoint_entry'),

    url(r'^users/create/$', views.UserCreateView.as_view(), name='create_user'),
    url(r'^users/update/(?P<pk>[0-9]+)/$', views.UserEditView.as_view(), name='user_update'),

    url(r'^source-data/$', views.source_data, name='source_data'),
    url(r'^source-data/[-a-zA-Z]+/[0-9]{4}/[0-9]{2}/[-a-zA-Z]+/[0-9]+/', views.source_data, name='source_data'),

    url(r'^charts/$', views.charts, name='charts'),
    url(r'^charts/create$', views.data_explorer, name='chart_create'),
    url(r'^charts/(?P<chart_id>[0-9]+)/$', views.chart, name='chart'),
    url(r'^charts/(?P<chart_id>[0-9]+)/edit/$', views.chart_edit, name='chart_edit'),

    url(r'^dashboards/eoc-post-campaign/$', views.builtin_dashboard, name='dashboards'),
    url(r'^dashboards/$', views.dashboards, name='dashboards'),

    url(r'^dashboards/(?P<dashboard_id>[0-9]+)/$', views.dashboard, name='dashboard'),
    url(r'^dashboards/(?P<dashboard_slug>[-a-zA-Z]+)/$', views.builtin_dashboard, name='builtin_dashboard'),
    url(r'^dashboards/(?P<dashboard_slug>[-a-zA-Z]+)/[-a-zA-Z]+/$', views.builtin_dashboard, name='dashboards'),
    url(r'^dashboards/(?P<dashboard_slug>[-a-zA-Z]+)/[-a-zA-Z]+/[0-9]+/$', views.builtin_dashboard, name='builtin_dashboard'),
]

urlpatterns = patterns(
    '',

    (r'^api/', include(v1_api.urls)),

    # url(r'^$', login_required(TemplateView.as_view(template_name='homepage.html')), name='homepage'),
    # url(r'^$', login_required(RedirectView.as_view(url='/dashboards/eoc-post-campaign/')), name='homepage'),

    url(r'^about$', views.about, name='about'),
    url(r'^admin/', decorator_include(login_required, admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^', decorator_include(login_required, protected_patterns, namespace='datapoints')),

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
