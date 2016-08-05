from datetime import datetime
from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.models.campaign_models import Campaign


class CampaignResource(BaseModelResource):
    '''
    **GET Request** Returns campaigns from the database
        - *Optional Parameters:*
            'id': a comma delimited list of campaign ids.
            If the parameter is not set, the API will return all campaigns
        - *Errors:*
            if an invalid id is provided, the API returns a 200 code with
            an empty list of campaigns.

    **GET Request: Request Detail** Another way to query for campaigns using the format: /api/v1/campaign/<campaign_id>/
        - *Errors:*
            if an id is invalid, the API returns a 500 error code.

    **POST Reguest:** Create a camapaign
        -*Required Parameters:*
            'name','top_lvl_location_id',
            #'top_lvl_indicator_tag_id', 'office_id','campaign_type_id',
            #'start_date','end_date','pct_complete'
        -*Errors:*
            If any of the fields are missing, the system returns a 500 error.

    '''
    class Meta(BaseModelResource.Meta):
        resource_name = 'campaign'
        object_class = Campaign
        required_fields_for_post = ['office_id', 'start_date', 'end_date']
