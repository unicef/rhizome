from rhizome.api.resources.base_model import BaseModelResource

from rhizome.models import SourceSubmission

class SourceSubmissionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'

    def get_object_list(self, request):

        try:
            qs = SourceSubmission.objects.filter(document_id=request.GET['document_id']).values()
        except KeyError:
            qs = SourceSubmission.objects.filter(id=request.GET['id']).values()

        return qs
