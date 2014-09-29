import pprint as pp

from django.core.exceptions import ObjectDoesNotExist

from source_data.models import *


def map_indicators(indicator_strings,source_id):

    indicator_mapping = {}

    for indicator_string in indicator_strings:

        source_indicator, created = SourceIndicator.objects.get_or_create(
            source_id = source_id,
            indicator_string = indicator_string
        )

        try:
            indicator_id = IndicatorMap.objects.get(source_indicator_id = \
                source_indicator.id).master_indicator_id

            indicator_mapping[indicator_string] = indicator_id
        except ObjectDoesNotExist:
            indicator_mapping[indicator_string] = None

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

            campaign_mapping[str(campaign)] = campaign_id
        except ObjectDoesNotExist:
            campaign_mapping[str(campaign)] = None

    return campaign_mapping


def map_regions(region_strings, source_id):

    region_mapping = {}

    for region_string in region_strings:

        source_region, created = SourceRegion.objects.get_or_create(\
            region_string=region_string,source_id=source_id)

        try:
            region_id = RegionMap.objects.get(source_region_id = \
                source_region.id).master_region_id

            region_mapping[region_string] = region_id
        except ObjectDoesNotExist:
            region_mapping[region_string] = None


    return region_mapping
