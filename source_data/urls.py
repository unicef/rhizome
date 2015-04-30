
from django.conf.urls import url
from source_data.views import *

urlpatterns = [
    url(r'^file_upload/$', file_upload, name='file_upload'),
    url(r'^map_header/(?P<document_id>[0-9]+)/',map_header\
        , name='map_header'),

    url(r'^refresh_master/$', refresh_master,name='refresh_master'),

    url(r'^mark_doc_as_processed/(?P<document_id>[0-9]+)/$'\
        , mark_doc_as_processed, name='mark_doc_as_processed'),

    url(r'^document_index/$', DocumentIndex.as_view(),name='document_index'),

    url(r'^etl_job_index/$', EtlJobIndex.as_view(),name='etl_job_index'),

    url(r'^pre_process_file/(?P<document_id>[0-9]+)/',\
        pre_process_file, name='pre_process_file'),

    url(r'^document_review/(?P<document_id>[0-9]+)/$', document_review,\
        name='document_review'),

    url(r'^sync_source_datapoints/(?P<document_id>[0-9]+)/\
        (?P<master_id>[0-9]+)/$',sync_source_datapoints,\
        name='sync_source_datapoints'),

    url(r'^refresh_master_no_indicator/(?P<document_id>[0-9]+)/',refresh_master_no_indicator,\
        name='refresh_master_no_indicator'),



]
