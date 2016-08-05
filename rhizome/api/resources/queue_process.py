from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.simple_models import SourceSubmission, DocumentDetail, Document


class QueueProcessResource(BaseNonModelResource):
    '''
    **GET Request:** Sets SourceSubmission objects for a given document id to "to process"
            - *Required Parameters:*
                    'document_id'
            - *Errors:*
                    returns a 500 error if a required parameter is not supplied
    '''
    class Meta(BaseNonModelResource.Meta):
        '''
        '''
        resource_name = 'queue_process'
        queryset = Document.objects.all().values()
        default_limit = 1
        GET_params_required = ['document_id']

    def pre_process_data(self, request):
        '''
        update a document with the "to_process" process status.

        Don't need to catch the keyerror here on docuemnt_id because it is
        already handled with the GET_params_required attribute on Meta
        '''

        SourceSubmission.objects\
            .filter(document_id=request.GET['document_id'])\
            .update(process_status='TO_PROCESS')
