from django.views.generic import TemplateView
from django.conf.urls import url

from datapoints import views


urlpatterns = [

    ## STATIC DASHBOARDS ( mgmnt, district, NGA campaign monitoring)
    # url(r'^$', views.DashBoardView.as_view(), name='dashboard'),

    ## CHARTS ##
    url(r'^charts/$', views.charts, name='charts'),
    url(r'^charts/create$', views.chart_builder, name='chart_create'),
    url(r'^explore$', views.chart_builder, name='chart_create'),
    url(r'^charts/(?P<chart_id>[0-9]+)/$', views.chart, name='chart'),
    url(r'^charts/(?P<chart_id>[0-9]+)/edit/$', views.chart_edit, name='chart_edit'),
    url(r'^chart_builder/(?P<dashboard_id>[0-9]+)/', views.chart_builder, name='chart_builder'),

    # PRINT DASHBOARDS
    url(r'^dashboards/export_file/?$', views.export_file, name='export_file'),

    ## DASHBOARDS ##
    url(r'^dashboards/$', views.dashboards, name='dashboards'),
    url(r'^dashboards/create$', views.dashboard_builder, name='dashboard_create'),
    url(r'^dashboards/(?P<dashboard_id>[0-9]+)/$', views.dashboard, name='dashboard'),
    url(r'^dashboards/(?P<dashboard_slug>[\w-]+)$', views.builtin_dashboard, name='builtin_dashboard'),
    url(r'^dashboards/(?P<dashboard_slug>[\w-]+/[-a-zA-Z]+/[0-9]+/[0-9]+)$', views.builtin_dashboard, name='builtin_dashboard'),
    url(r'^dashboards/(?P<dashboard_id>[0-9]+)/edit/$', views.dashboard_builder, name='dashboard_edit'),


    ## DATA BROWSERe ##
    url(r'^data_browser/$', views.data_browser, name='data_browser'),

    ## DATA ENTRY ##
    url(r'^entry/$', views.data_entry, name='datapoint_entry'),

    ## DATA SOURCE DATA
    url(r'^source-data/$', views.source_data, name='source_data'),

    ## ADMIN FUNCTINALITY THAT NEEDS TO BE MIGRATED OUT OF DJANGO INTO .js ##
    url(r'^campaign/', views.update_campaign, name='update_campaign'),

    url(r'^users/create/$', views.UserCreateView.as_view(),
        name='create_user'),
    url(r'^users/update/(?P<pk>[0-9]+)/$', views.UserEditView.as_view(),
        name='user_update'),

    ## PERMISSIONS NEEDED ##
    url(r'^permissions_needed/$', TemplateView.as_view(
        template_name='permissions_needed.html'),
        name='permissions_needed'),

]
