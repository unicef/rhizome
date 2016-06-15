from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.agg_tasks import AggRefresh
from rhizome.models import DataPointComputed


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

    def pre_process_resource_data(self, request):
        '''
        '''

        try:
            campaign_id = request.GET['campaign_id']
        except KeyError:
            campaign_id = None

        AggRefresh(campaign_id)
