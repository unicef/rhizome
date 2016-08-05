from tastypie.resources import ALL
from tastypie import fields

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.simple_models import DocDataPoint

class DocDataPointResource(BaseModelResource):
    '''
    - **GET Requests:**
        - *Required Parameters:*
            'document_id' the document id for which doc datapoints should be returned
    - **Errors:**
        - if no document_id is provided, API returns a 500 error
        - if an invalid document_id is provided, API returns an empty list
    '''

    document_id = fields.IntegerField(attribute='document_id')

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_datapoint'
        object_class = DocDataPoint
        GET_params_required = ['document_id']
        filtering = {
            'document_id': ALL
        }
