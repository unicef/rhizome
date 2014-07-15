from django.conf.urls import url
from datapoints import views
from datapoints.models import * 

urlpatterns = [

    ## INDEX ##
    url(r'^indicators$', views.IndexView.as_view(
        model=Indicator,
        template_name = 'indicators/index.html',
        context_object_name = 'top_indicators'),
    name='indicator_index'),

    ## DETAIL ##
    url(r'^indicators/(?P<pk>[0-9]+)/$', views.DetailView.as_view(
        model=Indicator,
        template_name='indicators/detail.html'),
    name='indicator_detail'),

    ## CREATE ##
    url(r'^indicators/create/$', views.CreateView.as_view(
        model=Indicator,
        success_url="/datapoints/indicator_relationships/create",
        template_name='indicators/create.html'),
    name='create_indicator'),
]