from rhizome.api.resources.base_model import BaseModelResource
from rhizome.simple_models import DataPoint, DataPointComputed
from rhizome.models.document_models import Document


class CampaignDocResultResource(BaseModelResource):
    '''
    **GET Request** Returns all doc_detail_type objects
        - *Required Parameters:*
                    None
    '''
    class Meta(BaseModelResource.Meta):
        object_class = DataPointComputed
        resource_name = 'campaign_doc_result'
        GET_fields = ['indicator__id', 'location__name',\
            'indicator__short_name', 'campaign__name', 'value']
        GET_params_required = ['document_id']

    def apply_filters(self, request, applicable_filters):
        """
        """

        document_id = request.GET.get('document_id', None)
        return self.get_object_list(request)\
            .filter(**{'document_id':document_id})
