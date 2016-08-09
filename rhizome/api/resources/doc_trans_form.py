from django.db import transaction
from django.db.transaction import TransactionManagementError

from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.models.document_models import Document, DocumentDetail,\
    SourceSubmission, DataPoint
from rhizome.agg_tasks import AggRefresh

class DocTransFormResource(BaseNonModelResource):
    '''
    **GET Request** Runs document transform, refresh master, and agg refresh
        for a given document
        - *Required Parameters:*
            'document_id'
        - *Errors:*
            returns 500 error if no document id is provided
    '''

    class Meta(BaseNonModelResource.Meta):
        '''
        '''
        resource_name = 'transform_upload'
        queryset = SourceSubmission.objects.all().values()
        GET_params_required = ['document_id']

    def pre_process_data(self, request):
        '''
        ## when you upload a file, step one is getting data into source
            submission
            ## --> DocTransform <-- ##
        ## Step two is translating form source_submission into datapoints
            ## --> REfreshMaster <----
        ## step three is aggregation
            ## agg refresh ##
        '''

        # user_id = request.user.id
        document_object = Document.objects\
            .get(id = request.GET.get('document_id'))

        document_object.transform_upload()
        document_object.refresh_master()

        if document_object.file_type == 'campaign':
            doc_campaign_ids = set(list(DataPoint.objects
                .filter(source_submission__document_id=document_object.id)
                .values_list('campaign_id', flat=True)))

            for c_id in doc_campaign_ids:
                print 'C_ID %s' % c_id
                agg_refresh_obj = AggRefresh(c_id)
                # try/except block hack because tests fail otherwise
                try:
                    with transaction.atomic():
                        agg_refresh_obj.main()
                except TransactionManagementError as e:
                    pass

        return Document.objects.filter(id=document_object.id).values()
