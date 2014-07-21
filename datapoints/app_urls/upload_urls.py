from django.conf.urls import url
from datapoints.views import file_upload


urlpatterns = [
  url(r'^file_upload/$', file_upload, name='file_upload'),
]
