from django.conf.urls import url
from datapoints import views

urlpatterns = [
    url(r'^$', views.RegionIndexView.as_view(), name='region_index'),
    url(r'^(?P<pk>[0-9]+)/$', views.RegionDetailView.as_view(), name='region_detail'),    
]