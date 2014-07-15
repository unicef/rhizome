from django.conf.urls import url
from datapoints import views
from datapoints.models import * 

urlpatterns = [

        #############
        ## REGIONS ##
        #############

    ## INDEX ##
    url(r'^$', views.IndexView.as_view(
        model = Region,
        template_name = 'regions/index.html',
        context_object_name = 'top_regions'),
    name='region_index'),

    ## DETAIL ##
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=Region,
        template_name='regions/detail.html'),
    name='region_detail'),

    ## CREATE ##
    url(r'^create/$', views.CreateView.as_view(
        model=Region,
        success_url="/datapoints/region_relationships/create",
        template_name='regions/create.html'),
    name='create_region'),

        ##########################
        ## REGION RELATIONSHIPS ##
        ##########################

    ## INDEX ##
    url(r'^region_relationships$', views.IndexView.as_view(
        model=RegionRelationship,
        template_name = 'region_relationships/index.html',
        context_object_name = 'top_region_relationships'),
    name='region_relationship_index'),

    ## DETAIL ##
    url(r'^region_relationships/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=RegionRelationship,
        template_name='region_relationships/detail.html'),
    name='region_relationship_detail'),

    ## CREATE ##
    url(r'^region_relationships/create/$', views.CreateView.as_view(
        model=RegionRelationship,
        success_url="/datapoints/regions",
        template_name='region_relationships/create.html'),
    name='create_region_relationship'),

        ###############################
        ## REGION RELATIONSHIP TYPES ##
        ###############################


    ## REL TYPE INDEX ##
    url(r'^region_relationship_types$', views.IndexView.as_view(
        model=RegionRelationshipType,
        template_name = 'region_relationships/type_index.html',
        context_object_name = 'top_region_relationship_types'),
    name='region_relationship_type_index'),

    ## REL TYPE CREATE ##
    url(r'^region_relationship_types/create/$', views.CreateView.as_view(
        model=RegionRelationshipType,
        success_url="/datapoints/regions",
        template_name='region_relationships/type_create.html'),
    name='create_region_relationship_type'),

]

