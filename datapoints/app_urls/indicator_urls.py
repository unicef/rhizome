from django.conf.urls import url
from datapoints import views
from datapoints.models import *

urlpatterns = [

        ################
        ## INDICATORS ##
        ################

    ## INDEX ##
    url(r'^$', views.IndicatorIndexView.as_view(),
        name='indicator_index'),

    ## CREATE ##
    url(r'^create/$', views.IndicatorCreateView.as_view(),
        name='create_indicator'),

    ## UPDATE ##
    url(r'^update/(?P<pk>[0-9]+)/$', views.IndicatorUpdateView.as_view(),
        name='update_indicator'),

    ## DELETE ##
    url(r'^delete/(?P<pk>[0-9]+)/$', views.IndicatorDeleteView.as_view(),
        name='delete_indicator'),


    ### CALCULATED ###

    ## INDEX ##
    url(r'^calculated_indicators/$', views.CalculatedIndicatorIndexView.as_view(),
        name='calculated_indicator_index'),

    ## CREATE ##
    url(r'^create_calculated_indicator/$', views.CalculatedIndicatorCreateView.as_view(),
        name='create_calculated_indicator'),

]
