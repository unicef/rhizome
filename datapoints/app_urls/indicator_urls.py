from django.conf.urls import url
from datapoints import views
from datapoints.models import * 

urlpatterns = [

        ################
        ## INDICATORS ##
        ################
        
    ## INDEX ##
    url(r'^$', views.IndexView.as_view(
        model=Indicator,
        template_name = 'indicators/index.html',
        context_object_name = 'top_indicators'),
    name='indicator_index'),

    ## DETAIL ##
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=Indicator,
        template_name='indicators/detail.html'),
    name='indicator_detail'),

    ## CREATE ##
    url(r'^create/$', views.CreateView.as_view(
        model=Indicator,
        success_url="/uf04/datapoints/indicators/indicator_relationships/create",
        template_name='indicators/create.html'),
    name='create_indicator'),

    ## UPDATE ##
    url(r'^update/(?P<pk>[0-9]+)/$', views.UpdateView.as_view( # 
        model=Indicator,
        success_url="/uf04/datapoints/indicators",
        template_name='indicators/update.html'),
    name='update_indicator'),

    ## DELETE ##
    url(r'^delete/(?P<pk>[0-9]+)/$', views.DeleteView.as_view( # 
        model=Indicator,
        success_url="/uf04/datapoints/indicators",
        template_name="indicators/confirm_delete.html"),
    name='delete_indicator'),


        #############################
        ## INDICATOR RELATIONSHIPS ##
        #############################

    ## INDEX ##
    url(r'^indicator_relationships$', views.IndexView.as_view(
        model=IndicatorRelationship,
        template_name = 'indicator_relationships/index.html',
        context_object_name = 'top_indicator_relationships'),
    name='indicator_relationship_index'),

    ## DETAIL ##
    url(r'^indicator_relationships/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=IndicatorRelationship,
        template_name='indicator_relationships/detail.html'),
    name='indicator_relationship_detail'),

    ## CREATE ##
    url(r'^indicator_relationships/create/$', views.CreateView.as_view(
        model=IndicatorRelationship,
        success_url="/uf04/datapoints/indicators",
        template_name='indicator_relationships/create.html'),
    name='create_indicator_relationship'),

    ## REL TYPE INDEX ##
    url(r'^indicator_relationship_types$', views.IndexView.as_view(
        model=IndicatorRelationshipType,
        template_name = 'indicator_relationships/type_index.html',
        context_object_name = 'top_indicator_relationship_types'),
    name='indicator_relationship_type_index'),

    ## REL TYPE CREATE ##
    url(r'^indicator_relationship_types/create/$', views.CreateView.as_view(
        model=IndicatorRelationshipType,
        success_url="/uf04/datapoints/indicators",
        template_name='indicator_relationships/type_create.html'),
    name='create_indicator_relationship_type'),

]