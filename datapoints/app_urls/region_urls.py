from django.conf.urls import url
from datapoints import views
from datapoints.models import *

urlpatterns = [

        #############
        ## REGIONS ##
        #############

    ## INDEX ##
    url(r'^$', views.RegionIndexView.as_view(),
        name='region_index'),

    ## CREATE ##
    url(r'^create/$', views.RegionCreateView.as_view(),
        name='create_region'),

    ## UPDATE ##
    url(r'^update/(?P<pk>[0-9]+)/$', views.RegionUpdateView.as_view(),
        name='update_region'),

]
