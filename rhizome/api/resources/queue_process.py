from rhizome.api.resources.base_model import BaseModelResource
from source_data.models import SourceSubmission, DocumentDetail


class QueueProcessResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'queue_process'

    def get_object_list(self, request):
        document_id = request.GET['document_id']

        SourceSubmission.objects.filter(document_id=document_id).update(process_status='TO_PROCESS')

        queryset = DocumentDetail.objects \
            .filter(document_id=document_id).values('id','doc_detail_type_id'\
                ,'doc_detail_type__name','document_id', 'doc_detail_value')

        return queryset

