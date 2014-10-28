import pprint as pp

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from source_data.models import *


def map_indicators(indicator_strings,document_id):

    indicator_mapping = {}

    distinct_indicator_strings = list(set(indicator_strings))

    for indicator_string in distinct_indicator_strings:

        try:
            source_indicator, created = SourceIndicator.objects.get_or_create(
                indicator_string = indicator_string,
                document_id = document_id,
            )
        except IntegrityErrror:
            source_indicator = None

        try:
            indicator_id = IndicatorMap.objects.get(source_indicator_id = \
                source_indicator.id).master_indicator_id

            indicator_mapping[indicator_string] = indicator_id
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass

    return indicator_mapping


def map_campaigns(campaign_strings,document_id):

    campaign_mapping = {}

    distinct_campaign_strings = list(set(campaign_strings))

    for campaign in distinct_campaign_strings:

        try:
            source_campaign, created = SourceCampaign.objects.get_or_create(
                campaign_string = campaign,
                document_id = document_id,
            )
        except IntegrityErrror:
            source_campaign = None


        try:
            campaign_id = CampaignMap.objects.get(source_campaign_id = \
                source_campaign.id).master_campaign_id

            campaign_mapping[str(campaign)] = campaign_id
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass


    return campaign_mapping


def map_regions(region_strings,document_id):

    region_mapping = {}

    distinct_region_strings =  list(set(region_strings))

    for region_string in distinct_region_strings:

        try:
            source_region, created = SourceRegion.objects.get_or_create(\
                region_string=region_string,
                document_id = document_id)
        except IntegrityError:
            source_region = None

        try:
            region_id = RegionMap.objects.get(source_region_id = \
                source_region.id).master_region_id

            region_mapping[region_string] = region_id
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass


    return region_mapping
