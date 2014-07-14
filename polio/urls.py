from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'polio.views.home', name='home'),

    url(r'^datapoints/', include('datapoints.urls', namespace="datapoints")),
    url(r'^admin/', include(admin.site.urls)),
)
