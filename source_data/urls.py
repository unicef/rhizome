
from django.conf.urls import url
from source_data.views import *

urlpatterns = [
    url(r'^file_upload/$', file_upload, name='file_upload'),
    url(r'^refresh_master/(?P<document_id>[0-9]+)$', refresh_master,name='refresh_master'),
    url(r'^odk_review/',odk_review, name='odk_review'),]
