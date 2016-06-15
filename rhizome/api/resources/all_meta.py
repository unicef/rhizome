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

    def get_object_list(self, request):
        qs = []
        am_result = AllMetaResult()
        am_result.campaigns = \
            list(Campaign.objects.all().values())
        am_result.charts = \
            list(CustomChart.objects.all().values())
        am_result.dashboards = \
            list(CustomDashboard.objects.all().values())
        am_result.indicators = \
            list(Indicator.objects.all().values())
        am_result.indicator_tags = \
            list(IndicatorTag.objects.all().values())
        am_result.indicators_to_tags =\
            list(IndicatorToTag.objects.all().values())

        am_result.locations = list(Location.objects.all().values())
        am_result.offices = \
            [o for o in Office.objects.all().values()]
        am_result.is_superuser = User.objects.get(
            id=request.user.id).is_superuser
        qs.append(am_result)

        return [x.__dict__ for x in qs]
