from tastypie import fields
from rhizome.api.resources.base_non_model import BaseNonModelResource

class ChartTypeResult(object):
    id = int()
    name = unicode()

class ChartTypeResource(BaseNonModelResource):
    '''
    **GET Request** Returns all Chart type names and ids
    '''

    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')

    class Meta(BaseNonModelResource.Meta):
        object_class = ChartTypeResult
        resource_name = 'chart_type'

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def get_object_list(self, request):

        chart_types =["PieChart","LineChart","BarChart","ColumnChart",\
            "ChoroplethMap","ScatterChart","TableChart"]
        qs = []

        for i,(ct) in enumerate(chart_types):

            ct_obj = ChartTypeResult()
            ct_obj.id = i
            ct_obj.name = ct
            qs.append(ct_obj)

        return qs

