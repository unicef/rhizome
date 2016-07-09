from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DataPointComputed, Campaign, Document
from rhizome.api.serialize import CustomSerializer

from pandas import DataFrame, notnull
import itertools

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
            c_end = filters.get('campaign_end', '2070-01-01')

            self.campaign_id_list = Campaign.objects.filter(
                                start_date__gte=c_start,
                                start_date__lte=c_end
                            ).values_list('id', flat=True)
        else:
            self.campaign_id_list = self.campaign_id_list.split(',')

        ## handle location logic ##
        self.location_id_list = self.get_locations_to_return_from_url(request)

        q_filters = {
            'location_id__in': self.location_id_list,
            'indicator_id__in': self.indicator_id_list,
            'campaign_id__in': self.campaign_id_list
        }

        objects_with_data = self.get_object_list(request).filter(**q_filters)
        # return self.get_object_list(request).filter(**filters)
        # FIXME hack to be fixed when we merge:
        # https://github.com/unicef/rhizome/tree/feature/fe-handle-missing


        if filters['chart_type'] == 'ColumnChart':
            objects = self.add_missing_data(objects_with_data)
        else:
            objects = objects_with_data

        return objects

    def add_missing_data(self, objects):
        '''
        In high charts ( our front end visualization module ) when we pass
        data to a stacked / grouped bar chart, everything has to be in order,
        meaning that if we have missing data, we have to pass the chart
        an object that contains an object for each peice of missing data.

        We are currently working on impementing the logic you see below into
        the front end, but in order to get somethign working fo the TAG
        meeting next week, instead of pushign forward on the front end
        implmentatino which is in it's early stages.. I have put this piece of
        code in to the campaign api so that the grouped bar charts
        will render properly.

        For more informatino on this see: https://trello.com/c/euIwyOh4/9
        '''

        ## build a data frame from the object list
        df = DataFrame(list(objects))

        ## create a dataframe with all possible objects based on possble objects
        list_of_lists = [df['location_id'].unique(), \
            df['indicator_id'].unique(), df['campaign_id'].unique()]
        cart_product = list(itertools.product(*list_of_lists))
        columns_list = ['location_id','indicator_id', 'campaign_id']
        cart_prod_df = DataFrame(cart_product, columns = columns_list)

        ## merge the two data frames, which will effectively fill in the missing
        ## data giving obects a Null value if they did not exist in query result
        df = df.merge(cart_prod_df, how='outer', on=columns_list)
        non_null_df = df.where((notnull(df)), None)

        ## create a list of dictionaries ( same structure as the input )
        object_list = [row.to_dict() for ix, row in non_null_df.iterrows()]

        return object_list


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
