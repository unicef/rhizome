import pprint as pp
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from source_data.models import *

def pivot_and_insert_src_datapoints(df,document_id,column_mappings):

    header = [col for col in df]
    source_datapoints = []

    print 'HEADER: '
    print header

    for row_number,(row) in enumerate(df.values):
        print row_number

        region_string = row[header.index(column_mappings['region_col'])]
        campaign_string = row[header.index(column_mappings['campaign_col'])]
        source_id = Source.objects.get(source_name='data entry').id
        to_process_status = ProcessStatus.objects.get(status_text='TO_PROCESS').id

        for cell_no,(cell) in enumerate(row):

            indicator_string = header[row_number]

            sdp = SourceDataPoint.objects.get_or_create(
                source_guid = 'doc_id: ' + str(document_id) + \
                    ' row_no: ' + str(row_number) + ' cell_no: ' + str(cell_no),
                defaults = {
                    'indicator_string': indicator_string,
                    'region_string':region_string,
                    'campaign_string':campaign_string,
                    'cell_value':cell,
                    'row_number':row_number,
                    'source_id':source_id,
                    'document_id':document_id,
                    'status_id':to_process_status
                })

            source_datapoints.append(sdp)
    return source_datapoints

def map_indicators(indicator_strings,document_id):
    ## THESE METHODS NEED TO BE ABSTRACTED SO THAT YOU PASS DOCUMENT_ID  ##
    ## STRINGS_TO_MAP AND STRING_TYPE.  THE CODE SHOULD HANDLE ALL CASES ##

    indicator_mapping = {}

    distinct_indicator_strings = list(set(indicator_strings))

    for indicator_string in distinct_indicator_strings:


        try:
            ## TO DO - CHANGE THIS TO GET_OR_CREATE ##
            source_indicator = SourceIndicator.objects.create(
                indicator_string = indicator_string,
                document_id = document_id,
            )
        except IntegrityError:

            source_indicator = SourceIndicator.objects.get(
                indicator_string = indicator_string)


        try:
            indicator_id = IndicatorMap.objects.get(source_indicator_id = \
                source_indicator.id).master_indicator_id

            indicator_mapping[indicator_string] = indicator_id


        except ObjectDoesNotExist as e:
            print e
            pass
        except AttributeError as e:
            print e
            pass

    return indicator_mapping


def map_campaigns(campaign_strings,document_id):

    campaign_mapping = {}

    distinct_campaign_strings = list(set(campaign_strings))



    for campaign in distinct_campaign_strings:

        try:
            source_campaign = SourceCampaign.objects.create(
            ## TO DO - CHANGE THIS TO GET_OR_CREATE ##
                campaign_string = campaign,
                document_id = document_id,
            )
        except IntegrityError:
            source_campaign = SourceCampaign.objects.get(
                campaign_string = campaign)


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
            source_region = SourceRegion.objects.create(\
                ## TO DO - CHANGE THIS TO GET_OR_CREATE ##
                region_string=region_string,
                document_id = document_id)
        except IntegrityError:
            source_region = SourceRegion.objects.get(region_string=region_string)


        try:
            region_id = RegionMap.objects.get(source_region_id = \
                source_region.id).master_region_id

            region_mapping[region_string] = region_id
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass


    return region_mapping
