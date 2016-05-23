from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DocDataPoint

class DocDataPointResource(BaseModelResource):
    '''
    - **GET Requests:**
        - *Required Parameters:*
            'document_id' the document id for which doc datapoints should be returned
    - **Errors:**
        - if no document_id is provided, API returns a 500 error
        - if an invalid document_id is provided, API returns an empty list
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_datapoint'

    def get_object_list(self, request):

        queryset = DocDataPoint.objects.filter(
            document_id=request.GET['document_id'],
            # campaign_id=campaign_id,
            # location_id__in=all_location_ids,
        )[:50].values('location__name', 'indicator__short_name', 'campaign__name', 'value')

        return queryset

