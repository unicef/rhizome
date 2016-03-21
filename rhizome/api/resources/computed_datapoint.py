from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DataPointComputed
from rhizome.models import SourceObjectMap, DocumentSourceObjectMap

class ComputedDataPointResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'computed_datapoint'
        queryset =  DataPointComputed.objects.all()

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()

        # for key, value in kwargs.items():
        for key, value in bundle.data.iteritems():
              setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        return self.save(bundle)

    def get_object_list(self, request):

        try:
            document_id = request.GET['document_id']
        except KeyError:
            document_id = None

        queryset = DataPointComputed.objects.filter(
            document_id=document_id
        ).values('indicator_id','location__name','campaign__name', 'value')

        return queryset
