from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DataPointComputed, Campaign

class CampaignDataPointResource(BaseModelResource):
    '''
    **GET Request** Returns computed datapoints for a given document
        - *Required Parameters:*
            'document_id'
        - *Errors:*
            Returns 200 code with an empty set of objects if the id is invalid, or an id is not specified
    **POST Request** Create a computed datapoint
        - *Required Parameters:*
            'document_id', 'indicator_id', 'campaign_id', 'location_id', 'value'
        - *Errors:*
            Returns 500 error if information is missing.
        - *To Note:*
            The api does not validate any of these required parameters. It is possible to create datapoints with invalid campaign ids, etc.
    **DELETE Request** Delete Detail: Delete a computed datapoint using the format '/api/v1/computed_datapoint/<datapoint_id>/'
    '''

    class Meta(BaseModelResource.Meta):
        object_class = DataPointComputed
        required_fields_for_post = ['campaign_id','indicator_id','value',\
            'location_id']
        resource_name = 'campaign_datapoint'
        GET_params_required = ['indicator__in']
        GET_fields = ['id', 'indicator_id', 'campaign_id', 'location_id',\
            'value']

    def apply_filters(self, request, applicable_filters):
        """
        This is how we query the datapoint table
        """

        filters = request.GET

        ## handle location logic ##
        location_id_list = self.get_locations_to_return_from_url(request)

        ## handle indicator filter ( it's required so assume the param exists )
        indicator_id_list = filters.get('indicator__in', 0).split(',')

        ## handle campeign logic ##
        c_start = filters.get('campaign_start', '2000-01-01')
        c_end = filters.get('campaign_start', '2070-01-01')
        self.campaign_id_list = Campaign.objects.filter(
                            start_date__gte=c_start,
                            start_date__lte=c_end
                        ).values_list('id', flat=True)

        filters = {
            'location_id__in': location_id_list,
            'indicator_id__in': indicator_id_list,
            'campaign_id__in': self.campaign_id_list
        }

        return self.get_object_list(request).filter(**filters)

    def get_response_meta(self, request, objects):

        meta = super(BaseModelResource, self)\
            .get_response_meta(request, objects)

        try:
            meta['campaign_ids'] = self.campaign_id_list
        except KeyError:
            pass

        try:
            location_ids = request.GET['location_id__in']
            meta['location_ids'] = location_ids
        except KeyError:
            location_ids = None

        try:
            indicator_ids = request.GET['indicator__in']
            meta['indicator_ids'] = indicator_ids
        except KeyError:
            indicator_ids = None

        try:
            chart_uuid = request.GET['chart_uuid']
            meta['chart_uuid'] = chart_uuid
        except KeyError:
            indicator_ids = None

        return meta
