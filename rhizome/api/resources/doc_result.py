from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Document, DataPoint, DataPointComputed


class DocResultResource(BaseModelResource):
    '''
    **GET Request** Returns all doc_detail_type objects
        - *Required Parameters:*
                    None
    '''
    class Meta(BaseModelResource.Meta):
        object_class = DataPointComputed
        resource_name = 'doc_result'
        # GET_fields = ['indicator__id', 'location__name',\
            # 'indicator__short_name', 'campaign__name', 'value']
        GET_params_required = ['document_id']

    # def apply_filters(self, request, applicable_filters):
    #     """
    #     """
    #
    #     document_id = request.GET.get('document_id', None)
    #     return self.get_object_list(request)\
    #         .filter(**{'document_id':document_id})

    def obj_get_list(self, bundle, **kwargs):
        """
        If this is a campaign datapoint then we return data from the
        calculated datapoint model, if it is date data, we return it
        from the datapoint model.
        """

        query_fields = ['indicator__id', 'location__name', \
            'indicator__short_name', 'value']

        document_object = Document.objects.get(id = \
            bundle.request.GET.get('document_id'))

        if document_object.file_type == 'campaign':
            query_fields.append('campaign__name')
            return DataPointComputed.objects.filter(
                document_id = document_object.id
            ).values(*query_fields)

        else:
            query_fields.append('data_date')
            return DataPoint.objects.filter(
                source_submission__document_id = document_object.id
            ).values(*query_fields)



        # ## validate the filters ##
        # filters = self.validate_filters(bundle.request)
        #
        # ## Update with the provided kwargs ##
        # filters.update(kwargs)
        #
        # ## clean and prepare the filters and their relavant query terms ##
        # applicable_filters = self.build_filters(filters=filters)
        #
        # ## get the objects and apply the filters ##
        # objects = self.apply_filters(bundle.request, applicable_filters)

        return objects
