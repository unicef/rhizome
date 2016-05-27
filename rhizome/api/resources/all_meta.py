from tastypie import fields
from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models import Campaign, CustomChart, CustomDashboard, Indicator, IndicatorTag, IndicatorToTag, Location, Office, User


class AllMetaResult(object):
    campaigns = list()
    charts = list()
    dashboards = list()
    indicators = list()
    indicator_tags = list()
    indicators_to_tags = list()
    locations = list()
    offices = list()
    is_superuser = bool()


class AllMetaResource(BaseNonModelResource):
    '''
    **GET Request** Returns all camapaigns, charts, dashboards, indicators,indicator_tags, locations and offices in the database.
        - *Required Parameters:*
            none
    '''
    campaigns = fields.ListField(attribute='campaigns')
    charts = fields.ListField(attribute='charts')
    dashboards = fields.ListField(attribute='dashboards')
    indicators = fields.ListField(attribute='indicators')
    indicator_tags = fields.ListField(attribute='indicator_tags')
    indicators_to_tags = fields.ListField(attribute='indicators_to_tags')
    locations = fields.ListField(attribute='locations')
    offices = fields.ListField(attribute='offices')
    is_superuser = fields.BooleanField(attribute='is_superuser')

    class Meta(BaseNonModelResource.Meta):
        object_class = AllMetaResult
        resource_name = 'all_meta'

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def get_object_list(self, request):
        qs = []
        am_result = AllMetaResult()
        am_result.campaigns = \
            [c for c in Campaign.objects.all().values()]
        am_result.charts = \
            [c for c in CustomChart.objects.all().values()]
        am_result.dashboards = \
            [d for d in CustomDashboard.objects.all().values()]
        am_result.indicators = \
            [ind for ind in Indicator.objects.all().values()]
        am_result.indicator_tags = \
            [t for t in IndicatorTag.objects.all().values()]
        am_result.indicators_to_tags = \
            [itt for itt in IndicatorToTag.objects.all().values()]
        am_result.locations = \
            [l for l in Location.objects.all().values()]
        am_result.offices = \
            [o for o in Office.objects.all().values()]
        am_result.is_superuser = User.objects.get(
            id=request.user.id).is_superuser
        qs.append(am_result)

        return qs
