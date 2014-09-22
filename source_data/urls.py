
from django.conf.urls import url
from source_data.views import file_upload, document_review


urlpatterns = [
  url(r'^file_upload/$', file_upload, name='file_upload'),
  url(r'^document_review/(?P<pk>[0-9]+)/$', document_review, name='document_review'),

]
