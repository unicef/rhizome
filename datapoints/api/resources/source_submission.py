from datapoints.api.resources.base_model import BaseModelResource

from source_data.models import SourceSubmission

class SourceSubmissionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'

    def get_object_list(self, request):

        try:
            # see: https://trello.com/c/IGNzN87U/296-3-collapse-source-submission-adn-submission-detail
            qs = SourceSubmission.objects.filter(document_id=request.GET['document_id'])[:50].values()
        except KeyError:
            qs = SourceSubmission.objects.filter(id=request.GET['id']).values()

        return qs

