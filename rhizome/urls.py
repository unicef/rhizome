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
v1_api.register(
    calculated_indicator_component.CalculatedIndicatorComponentResource())
v1_api.register(campaign.CampaignResource())
v1_api.register(campaign_type.CampaignTypeResource())
v1_api.register(computed_datapoint.ComputedDataPointResource())
v1_api.register(custom_chart.CustomChartResource())
v1_api.register(custom_dashboard.CustomDashboardResource())
v1_api.register(campaign_datapoint.CampaignDatapointResource())
v1_api.register(date_datapoint.DateDatapointResource())
v1_api.register(doc_datapoint.DocDataPointResource())
v1_api.register(doc_detail_type.DocDetailTypeResource())
v1_api.register(doc_trans_form.DocTransFormResource())
v1_api.register(document.DocumentResource())
v1_api.register(document_detail.DocumentDetailResource())
v1_api.register(geo.GeoResource())
v1_api.register(group.GroupResource())
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
v1_api.register(source_object_to_map.SourceObjectToMapResource())
v1_api.register(source_submission.SourceSubmissionResource())
v1_api.register(sync_odk.SyncOdkResource())
v1_api.register(user_group.UserGroupResource())
v1_api.register(user.UserResource())
v1_api.register(all_meta.AllMetaResource())


protected_patterns = [

    url(r'^$', RedirectView.as_view(url='dashboards/'), name='homepage-redirect'),

    url(r'^permissions_needed$', TemplateView.as_view(
        template_name='permissions_needed.html'), name='permissions_needed'),
    url(r'^manage_system', views.manage_system, name='manage_system'),
    url(r'^campaign', views.update_campaign, name='update_campaign'),
    url(r'^export_file?$', views.export_file, name='export_file'),
    url(r'^explore$', views.chart_create, name='chart_create'),
    url(r'^entry$', views.data_entry, name='datapoint_entry'),

    url(r'^users/create/$', views.UserCreateView.as_view(), name='create_user'),
    url(r'^users/update/(?P<pk>[0-9]+)$', views.UserEditView.as_view(), name='user_update'),

    url(r'^source-data/', views.source_data, name='source_data'),

    url(r'^charts$', views.charts, name='charts'),
    url(r'^charts/create$', views.chart_create, name='chart_create'),
    url(r'^charts/(?P<chart_id>[0-9]+)', views.chart, name='chart'),

    url(r'^dashboards/$', views.dashboards, name='dashboards'),
    url(r'^dashboards/create$', views.dashboard_create, name='dashboard_create'),
    url(r'^dashboards/(?P<dashboard_id>[0-9]+)', views.dashboard, name='dashboard'),

    ## react app -- some day this will be the only ( non api ) url ##
    url(r'^react_app', views.react_app, name='react_app'),

]

urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),

    url(r'^about$', views.about, name='about'),
    url(r'^admin/', decorator_include(login_required, admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^', decorator_include(login_required, protected_patterns)),

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
