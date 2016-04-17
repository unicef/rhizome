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

        queryset = DataPointComputed.objects.filter(
            document_id=document_id
        ).values('indicator_id','location__name','campaign__name','indicator__short_name' ,'value')

        return queryset

    def delete_detail(self, request, **kwargs):

        DataPointComputed.objects.get(id = kwargs['pk']).delete()
