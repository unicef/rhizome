from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from polio.views import UserCreateView
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    url(r'^$', 'polio.views.home', name='home'),

    # url(r'^uf04/datapoints/', ),
    url(r'^datapoints/', include('datapoints.app_urls.urls', namespace="datapoints")),
    url(r'^datapoints/indicators/', include('datapoints.app_urls.indicator_urls', namespace="indicators")),
    url(r'^datapoints/regions/', include('datapoints.app_urls.region_urls', namespace="regions")),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/create/$', UserCreateView.as_view(), name='create_user'),

    (r'^upload/', include('datapoints.app_urls.upload_urls', namespace="upload")),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT

)
