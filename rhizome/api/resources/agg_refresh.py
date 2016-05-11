from rhizome.api.resources.base_model import BaseModelResource
from rhizome.agg_tasks import AggRefresh
from rhizome.models import Campaign, Office

class AggRefreshResource(BaseModelResource):
  '''
      **GET Request** Runs AggRefresh on the backend
        - *Optional Parameters:*
            'id': campaign id of the campaign to run agg refresh on.
            If the parameter is not set, the API will run agg refresh on a randomly chosen campaign that needs to be aggregated.
        - *Errors:*
            if an invalid id is provided, the API returns a 500 error
  '''
  class Meta(BaseModelResource.Meta):
        resource_name = 'agg_refresh'

  def get_object_list(self, request):
     '''
     If no campaign is provided, find one datapoitn that needs processing,
     then find the related campaign based on the

     To Do -- Make a method on the Datapoint model called..
     get_campaign_for_datapoint so that this logic can be easily extended.

         This needs cleanup.

         cache_job_id = -1 --> NEEDS PROCESSING
     cache_job_id = -2 --> NEEDS CAMPAIGN ASSOCIATED
     '''

     try:
         campaign_id = request.GET['campaign_id']
         ar = AggRefresh(campaign_id)
         return Campaign.objects.filter(id=campaign_id).values()
     except KeyError:
         ar = AggRefresh()
         return Office.objects.all().values()
