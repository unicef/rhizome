from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.models.campaign_models import Campaign, DataPointComputed


class AggRefreshResource(BaseModelResource):
    '''
        **GET Request** Runs agg_refresh on the backend
          - *Optional Parameters:*
              'id': campaign id of the campaign to run agg refresh on.
              If the parameter is not set, the API will run agg refresh on a
              randomly chosen campaign that needs to be aggregated.
          - *Errors:*
              if an invalid id is provided, the API returns a 500 error
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'agg_refresh'
        object_class = DataPointComputed
        required_GET_params = 'campaign_id'

    def pre_process_data(self, request):
        '''
        '''

        campaign_id = request.GET.get('campaign_id')
        campaign_object = Campaign.objects.get(id = campaign_id)
        campaign_object.aggregate_and_calculate()
