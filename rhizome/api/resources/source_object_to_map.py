from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Indicator, Location, Campaign
from rhizome.models import SourceObjectMap, DocumentSourceObjectMap


class SourceObjectToMapResource(BaseModelResource):
    '''
    '''

    class Meta(BaseModelResource.Meta):
        '''
        '''

        resource_name = 'source_object_to_map'
        object_class = SourceObjectMap
        required_GET_params = ['document_id']

    def apply_filters(self, request, applicable_filters):
        """
        We use this to handle attional filters for the source object map model.

        This is overridden from the parent BaseModelResource
        """

        som_ids_for_document = DocumentSourceObjectMap.objects \
                .filter(document_id=request.GET['document_id']). \
                values_list('source_object_map_id', flat=True)

        applicable_filters['id__in'] = som_ids_for_document
        applicable_filters['master_object_id'] = -1


        return self.get_object_list(request).filter(**applicable_filters)
