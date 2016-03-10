from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import DatapointsException
from rhizome.models import Document
from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform


class DocTransFormResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

    def get_object_list(self, request):
        try:
            doc_id = request.GET['document_id']
        except KeyError:
            raise DatapointsException(message='Document_id is a required API param')
        # dt = DocTransform(request.user.id, doc_id)

        try:
            dt = SimpleDocTransform(request.user.id, doc_id)
            dt.main()
        except Exception as err:
            raise DatapointsException(message=err.message)

        return Document.objects.filter(id=doc_id).values()
