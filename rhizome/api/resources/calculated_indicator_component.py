from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import CalculatedIndicatorComponent

class CalculatedIndicatorComponentResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        # queryset = CalculatedIndicatorComponent.objects.all().values()
        resource_name = 'indicator_calculation'

    def get_object_list(self, request):

        try:
            indicator_id = request.GET['indicator_id']
        except KeyError:
            indicator_id = -1
        qs = CalculatedIndicatorComponent.objects \
            .filter(indicator_id=indicator_id) \
            .values('id', 'indicator_id', 'indicator_component_id', 'indicator_component__short_name', 'calculation')
        return qs

    def obj_create(self, bundle, **kwargs):
        indicator_id = bundle.data['indicator_id']
        component_id = bundle.data['component_id']
        type_info = bundle.data['typeInfo']

        it = CalculatedIndicatorComponent.objects.create(
            indicator_id=indicator_id,
            indicator_component_id=component_id,
            calculation=type_info,
        )

        bundle.obj = it
        bundle.data['id'] = it.id

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CalculatedIndicatorComponent.objects.filter(id=obj_id).delete()

