from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models.document_models import Document, DataPoint
from rhizome.api.exceptions import RhizomeApiException
from rhizome.agg_tasks import AggRefresh


class RefreshMasterResource(BaseNonModelResource):
    '''
    **GET Request** Runs refresh master, and agg refresh for a given document
        - *Required Parameters:*
            'document_id'
        - *Errors:*
            returns 500 error if no document id is provided
    '''
    class Meta(BaseNonModelResource.Meta):
        resource_name = 'refresh_master'
        GET_params_required = ['document_id']
        queryset = Document.objects.all().values()
        default_limit = 1

    def pre_process_data(self, request):
        '''
        Run the refresh master task for the document_id passed.

        Also, for any effected campaigns, run the agg_refresh on those in order
        to calculated aggregated and calcualted values.
        '''

        doc_id = request.GET.get('document_id', None)
        document_object = Document.objecst.get(id = doc_id)
        document_object.refresh_master()

        if Document.objects.get(id = doc_id).file_type == 'campaign':
            doc_campaign_ids = set(list(DataPoint.objects
                            .filter(source_submission__document_id=doc_id)
                            .values_list('campaign_id', flat=True)))
            for c_id in doc_campaign_ids:
                AggRefresh(c_id)

        return Document.objects.filter(id=doc_id).values()
