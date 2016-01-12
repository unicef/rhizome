from tastypie.resources import ALL
from tastypie import fields

from datapoints.api.base import BaseModelResource, BaseNonModelResource
from datapoints.models import Campaign, Location, LocationPermission, Office


class HomePageResult(object):
    # campaign: Object
    # charts: Array[4]
    # dashboard: Object
    #     builtin: true
    #     charts: Array[4]
    #     country: "afghanistan"
    #     id: -6
    #     indicators: Array[9]
    #     latest_campaign_id: 299
    #     location: "Badghis"
    #     title: "Homepage Afghanistan"
    # hasMap: true
    # location: Object

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

    def build_dashboard_for_loc(self, loc, campaign_obj):
        #     charts: Array[4]
        #     country: "afghanistan"
        #     id: -6
        #     indicators: Array[9]
        #     latest_campaign_id: 299
        #     location: "Badghis"
        #     title: "Homepage Afghanistan"

        dashboard = {}
        country_obj = Office.objects.get(id = loc.office_id)
        dashboard['country'] = country_obj.name.lower()
        dashboard['title'] = 'Home Page %s' % country_obj.name
        dashboard['latest_campaign_id'] = campaign_obj.id
        # dashboard['latest_campaign_id'] = Campaign.objects\
        #     .filter(office_id = country_obj.id).order_by('-start_date')[0].id
        ## FIXME -- pull these from the database ! ##
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

        top_lvl_location_id = LocationPermission.objects.get(user_id = \
            request.user.id).top_lvl_location.id

        # replace with fancier logic i.e. locations wiht highest msd chd % ##
        # three_locations = Location.objects.filter(parent_location_id=\
        #     top_lvl_location_id)[:3]
        three_locations = Location.objects.filter(id__in=[3093,3100,3085]) # hilmand, kandahar, nangarhar
        three_location_ids = [x.id for x in three_locations]

        # campaign_obj = Campaign.objects\
        #     .filter(top_lvl_location_id=top_lvl_location_id)\
        #     .order_by('-start_date')[0]

        campaign_obj = Campaign.objects.get(id=299)




        qs = []

        for loc in three_locations:
            hp_obj = HomePageResult()
            hp_obj.campaign = campaign_obj.__dict__
            hp_obj.location = loc.__dict__
            hp_obj.dashboard = self.build_dashboard_for_loc(loc,campaign_obj)
            hp_obj.charts = hp_obj.dashboard['charts']

            hp_obj.campaign.pop('_state', None)
            hp_obj.location.pop('_state', None)

            qs.append(hp_obj)

        return qs
