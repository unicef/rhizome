from pandas import DataFrame, concat, notnull
from django.http import HttpResponse

from tastypie import fields
from tastypie.utils.mime import build_content_type

from rhizome.api.serialize import CustomSerializer
from rhizome.api.resources.base_datapoint import BaseDataPointResource
from rhizome.api.custom_logic import handle_polio_case_table

from rhizome.models import DataPointComputed, Campaign, Location,\
    LocationPermission, LocationTree, IndicatorClassMap, Indicator, DataPoint, \
    CalculatedIndicatorComponent

import math

class CampaignDatapointResource(BaseDataPointResource):
    '''
    - **GET Requests:**
        - *Required Parameters:*
            'indicator__in' A comma-separated list of indicator IDs to fetch. By default, all indicators
            'chart_type'
        - *Optional Parameters:*
            'location__in' A comma-separated list of location IDs
            'campaign_start' format: ``YYYY-MM-DD``  Include only datapoints from campaigns that began on or after the supplied date
            'campaign_end' format: ``YYYY-MM-DD``  Include only datapoints from campaigns that ended on or before the supplied date
            'campaign__in'   A comma-separated list of campaign IDs. Only datapoints attached to one of the listed campaigns will be returned
            'cumulative'
    '''

    class Meta(BaseDataPointResource.Meta):
        '''
        '''

        resource_name = 'campaign_datapoint'
        max_limit = None
        serializer = CustomSerializer()

    def __init__(self, *args, **kwargs):
        '''
        '''
        
        super(CampaignDatapointResource, self).__init__(*args, **kwargs)

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie..
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle)

        response_meta = self.get_datapoint_response_meta(request, objects)
        response_data = {
            'objects': objects,
            'meta': response_meta,
            'error': None,
        }

        return self.create_response(request, response_data)

    def obj_get_list(self, bundle, **kwargs):
        '''
        This is where the action happens in this resource.  AFter passing the
        url paremeters, get the list of locations based on the parameters passed
        in the url as well as the permissions granted to the user responsible
        for the request.
        Using the location_ids from the get_locations_to_return_from_url method
        we query the datapoint abstracted table, then iterate through these
        values cleaning the indicator_json based in the indicator_ids passed
        in the url parameters, and creating a ResultObject for each row in the
        response.
        '''

        request = bundle.request
        results = []

        self.parsed_params = self.parse_url_params(request.GET)
        self.location_ids = self.get_locations_to_return_from_url(request)

        response_fields = ['id', 'indicator_id', 'campaign_id', 'location_id',\
            'value']

        results = list(DataPointComputed.objects.filter(
                campaign__in=self.parsed_params['campaign__in'],
                location__in=self.location_ids,
                indicator__in=self.parsed_params['indicator__in'])\
                .values(*response_fields))

        ## fill in missing data if requested ##
        if self.parsed_params['show_missing_data'] == u'1':
            df = self.add_missing_data(DataFrame(results))
            df = df.where((notnull(df)),None)
            results = df.to_dict('records')

        ## add enumeration for 'class' indicators
        # if 'class' in Indicator.objects\
        #     .filter(id__in = self.parsed_params['indicator__in'])\
        #     .values_list('data_format', flat=True):
        #
        #     self.class_indicator_map = self.build_class_indicator_map()
        #     df = DataFrame(results).apply(self.add_class_indicator_val, axis=1)
        #     results = df.to_dict('records')

        return results
