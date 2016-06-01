import base64
import time

from tastypie.resources import ALL
from tastypie import fields

from django.core.files.base import ContentFile
from pandas import read_excel

from rhizome.api.resources.base_model import BaseModelResource
from source_data.models import Document
from django.conf import settings
from rhizome.api.exceptions import DatapointsException

import os

class DocumentResource(BaseModelResource):
    '''
    **POST Request** uploads a document to the rhizome server.
        - *Required Parameters:*
            'docfile' the base64 encoded file: csv, xls, xlsx file format
            'doc_title' the title of the document
        - *Optional Parameters:*
            'doc_id' an id for the document
        - *Errors:*
            returns 500 error of the document is empty
            returns 500 error if a required parameter is not supplied
    '''

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

        #TODO: better exception handling. This is kind of lame but handles the fact that test posts are different from
        #application posts. Need to investigate.
        if post_data == 'data:' or len(post_data) == 0:
            raise DatapointsException(message='file is empty please check the upload and try again')
        try:
            file_meta, base64data = post_data.split(',')
        except ValueError:
            base64data = post_data
        file_header = None
        file_content = None
        if '.csv' in doc_title:
            file_content = ContentFile(base64.b64decode(base64data))
            file_header = file_content.readline()
        elif '.xlsx' in doc_title or '.xls' in doc_title:
            # workaround-- need to create the excel file in order to read from it
            new_file_path = settings.MEDIA_ROOT+doc_title
            new_file = open(new_file_path, 'wr')
            new_file.write(base64.b64decode(base64data))
            new_file.close()
            the_file = open(new_file_path)
            try:
                file_df=read_excel(the_file)
            except Exception as err:
                os.remove(new_file_path)
                raise DatapointsException(message='There was an error with your file. Please check the upload and try again')
            file_content = ContentFile(file_df.to_csv())
            file_header = file_content.readline()
            # delete the excel file
            os.remove(new_file_path)
        sd, created = Document.objects.update_or_create(
            id=doc_id,
            defaults={'doc_title': doc_title, 'created_by_id': user_id, \
                'file_header': file_header}
        )
        sd.docfile.save(sd.guid, file_content)
        return sd
