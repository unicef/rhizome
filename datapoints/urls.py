from django.conf.urls import url

from datapoints import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]