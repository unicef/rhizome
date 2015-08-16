
from django.conf.urls import url
from source_data.views import *

urlpatterns = [
    url(r'^file_upload/$', file_upload, name='file_upload'),

    url(r'^refresh_master/(?P<document_id>[0-9]+)$', refresh_master,name='refresh_master'),

    url(r'^document_index/$', DocumentIndex.as_view(),name='document_index'),

    url(r'^pre_process_file/(?P<document_id>[0-9]+)/',\
        pre_process_file, name='pre_process_file'),

    url(r'^field_mapping/(?P<document_id>[0-9]+)/$', field_mapping,\
        name='field_mapping'),

    url(r'^odk_review/',odk_review, name='odk_review'),



]
