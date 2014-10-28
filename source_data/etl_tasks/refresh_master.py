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
from source_data.models import ProcessStatus,SourceDataPoint
from datapoints.models import DataPoint


class MasterRefresh(object):


      def __init__(self,source_datapoints,user_id,document_id):

          self.document_id = document_id
          self.source_datapoints = source_datapoints
          self.user_id = user_id

          self.new_datapoints = []


      def main(self):

          self.mappings = self.get_mappings()
          for sdp in self.source_datapoints:

              err, datapoint = self.process_source_datapoint_record(sdp=sdp)

              print '=='
              print err
              print '=='
              print err

              if err:
                  sdp.error_msg = err
                  sdp.save()


      def get_mappings(self):

          mappings = {}

          mappings['regions'] = map_regions([sdp.region_string for sdp in self.source_datapoints],self.document_id)
          mappings['indicators'] = map_indicators([sdp.indicator_string for sdp in self.source_datapoints],self.document_id)
          mappings['campaigns'] = map_campaigns([sdp.campaign_string for sdp in self.source_datapoints],self.document_id)

          return mappings


      def process_source_datapoint_record(self,sdp):

          try:
              indicator_id = self.mappings['indicators'][sdp.indicator_string]
              region_id = self.mappings['regions'][sdp.region_string]
              campaign_id = self.mappings['campaigns'][sdp.campaign_string]
          except KeyError:
              err = traceback.format_exc()
              return err, None

          sdp.cell_value = locale.atoi(sdp.cell_value)
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
              record.save()
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
              print '==='
              print err
              print '==='
              print err
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
