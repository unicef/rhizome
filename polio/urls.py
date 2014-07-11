from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'polio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^datapoints/', include('datapoints.urls')),

    url(r'^datapoints/', include('datapoints.urls', namespace="datapoints")),
    url(r'^regions/', include('datapoints.region_urls', namespace="regions")),
    url(r'^admin/', include(admin.site.urls)),
)
