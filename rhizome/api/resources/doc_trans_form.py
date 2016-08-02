from django.db import transaction
from django.db.transaction import TransactionManagementError

from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.models import DataPoint
from rhizome.models import Document, SourceSubmission
from rhizome.etl_tasks.transform_upload import CampaignDocTransform, DateDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
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
        # GET_params_required = ['document_id', 'file_type']

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

        user_id = request.user.id

        ran_campaign_doc_transform = False # if so, we need to run agg_refresh
        document_id = request.GET.get('document_id', None)
        file_type = request.GET.get('file_type', 'campaign')

        if file_type == 'campaign':
            transform_obj = CampaignDocTransform(user_id, document_id)
        elif file_type == 'date':
            transform_obj = DateDocTransform(user_id, document_id)
        else:
            raise RhizomeApiException(message='file_type %s not supported' %\
                file_type)

        try:
            transform_obj.main()
            refresh_obj = MasterRefresh(request.user.id, document_id)
            refresh_obj.main()
        except Exception as err:
            raise RhizomeApiException(message=err.message)

        if file_type == 'campaign':
            refresh_master_for_campaigns()

        return Document.objects.filter(id=document_id).values()

    def refresh_master_for_campaigns(self):
        '''
        '''
        doc_campaign_ids = set(list(DataPoint.objects
            .filter(source_submission__document_id=document_id)
            .values_list('campaign_id', flat=True)))

        for c_id in doc_campaign_ids:
            
            agg_refresh_obj = AggRefresh(c_id)
            # try/except block hack because tests fail otherwise
            try:
                with transaction.atomic():
                    agg_refresh_obj.main()
            except TransactionManagementError as e:
                pass
