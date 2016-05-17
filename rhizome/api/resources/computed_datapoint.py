from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DataPointComputed
from rhizome.models import SourceObjectMap, DocumentSourceObjectMap, Document

class ComputedDataPointResource(BaseModelResource):
    '''
    **GET Request** Returns computed datapoints for a given document
        - *Required Parameters:*
            'document_id'
        - *Errors:*
            Returns 200 code with an empty set of objects if the id is invalid, or an id is not specified
    **POST Request** Create a computed datapoint
        - *Required Parameters:*
            'document_id', 'indicator_id', 'campaign_id', 'location_id', 'value'
        - *Errors:*
            Returns 500 error if information is missing.
        - *To Note:*
            The api does not validate any of these required parameters. It is possible to create datapoints with invalid campaign ids, etc.
    **DELETE Request: Delete Detail** Delete a computed datapoint using the format '/api/v1/computed_datapoint/<datapoint_id>/'
        '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'computed_datapoint'
        queryset =  DataPointComputed.objects.all()

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """

        bundle.data['document_id'] = Document.objects.get(doc_title = 'Data Entry').id
        dwc_obj = DataPointComputed.objects.create(**bundle.data)
        bundle.data['id'] = dwc_obj.id
        bundle.obj = dwc_obj

        return bundle

    def get_object_list(self, request):

        try:
            document_id = request.GET['document_id']
        except KeyError:
            document_id = None

        indicator_id_list = DocumentSourceObjectMap.objects.filter(
            document_id = document_id,
            source_object_map__content_type = 'indicator',
            source_object_map__master_object_id__gt = 0
        ).values_list('source_object_map__master_object_id', flat=True)

        queryset = DataPointComputed.objects.filter(
            document_id=document_id, indicator_id__in = indicator_id_list
        ).values('indicator_id','location__name','campaign__name','indicator__short_name' ,'value')

        return queryset

    def delete_detail(self, request, **kwargs):

        DataPointComputed.objects.get(id = kwargs['pk']).delete()
