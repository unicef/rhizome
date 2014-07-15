from django.conf.urls import url
from datapoints import views
from datapoints.models import * 

urlpatterns = [
        #############
        ## REGIONS ##
        #############

    ## INDEX ##
    url(r'^regions$', views.IndexView.as_view(
        model = Region,
        template_name = 'regions/index.html',
        context_object_name = 'top_regions'),
    name='region_index'),

    ## DETAIL ##
    url(r'^regions/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=Region,
        template_name='regions/detail.html'),
    name='region_detail'),

    ## CREATE ##
    url(r'^regions/create/$', views.CreateView.as_view(
        model=Region,
        success_url="/datapoints/region_relationships/create",
        template_name='regions/create.html'),
    name='create_region'),
]