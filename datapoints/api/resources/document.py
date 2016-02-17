import base64
import time

from tastypie.resources import ALL
from tastypie import fields

from django.core.files.base import ContentFile

from datapoints.api.resources.base_model import BaseModelResource
from source_data.models import Document

class DocumentResource(BaseModelResource):
    docfile = fields.FileField(attribute="csv", null=True, blank=True)

    class Meta(BaseModelResource.Meta):
        queryset = Document.objects.all().order_by('-created_at').values()
        max_limit = 10
        resource_name = 'source_doc'
        filtering = {
            "id": ALL,
        }

    def obj_create(self, bundle, **kwargs):
        '''
        If post, create file and return the JSON of that object.
        If get, just query the source_doc table with request parameters
        '''

        doc_data = bundle.data['docfile']

        try:
            doc_id = bundle.data['id']
        except KeyError:
            doc_id = None

        try:
            doc_title = bundle.data['doc_title'] + '-' + str(int(time.time()))
        except KeyError:
            doc_title = doc_data[:10]

        new_doc = self.post_doc_data(doc_data, bundle.request.user.id, doc_title, doc_id)

        bundle.obj = new_doc
        bundle.data['id'] = new_doc.id

        return bundle

    def post_doc_data(self, post_data, user_id, doc_title, doc_id):

        # when posting from ODK, i dont add the file_meta.. from the webapp
        # i do.  I should change so the post requests are consistent but
        # tryign to get this working for now.

        try:
            file_meta, base64data = post_data.split(',')
        except ValueError:
            base64data = post_data

        file_content = ContentFile(base64.b64decode(base64data))
        file_header = file_content.readline()

        sd, created = Document.objects.update_or_create(
            id=doc_id,
            defaults={'doc_title': doc_title, 'created_by_id': user_id, \
                'file_header': file_header}
        )

        sd.docfile.save(sd.guid, file_content)

        return sd

