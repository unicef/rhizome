from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DataPointComputed, Campaign, Document
from rhizome.api.serialize import CustomSerializer

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
        serializer = CustomSerializer()

    def apply_filters(self, request, applicable_filters):
        """
        This is how we query the datapoint table
        """

        filters = request.GET

        ## handle indicator filter ( it's required so assume the param exists )
        self.indicator_id_list = filters.get('indicator__in', 0).split(',')

        ## handle campeign logic ##
        ## if campaign__in param passed, use those ids, else get from  start/end

        self.campaign_id_list = filters.get('campaign__in', None)

        if not self.campaign_id_list:
            c_start = filters.get('campaign_start', '2000-01-01')
            c_end = filters.get('campaign_start', '2070-01-01')
            self.campaign_id_list = Campaign.objects.filter(
                                start_date__gte=c_start,
                                start_date__lte=c_end
                            ).values_list('id', flat=True)
        else:
            self.campaign_id_list = self.campaign_id_list.split(',')

        ## handle location logic ##
        self.location_id_list = self.get_locations_to_return_from_url(request)


        filters = {
            'location_id__in': self.location_id_list,
            'indicator_id__in': self.indicator_id_list,
            'campaign_id__in': self.campaign_id_list
        }

        return self.get_object_list(request).filter(**filters)

    def get_response_meta(self, request, objects):

        meta = super(BaseModelResource, self)\
            .get_response_meta(request, objects)

        chart_uuid = request.GET.get('chart_uuid', None)
        if chart_uuid:
            meta['chart_uuid'] = chart_uuid

        meta['location_ids'] =  [int(x) for x in self.location_id_list]
        meta['indicator_ids'] = [int(x) for x in self.indicator_id_list]
        meta['campaign_ids'] = [int(x) for x in self.campaign_id_list]

        return meta

    def add_default_post_params(self, bundle):
        '''
        Add document_id of data entry to the bundle
        '''
        data_entry_doc_id = Document.objects.get(doc_title = 'Data Entry').id
        bundle.data['document_id'] = data_entry_doc_id
        return bundle
