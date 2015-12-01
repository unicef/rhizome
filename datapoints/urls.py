from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from decorator_include import decorator_include

from datapoints import views


urlpatterns = [

    ## STATIC DASHBOARDS ( mgmnt, district, NGA campaign monitoring)
    url(r'^$', views.DashBoardView.as_view(),name='dashboard'),

    ## CUSTOM DASHBOARDS ##
    url(r'^dashboards/$', views.dashboard_list,name='dashboard_list'),
    url(r'^dashboards/edit$', views.dashboard_builder,name='dashboard_builder_no_params'),
    url(r'^dashboards/edit/(?P<dashboard_id>[0-9]+)/$', views.dashboard_builder,name='dashboard_builder'),

    ## CHART BUILDER ##
    url(r'^chart_builder/(?P<dashboard_id>[0-9]+)/', views.chart_builder,name='chart_builder'),

    ## DATA BROWSERe ##
    url(r'^data_browser/$', views.data_browser,name='data_browser'),

    ## DATA ENTRY ##
    url(r'^entry/$', views.data_entry,name='datapoint_entry'),

    ## ADMIN FUNCTINALITY THAT NEEDS TO BE MIGRATED OUT OF DJANGO INTO .js ##
    url(r'^campaigns/create/$',views.CampaignCreateView.as_view(),
        name='create_campaign'),
    url(r'^campaigns/update/(?P<pk>[0-9]+)/$', views.CampaignUpdateView.as_view(),
        name='update_campaign'),
    url(r'^users/create/$', views.UserCreateView.as_view(),
        name='create_user'),
    url(r'^users/update/(?P<pk>[0-9]+)/$', views.UserEditView.as_view(),
        name='user_update'),

    ## PERMISSIONS NEEDED ##
    url(r'^permissions_needed/$', TemplateView.as_view(
        template_name='permissions_needed.html'),
        name='permissions_needed'),

]
