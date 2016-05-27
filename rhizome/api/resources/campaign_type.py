from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import CampaignType


class CampaignTypeResource(BaseModelResource):
    '''
    **GET Request** Returns all campaign types
        - *Optional Parameters:* 
          none
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'campaign_type'

    def get_object_list(self, request):
        queryset = CampaignType.objects.all().values()
        return queryset
