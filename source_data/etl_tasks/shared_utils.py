from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from source_data.models import *
from datapoints.models import Office

def pivot_and_insert_src_datapoints(df,document_id,column_mappings):

    header = [col for col in df]
    source_datapoints = []

    source_id = Source.objects.get(source_name='data entry').id

    for row_number,(row) in enumerate(df.values):

        batch = []

        region_code = row[header.index(column_mappings['region_code_col'])]
        campaign_string = row[header.index(column_mappings['campaign_col'])]
        to_process_status = ProcessStatus.objects.get(status_text='TO_PROCESS').id

        for cell_no,(column_header) in enumerate(header):

            indicator_string = header[cell_no]

            row_guid =  'doc_id: ' + str(document_id) + ' row_no: ' + \
                str(row_number) + ' cell_no: ' + str(cell_no)

            sdp_dict = {
                'source_guid':row_guid,
                'guid':row_guid,
                'indicator_string': indicator_string,
                'region_code':region_code,
                'campaign_string':campaign_string,
                'cell_value':row[cell_no],
                'row_number':row_number,
                'source_id':source_id,
                'document_id':document_id,
                'status_id':to_process_status
            }

            sdp = SourceDataPoint(**sdp_dict)

            batch.append(sdp)

        SourceDataPoint.objects.bulk_create(batch)


    sdps = SourceDataPoint.objects.filter(document_id=document_id)
    return sdps
    # return source_datapoints

def map_indicators(indicator_strings,document_id):
    ## THESE METHODS NEED TO BE ABSTRACTED SO THAT YOU PASS DOCUMENT_ID  ##
    ## STRINGS_TO_MAP AND STRING_TYPE.  THE CODE SHOULD HANDLE ALL CASES ##

    indicator_mapping = {}

    distinct_indicator_strings = list(set(indicator_strings))

    for indicator_string in distinct_indicator_strings:


        source_indicator,created = SourceIndicator.objects.get_or_create(
            indicator_string = indicator_string,
            defaults = {'document_id': document_id})

        try:
            indicator_id = IndicatorMap.objects.get(source_object_id = \
                source_indicator.id).master_object_id

            indicator_mapping[indicator_string] = indicator_id


        except ObjectDoesNotExist as e:
            print e
            pass
        except AttributeError as e:
            print e
            pass

    return indicator_mapping


def map_campaigns(campaign_strings,document_id):

    offices = [u'Nigeria',u'Afghanistan',u'Pakistan']

    campaign_mapping = {}

    distinct_campaign_strings = list(set(campaign_strings))


    for campaign in distinct_campaign_strings:

        ## parse the office string
        campaign_split = set(campaign.split(' '))

        print campaign_split

        ## put a try / excpet here to ensure that the campaign exists
        office_string = str(list(campaign_split.intersection(set(offices)))[0])

        office_obj = Office.objects.get(name = office_string)

        source_campaign,created = SourceCampaign.objects.get_or_create(
            campaign_string = campaign,
            defaults = {'document_id':document_id,'office':office_obj})

        try:
            campaign_id = CampaignMap.objects.get(source_object_id = \
                source_campaign.id).master_object_id

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

        print 'region string'

        try:
            source_region,created = SourceRegion.objects.get_or_create(\
                    region_string=region_string,
                    document_id = document_id,
                    region_type = 'UKNOWN',
                    country = 'UNKNOWN')
        except IntegrityError:
            source_region = None


        try:
            region_id = RegionMap.objects.get(source_object_id = \
                source_region.id).master_object_id

            region_mapping[region_string] = region_id
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass


    return region_mapping
