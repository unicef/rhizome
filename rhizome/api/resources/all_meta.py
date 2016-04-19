from tastypie import fields
from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models import Indicator, IndicatorTag, Location, Campaign, Office, CustomChart, CustomDashboard, User
import json
from rhizome.api.serialize import CustomSerializer

class AllMetaResult(object):
    campaigns = list()
    charts = list()
    dashboards = list()
    indicators = list()
    indicator_tags = list()
    locations = list()
    offices = list()
    is_sueperuser = bool()

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
    locations = fields.ListField(attribute='locations')
    offices = fields.ListField(attribute='offices')
    is_sueperuser = fields.BooleanField(attribute='is_sueperuser')

    class Meta(BaseNonModelResource.Meta):
        object_class = AllMetaResult
        resource_name = 'all_meta'

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)


    def get_object_list(self, request):
        qs = []
        am_result = AllMetaResult()
        am_result.campaigns = Campaign.objects.all().values()
        am_result.charts = CustomChart.objects.all().values()
        am_result.dashboards = CustomDashboard.objects.all().values()
        am_result.indicators = Indicator.objects.all().values()
        am_result.indicator_tags = IndicatorTag.objects.all().values()
        am_result.locations = Location.objects.all().values()
        am_result.offices = Office.objects.all().values()
        am_result.is_superuser = User.objects.get(id = request.user.id).is_superuser
        qs.append(am_result)

        return qs
