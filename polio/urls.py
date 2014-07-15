from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'polio.views.home', name='home'),

    url(r'^datapoints/', include('datapoints.urls', namespace="datapoints")),
    url(r'^datapoints/', include('datapoints.region_urls', namespace="regions")),
    url(r'^datapoints/', include('datapoints.indicator_urls', namespace="indicators")),

    url(r'^admin/', include(admin.site.urls)),
)
