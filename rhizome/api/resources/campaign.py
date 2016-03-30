from datetime import datetime
from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import DatapointsException
from rhizome.models import Campaign

class CampaignResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'campaign'

    def get_detail(self, request, **kwargs):
        bundle = self.build_bundle(request=request)
        bundle.data = Campaign.objects.get(id=kwargs['pk']).__dict__
        return self.create_response(request, bundle)

    def get_object_list(self, request):

        if self.top_lvl_location_id == 4721: ## hack to get sherine off my back !
            qs = Campaign.objects.all()
        else:
            qs = Campaign.objects.filter(\
                top_lvl_location_id = self.top_lvl_location_id)

        if 'id__in' in request.GET:
            requested_ids = request.GET['id__in'].split(",")
            return qs.filter(id__in = requested_ids).values().order_by('-start_date')
        else:
            return qs.values().order_by('-start_date')

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        if 'id' in post_data and post_data['id'] !=-1:
            campaign_id = int(post_data['id'])
        else:
            campaign_id = None

        try:
            defaults = {
                'name': str(post_data['name']),
                'top_lvl_location_id': post_data['top_lvl_location_id'],
                'top_lvl_indicator_tag_id': post_data['top_lvl_indicator_tag_id'],
                'office_id': post_data['office_id'],
                'campaign_type_id': post_data['campaign_type_id'],
                'start_date': datetime.strptime(post_data['start_date'], '%Y-%m-%d'),
                'end_date':  datetime.strptime(post_data['end_date'], '%Y-%m-%d'),
                'pct_complete': post_data['pct_complete']
            }
        except Exception as error:
            print 'Please provide "{0}" for the campaign.'.format(error)
            raise DatapointsException('Please provide "{0}" for the campaign.'.format(error))

        try:
            campaign, created = Campaign.objects.update_or_create(
                id=campaign_id,
                defaults=defaults
            )
        except Exception as error:
            raise DatapointsException(error)

        bundle.obj = campaign
        bundle.data['id'] = campaign.id

        return bundle
