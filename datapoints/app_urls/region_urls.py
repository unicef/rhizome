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

    ## DELETE ##
    url(r'^delete/(?P<pk>[0-9]+)/$', views.RegionDeleteView.as_view(),
        name='delete_region'),

        ##########################
        ## REGION RELATIONSHIPS ##
        ##########################

    ## INDEX ##
    url(r'^region_relationships$', views.RegionRelationshipIndexView.as_view(),
        name='region_relationship_index'),

    ## CREATE ##
    url(r'^region_relationships/create/$',
        views.RegionRelationshipCreateView.as_view(),
        name='create_region_relationship'),

        ###############################
        ## REGION RELATIONSHIP TYPES ##
        ###############################

    ## REL TYPE INDEX ##
    url(r'^region_relationship_types$',
        views.RegionRelagionshipTypeIndexView.as_view(),
        name='region_relationship_type_index'),

    ## REL TYPE CREATE ##
    url(r'^region_relationship_types/create/$',
        views.RegionRelationshipTypeCreateView.as_view(),
        name='create_region_relationship_type'),

]
