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


    def __init__(self,source_datapoint_ids,user_id,document_id,indicator_id):

        self.document_id = document_id
        self.user_id = user_id
        self.indicator_id = indicator_id

        self.source_datapoint_ids = source_datapoint_ids
        self.source_region_ids, self.source_campaign_id\
            , self.source_indicator_ids = [],[],[]

        self.sdp_df = DataFrame(list(SourceDataPoint.objects.filter(id__in =\
            self.source_datapoint_ids).values()))

        self.new_datapoints = []


    def create_source_meta_data(self):
        '''
        based on the source datapoints, create the source_regions /
        source_campaigns / source indicators/
        '''

        ## campaigns ##
        campaign_strings = self.sdp_df['campaign_string'].unique()
        for c in campaign_strings:

            created, s_c_obj = SourceCampaign.objects.get_or_create(
                campaign_string = c,
                document_id = self.document_id,
                source_guid = ('%s - %s',( self.document_id, c )))


        ## indicators ##
        indicator_strings = self.sdp_df['indicator_string'].unique()
        for i in indicator_strings:

            created, s_i_obj = SourceIndicator.objects.get_or_create(
                indicator_string = i,
                document_id = self.document_id,
                source_guid = ('%s - %s',( self.document_id, i )))

        # regions #
        region_codes = self.sdp_df['region_code'].unique()
        for r in region_codes:

            created, s_r_obj = SourceRegion.objects.get_or_create(
                region_code = r,
                region_string = r,
                document_id = self.document_id,
                source_guid = ('%s - %s',( self.document_id, r )))


    def source_dps_to_dps(self):

        sdps_to_sync = SourceDataPoint.objects.raw('''
            SELECT
                  sd.id
                , sd.cell_value
                , rm.master_region_id
                , cm.master_campaign_id
                , im.master_indicator_id
            FROM source_datapoint sd
            INNER JOIN source_region sr
            	ON sd.region_code = sr.region_code
            INNER JOIN region_map rm
             	ON sr.id = rm.source_region_id
            INNER JOIN source_indicator si
            	ON sd.indicator_string = si.indicator_string
            INNER JOIN indicator_map im
             	ON si.id = im.source_indicator_id
            INNER JOIN source_campaign sc
            	ON sd.campaign_string = sc.campaign_string
            INNER JOIN campaign_map cm
             	ON sc.id = im.source_indicator_id
            WHERE sd.document_id = %s
            AND NOT EXISTS (
                 SELECT 1 FROM datapoint d
                 WHERE sd.id = d.source_datapoint_id)
            ''', [self.document_id])


        for row in sdps_to_sync:

            created, dp = DataPoint.objects.get_or_create(
                campaign_id = row.master_campaign_id,
                indicator_id = row.master_indicator_id,
                region_id = row.master_region_id,
                defaults = {
                    'value':row.cell_value,
                    'source_datapoint_id': row.id,
                    'changed_by_id': self.user_id
                })

            ## if this datapoint exists and was not added by a human ##
            if created == 0 and dp.source_datapoint_id > 0:

                dp.source_datapoint_id = row.source_datapoint_id
                dp.value = row.cell_value
                dp.changed_by_id = self.user.id
                dp.save()


    def delete_un_mapped(self):

        datapoint_ids = MissingMapping.objects.filter(document_id=\
            self.document_id).values_list('datapoint_id',flat=True)

        MissingMapping.objects.filter(document_id=self.document_id).delete()

        DataPoint.objects.filter(id__in=datapoint_ids).delete()



    def sync_regions(self):

        mapped_source_regions = RegionMap.objects.filter(source_region__document_id=self.document_id)


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
