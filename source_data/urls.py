
from django.conf.urls import url
from source_data.views import file_upload, process_file, map_header

urlpatterns = [
    url(r'^file_upload/$', file_upload, name='file_upload'),
    url(r'^process_file/(?P<document_id>[0-9]+)$', process_file, name='process_file'),
    url(r'^map_header/(?P<document_id>[0-9]+)$', map_header, name='map_header'),
]
