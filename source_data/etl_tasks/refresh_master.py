import pprint as pp
import traceback
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import datetime

from decimal import InvalidOperation

from django.db import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError

from source_data.etl_tasks.shared_utils import map_indicators,map_campaigns,map_regions
from source_data.models import *
from datapoints.models import *


class MasterRefresh(object):


    def __init__(self,source_datapoints,user_id,document_id):

        self.document_id = document_id
        self.source_datapoints = source_datapoints
        self.user_id = user_id

        self.new_datapoints = []


    def main(self):

        self.delete_un_mapped()
        self.sync_regions()

        self.mappings = self.get_mappings()
        for sdp in self.source_datapoints:

          err, datapoint = self.process_source_datapoint_record(sdp=sdp)

          if err:
              sdp.error_msg = err
              sdp.save()


    def delete_un_mapped(self):

        datapoint_ids = MissingMapping.objects.filter(document_id=\
            self.document_id).values_list('datapoint_id',flat=True)

        MissingMapping.objects.filter(document_id=self.document_id).delete()

        DataPoint.objects.filter(id__in=datapoint_ids).delete()


    def sync_regions(self):

        mapped_source_regions = RegionMap.objects.filter(source_region__document_id=self.document_id)


        for sr in mapped_source_regions:

            source_polygon = SourceRegionPolygon.objects.get(source_region=\
                sr.source_region)

            master_polygon = RegionPolygon.objects.get_or_create(
                region = sr.master_region,
                defaults = { 'shape_len': source_polygon.shape_len,
                    'shape_area':source_polygon.shape_area,
                    'polygon': source_polygon.polygon
                })

        # SourceRegion.objects.filter(document_id=\


    def get_mappings(self):

        mappings = {}

        mappings['regions'] = map_regions([sdp.region_string for sdp in self.source_datapoints],self.document_id)
        mappings['indicators'] = map_indicators([sdp.indicator_string for sdp in self.source_datapoints],self.document_id)
        mappings['campaigns'] = map_campaigns([sdp.campaign_string for sdp in self.source_datapoints],self.document_id)

        return mappings


    def process_source_datapoint_record(self,sdp):

        try:
            indicator_id = self.mappings['indicators'][sdp.indicator_string]
            region_id = self.mappings['regions'][sdp.region_string] # hack!
            campaign_id = self.mappings['campaigns'][sdp.campaign_string]
        except KeyError:
            err = traceback.format_exc()
            return err, None

        sdp.cell_value = sdp.cell_value.replace(',','')
        sdp.save()

        try:
            with transaction.atomic():
                datapoint = DataPoint.objects.create(
                      indicator_id = indicator_id,
                      region_id = region_id,
                      campaign_id = campaign_id,
                      value = sdp.cell_value,
                      changed_by_id = self.user_id,
                      source_datapoint_id = sdp.id
                )
                self.new_datapoints.append(datapoint.id)
            sdp.status_id = ProcessStatus.objects.get(status_text='SUCCESS_INSERT').id
            sdp.save()
            self.new_datapoints.append(datapoint.id)

        except IntegrityError:
            err, datapoint = self.handle_dupe_record(sdp,indicator_id,region_id,campaign_id)
            return err,datapoint
        except ValidationError:
            err = traceback.format_exc()
            return err, None
        except InvalidOperation:
            err = traceback.format_exc()
            return err, None
        except TypeError:
            err = traceback.format_exc()
            return err, None
        except Exception:
            err = traceback.format_exc()
            return err, None

        return None, datapoint


    def handle_dupe_record(self,sdp,indicator_id,region_id,campaign_id):

        datapoint = DataPoint.objects.get(
            indicator_id = indicator_id,
            region_id = region_id,
            campaign_id = campaign_id,
        )

        original_sdp = SourceDataPoint.objects.get(id=datapoint.source_datapoint_id)

        if original_sdp.created_at.replace(tzinfo=None) <= sdp.created_at.replace(tzinfo=None):

            datapoint.value = sdp.cell_value
            datapoint.source_datapoint_id = sdp.id

            datapoint.save()

            sdp.status = ProcessStatus.objects.get(status_text= "SUCCESS_UPDATE")
            sdp.save()

            original_sdp.status = ProcessStatus.objects.get(status_text= "OVERRIDDEN")
            original_sdp.save()

            return None, datapoint

        else:
            sdp.status = ProcessStatus.objects.get(status_text= "OVERRIDDEN")
            sdp.save()

            return None, datapoint
