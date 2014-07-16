from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'polio.views.home', name='home'),

    url(r'^uf04/datapoints/', include('datapoints.app_urls.urls', namespace="datapoints")),
    url(r'^uf04/datapoints/indicators/', include('datapoints.app_urls.indicator_urls', namespace="indicators")),
    url(r'^uf04/datapoints/regions/', include('datapoints.app_urls.region_urls', namespace="regions")),

    url(r'^uf04/admin/', include(admin.site.urls)),
)
