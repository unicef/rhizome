from rhizome.api.resources.base_model import BaseModelResource
from rhizome.simple_models import DataPoint, DataPointComputed
from rhizome.models.document_models import Document

class DateDocResultResource(BaseModelResource):
    '''
    **GET Request** Returns all doc_detail_type objects
        - *Required Parameters:*
                    None
    '''
    class Meta(BaseModelResource.Meta):
        object_class = DataPoint
        resource_name = 'date_doc_result'
        GET_fields = ['indicator__id', 'location__name',\
            'indicator__short_name', 'data_date', 'value']
        GET_params_required = ['document_id']

    def apply_filters(self, request, applicable_filters):
        """
        """

        document_id = request.GET.get('document_id', None)
        return self.get_object_list(request)\
            .filter(**{'source_submission__document_id':document_id})
