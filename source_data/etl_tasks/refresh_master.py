import traceback

from decimal import InvalidOperation

from django.db import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from pandas import DataFrame

from source_data.etl_tasks.shared_utils import map_indicators,map_campaigns,map_regions
from source_data.models import *
from datapoints.models import *


class MasterRefresh(object):

    def __init__(self,user_id,document_id,indicator_id=None):

        self.document_id = document_id
        self.user_id = user_id
        self.indicator_id = indicator_id

        self.source_ids, self.source_id\
            , self.source_ids = [],[],[]

        self.sdp_df = DataFrame(list(SourceDataPoint.objects\
            .filter(document_id = self.document_id).values()))

        self.new_datapoints = []

    def source_dps_to_dps(self):

        ## get source data for which all metadata is mapped
        ## and the user is permitted to write ##
        sdps_to_sync = SourceDataPoint.objects.raw('''
            SELECT * FROM fn_get_source_dbs_to_sync(%s, %s, %s);
            ''', [self.user_id,self.document_id,self.indicator_id])


        for row in sdps_to_sync:

            cleaned_value = self.clean_cell_value(row.cell_value)

            dp,created = DataPoint.objects.get_or_create(
                campaign_id = row.campaign_id,
                indicator_id = row.indicator_id,
                region_id = row.region_id,
                defaults = {
                    'value': cleaned_value,
                    'source_datapoint_id': row.id,
                    'changed_by_id': self.user_id
                })

            ## if this datapoint exists and was not added by a human ##
            if created == False and dp.id > 0:

                dp.source_datapoint_id = row.id
                dp.value = cleaned_value
                dp.changed_by_id = self.user_id
                dp.save()


    def clean_cell_value(self,cell_value):

        if cell_value == None:
            return None
        # elif cell_value == '':
        #     return None

        try:
            cleaned = float(cell_value.replace(',',''))
        except ValueError:
            return None


        print cleaned
        return

    def delete_un_mapped(self):

        datapoint_ids = MissingMapping.objects.filter(document_id=\
            self.document_id).values_list('datapoint_id',flat=True)

        MissingMapping.objects.filter(document_id=self.document_id).delete()

        DataPoint.objects.filter(id__in=datapoint_ids).delete()


    def sync_regions(self):

        mapped_source_regions = RegionMap.objects.filter(source_object__document_id=self.document_id)


        for sr in mapped_source_regions:

            try:
                source_polygon = SourceRegionPolygon.objects.get(source_region=\
                    sr.source_region)

            except ObjectDoesNotExist:
                return

            master_polygon = RegionPolygon.objects.get_or_create(
                region = sr.master_region,
                defaults = { 'shape_len': source_polygon.shape_len,
                    'shape_area':source_polygon.shape_area,
                    'polygon': source_polygon.polygon
                })

#####
#####

def create_source_meta_data(document_id):
    '''
    based on the source datapoints, create the source_regions /
    source_campaigns / source indicators/
    '''

    sdp_df = DataFrame(list(SourceDataPoint.objects.filter(
        document_id = document_id).values()))

    sr_df = DataFrame(list(SourceRegion.objects.filter(
        document_id = document_id).values()))

    if len(sr_df) > 0 and len(sdp_df) == 0:

        pass

    else:

        ## campaigns ##

        campaign_strings = sdp_df['campaign_string'].unique()

        for cntr,(c) in enumerate(campaign_strings):

            try:
                created, s_c_obj = SourceCampaign.objects.create(
                    campaign_string = c,
                    document_id = document_id,
                    source_guid = ('%s - %s',( document_id, c )))
            except IntegrityError:
                pass
            except TypeError: # fix for POL-332
                pass

        ## indicators ##
        indicator_strings = sdp_df['indicator_string'].unique()

        for i in indicator_strings:

            try:
                s_i_obj = SourceIndicator.objects.create(
                    indicator_string = i,
                    document_id = document_id,
                    source_guid =  ('%s - %s',( document_id, i )))
            except IntegrityError:
                pass

        # regions #
        region_codes = sdp_df['region_code'].unique()

        for r in region_codes:

            try:
                s_r_obj = SourceRegion.objects.create(
                    region_code = r,
                    document_id = document_id,
                    region_string = r,
                    source_guid = ('%s - %s',( document_id, r )))
            except IntegrityError:
                pass
