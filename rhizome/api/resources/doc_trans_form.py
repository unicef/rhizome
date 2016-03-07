from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Document
from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform

class DocTransFormResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

    def get_object_list(self, request):
        doc_id = request.GET['document_id']
        # dt = DocTransform(request.user.id, doc_id)
        dt = SimpleDocTransform(request.user.id, doc_id)
        dt.main()

        return Document.objects.filter(id=doc_id).values()
