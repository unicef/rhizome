from source_data.models import *
from django.core.exceptions import ObjectDoesNotExist

def map_indicators(df,source_id):

    indicator_mapping = {}
    cols = [col.lower() for col in df]

    for col_name in cols:

        source_indicator, created = SourceIndicator.objects.get_or_create(
            source_id = source_id,
            indicator_string = col_name
        )

        try:
            indicator_id = IndicatorMap.objects.get(source_indicator_id = \
                source_indicator.id).master_indicator_id

            indicator_mapping[col_name] = indicator_id
        except ObjectDoesNotExist:
            pass

    return indicator_mapping


def map_campaigns(campaign_strings,source_id):

    campaign_mapping = {}


    for campaign in campaign_strings:

        source_campaign, created = SourceCampaign.objects.get_or_create(
            source_id = source_id,
            campaign_string = campaign
        )
        try:
            campaign_id = CampaignMap.objects.get(source_campaign_id = \
                source_campaign.id).master_campaign_id

            campaign_mapping[str(campaign[0])] = campaign_id
        except ObjectDoesNotExist:
            pass

    return campaign_mapping
