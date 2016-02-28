from tastypie.resources import ALL
from tastypie import fields

from datapoints.api.resources.base_non_model import BaseNonModelResource
from datapoints.api.resources.base_model import BaseModelResource
from datapoints.models import Campaign, Location, LocationPermission, Office
from django.core.exceptions import ObjectDoesNotExist

class HomePageResult(object):
    id = int()
    campaign = dict()
    charts = list()
    dashboard = dict()
    location = dict()
    campaign = dict()

class HomePageResource(BaseNonModelResource):
    id = fields.IntegerField(attribute='id')
    location = fields.DictField(attribute='location')
    charts = fields.ListField(attribute='charts')
    dashboard = fields.DictField(attribute='dashboard')
    location = fields.DictField(attribute='location')
    campaign = fields.DictField(attribute='campaign')

    class Meta(BaseNonModelResource.Meta):
        object_class = HomePageResult
        resource_name = 'homepage'
        filtering = {
            "id": ALL,
        }

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def build_dashboard_for_loc(self, location_obj, campaign_obj):
        '''
        This is a hack.
        '''
        dashboard = {}
        country_obj = Office.objects.get(id = location_obj.office_id)


        dashboard['country'] = country_obj.name.lower()
        dashboard['title'] = 'Home Page %s' % country_obj.name
        dashboard['latest_campaign_id'] = campaign_obj.id

        dashboard['charts'] = [{
            'title': 'Polio Cases YTD',
            'section': 'impact',
            'indicators': [168],
            'startOf': 'year',
            'timeRange': {
              'years': 2
            }
          }, {
            'title': 'Under-Immunized Children',
            'section': 'impact',
            'indicators': [431, 432, 433],
            'startOf': 'quarter',
            'timeRange': {
              'years': 3
            }
          }, {
            'title': 'Missed Children',
            'section': 'performance',
            'indicators': [166, 164, 167, 165],
            'timeRange': {
              'months': 12
            }
          }, {
            'title': 'Missed Children by Province',
            'section': 'performance',
            'type': 'ChoroplethMap',
            'locations': 'sublocations',
            'timeRange': 0,
            'indicators': [475]
          }
        ]

        return dashboard

    def get_object_list(self, request):
        '''
        Hacking this temporarily.  This is dependent on ranking of locations
        in the cache_meta process.
        '''

        homepage_lookup = {
            # top_lvl_location_id {[campagn_id,sub_loc]...}
            1: [[296, 7],[296, 8],[296, 12]],
            2: [[302, 3093],[302, 3100],[302, 3085]],
            3: [[45, 3108],[45, 3113],[45, 3110]],
            4721: [[296, 1],[302, 2],[45, 3]]
        }

        hp_config = homepage_lookup[self.top_lvl_location_id]
        qs = []

        for campaign_id, location_id in hp_config:

            try:
                hp_obj = self.build_home_page_object(campaign_id,location_id)
            except ObjectDoesNotExist:
                hp_obj = HomePageResult()

            qs.append(hp_obj)

        return qs

    def build_home_page_object(self,campaign_id,location_id):

        campaign_obj = Campaign.objects.get(id = campaign_id)
        location_obj = Location.objects.get(id = location_id)

        hp_obj = HomePageResult()
        hp_obj.campaign = campaign_obj.__dict__
        hp_obj.location = location_obj.__dict__
        hp_obj.dashboard = self.build_dashboard_for_loc(location_obj\
            ,campaign_obj)
        hp_obj.charts = hp_obj.dashboard['charts']

        hp_obj.campaign.pop('_state', None)
        hp_obj.location.pop('_state', None)

        return hp_obj
