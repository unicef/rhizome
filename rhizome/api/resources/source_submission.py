from rhizome.api.resources.base_model import BaseModelResource

from rhizome.models import SourceSubmission


class SourceSubmissionResource(BaseModelResource):
    '''
    **GET Request** Returns all SourceSubmissions unless an optional parameter is specified
        - *Optional Parameters:*
            'document_id': return only the source submissions with the specified document ids
        - *Errors:*
                        if an incorrect document id is provided, returns an empty object list
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'
        object_class = SourceSubmission
        GET_params_required = ['document_id']

    def apply_filters(self, request, applicable_filters):
        """
        An ORM-specific implementation of ``apply_filters``.
        The default simply applies the ``applicable_filters`` as ``**kwargs``,
        but should make it possible to do more advanced things.
        """

        doc_filter = {'document_id': request.GET.get('document_id')}
        return self.get_object_list(request).filter(**doc_filter)
