from datapoints.api.base import BaseModelResource

from source_data.models import SourceSubmission

class SubmissionResource(BaseModelResource):
    '''
    **GET Request** Returns all SourceSubmissions unless an optional parameter is specified
        - *Optional Parameters:*
            'document_id': return only the source submissions with the specified document ids
        - *Errors:*
			if an incorrect document id is provided, returns an empty object list
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'

    def get_object_list(self, request):
        print 'hello==\n' * 5
        try:
            qs = SourceSubmission.objects.filter(document_id=request.GET['document_id']).values()
        except KeyError:
            qs = SourceSubmission.objects.filter(id=request.GET['id']).values()

        return qs
