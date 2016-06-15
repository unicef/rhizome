from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.agg_tasks import AggRefresh
from rhizome.models import DataPointComputed, Campaign



class AggRefreshResource(BaseNonModelResource):
    '''
        **GET Request** Runs AggRefresh on the backend
          - *Optional Parameters:*
              'id': campaign id of the campaign to run agg refresh on.
              If the parameter is not set, the API will run agg refresh on a
              randomly chosen campaign that needs to be aggregated.
          - *Errors:*
              if an invalid id is provided, the API returns a 500 error
    '''
    class Meta(BaseNonModelResource.Meta):
        resource_name = 'agg_refresh'
        queryset = DataPointComputed.objects.all().values()

    def pre_process_data(self, request):
        '''
        Get the campaign_id from the request, if it exists, make sure that
        the campaign_id exists in the database then pass that to the
        AggRefresh class.
        '''

        campaign_id = request.GET.get('campaign_id', None)

        if campaign_id:
            try:
                campaign_object = Campaign.objects.get(id = campaign_id)
            except Campaign.DoesNotExist as err:
                raise RhizomeApiException(err)

        AggRefresh(campaign_id)
