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


]
