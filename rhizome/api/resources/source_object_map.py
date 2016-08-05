from rhizome.api.resources.base_model import BaseModelResource
from rhizome.simple_models import Indicator, Location, Campaign
from rhizome.simple_models import SourceObjectMap, DocumentSourceObjectMap

class SourceObjectMapResource(BaseModelResource):
    '''
    **GET Request** Returns all Source Object Maps
        - *Optional Parameters:*
            'id': return only the id(s) specified
            'document_id': returns only Source Object Maps associated with the given document id(s)
        - *Errors:*
            If an error occurs, the API returns 200 code and an empty list of Source Object Maps
    **POST Request** Changes the master object for an existing source object map
        - *Required Parameters:*
           'master_object_id' 'mapped_by_id' 'id'
        - *Errors:*
            if any of the required fields are missing or incorrect, the API returns a 500 error code.
    '''

    class Meta(BaseModelResource.Meta):
        '''
        '''
        resource_name = 'source_object_map'
        object_class = SourceObjectMap
        required_fields_for_post = ['id'] #['source_object_code', 'content_type']
        # bring back when REST resource fetch is handled properly in FE
        # GET_params_required = ['document_id'] FE

    def apply_filters(self, request, applicable_filters):
        """
        We use this to handle attional filters for the source object map model.

        This is overridden from the parent BaseModelResource
        """

        filters = request.GET

        ## fix this in the front end to request the resourec in REST style ##
        id_param = request.GET.get('id', None)
        if id_param:
            return self.get_object_list(request).filter(**{'id': id_param})

        ## first filter by the meta data relevant to this document ##
        som_ids_for_document = DocumentSourceObjectMap.objects \
                .filter(document_id=filters['document_id']). \
                values_list('source_object_map_id', flat=True)
        applicable_filters['id__in'] = som_ids_for_document

        ## get the is_mapped filter, if not passed we name this var show_all
        ## because that is the behavior that we execute when there is no param
        is_mapped = filters.get('is_mapped', 'show_all')
        if is_mapped == '0':
            applicable_filters['master_object_id'] = -1
        elif is_mapped == '1':
            applicable_filters['master_object_id__gt'] = 0
        else:
            pass

        return self.get_object_list(request).filter(**applicable_filters)
