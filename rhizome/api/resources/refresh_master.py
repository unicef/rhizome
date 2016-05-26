from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DataPoint
from rhizome.models import Document
from rhizome.api.exceptions import DatapointsException
from rhizome.agg_tasks import AggRefresh

from rhizome.etl_tasks.refresh_master import MasterRefresh

class RefreshMasterResource(BaseModelResource):
    '''
    **GET Request** Runs refresh master, and agg refresh for a given document
        - *Required Parameters:* 
            'document_id'
        - *Errors:*
            returns 500 error if no document id is provided          
    '''
    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_master'

    def get_object_list(self, request):
        try:
            doc_id = request.GET['document_id']
        except KeyError:
            raise DatapointsException(message='Document_id is a required API param')
        # dt = DocTransform(request.user.id, doc_id)

        mr = MasterRefresh(request.user.id, doc_id)
        mr.main()

        doc_campaign_ids = set(list(DataPoint.objects\
            .filter(source_submission__document_id = doc_id)\
            .values_list('campaign_id',flat=True)))
        for c_id in doc_campaign_ids:
            AggRefresh(c_id)

        return Document.objects.filter(id=doc_id).values()
