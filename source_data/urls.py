
from django.conf.urls import url
from source_data.views import file_upload


urlpatterns = [
  url(r'^file_upload/$', file_upload, name='file_upload'),
]
