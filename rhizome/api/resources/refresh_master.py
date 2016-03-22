from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DocDataPoint, DataPoint, Document
from rhizome.api.exceptions import DatapointsException
from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform
from rhizome.agg_tasks import AggRefresh

from rhizome.models import DocumentDetail, DocDetailType, SourceSubmission
from rhizome.etl_tasks.refresh_master import MasterRefresh

class RefreshMasterResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_master'

    def get_object_list(self, request):
        document_id = request.GET['document_id']

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
            ar = AggRefresh(c_id)
            ar.main()

        return Document.objects.filter(id=doc_id).values()
