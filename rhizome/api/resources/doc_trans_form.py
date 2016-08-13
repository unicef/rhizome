from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models.document_models import Document, SourceSubmission
from rhizome.models.datapoint_models import DataPoint
from rhizome.models.campaign_models import Campaign

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
        ## when you upload a file, step one is getting data into source_submission
         `document.doc_transform()`
        ## Step two is translating form source_submission into datapoints
          `document.refresh_master()`
        ## step three, if the file is of type `campaign`, is aggregation
           for each campaign in the document `campaign.aggregate_and_calculate()`
        '''

        document_object = Document.objects\
            .get(id = request.GET.get('document_id'))

        document_object.transform_upload()
        document_object.refresh_master()

        if document_object.file_type == 'campaign':
            doc_campaign_ids = set(list(DataPoint.objects
                .filter(source_submission__document_id=document_object.id)
                .values_list('campaign_id', flat=True)))

            for c_id in doc_campaign_ids:
                campaign_object = Campaign.objects.get(id = c_id)
                campaign_object.aggregate_and_calculate()


        return Document.objects.filter(id=document_object.id).values()
