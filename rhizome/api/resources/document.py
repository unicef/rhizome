import base64
import time

from tastypie.resources import ALL
from tastypie import fields

from django.core.files.base import ContentFile
from pandas import read_excel

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Document
from django.conf import settings
from rhizome.api.exceptions import RhizomeApiException

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
        object_class = Document
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

        new_doc = self.post_doc_data(bundle)
        bundle.obj = new_doc
        bundle.data['id'] = new_doc.id

        return bundle

    def post_doc_data(self, bundle):

        # get the basic information needed from the request
        # and add the epoch time to the title of the document
        user_id, GET_data = bundle.request.user.id, bundle.data
        post_data, doc_title = GET_data['docfile'], GET_data['doc_title'] \
            + '-' + str(int(time.time()))

        # this handles the fact that test posts are different from
        # application posts. Need to investigate.
        if post_data == 'data:' or len(post_data) == 0:
            raise RhizomeApiException(
                message='file is empty please check the upload and try again')

        # when posting from ODK cronjob, we dont add the file_meta. but we do
        # from the webapp.  Look into changing so the requests are consistent
        try:
            file_meta, base64data = post_data.split(',')
        except ValueError:
            base64data = post_data

        file_header = None
        file_content = None

        if '.csv' in doc_title:
            new_file_path = None
            file_content = ContentFile(base64.b64decode(base64data))
            file_header = file_content.readline()
        elif '.xlsx' in doc_title or '.xls' in doc_title:
            # workaround - need to create the xls file in order to read from it
            new_file_path = settings.MEDIA_ROOT + doc_title
            new_file = open(new_file_path, 'w')
            new_file.write(base64.b64decode(base64data))
            new_file.close()
            the_file = open(new_file_path)
            try:
                file_df = read_excel(the_file)
            except Exception:
                os.remove(new_file_path)
                raise RhizomeApiException(
                    message='There was an error with your file. Please check \\\
                        the upload and try again')
            file_content = ContentFile(file_df.to_csv())
            file_header = file_content.readline()
        else:
            RhizomeApiException(
                message='Please upload either xls, xlsx or csv file formats')

        sd = Document.objects.create(**{
             'doc_title': doc_title,
             'created_by_id': user_id,
             'file_header': file_header
             })
        sd.docfile.save(sd.guid, file_content)

        return sd
