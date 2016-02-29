from rhizome.api.resources.base_model import BaseModelResource
from source_data.models import Document
from source_data.etl_tasks.transform_upload import DocTransform

class DocTransFormResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

    def get_object_list(self, request):
        doc_id = request.GET['document_id']
        dt = DocTransform(request.user.id, doc_id)
        dt.main()

        return Document.objects.filter(id=doc_id).values()
