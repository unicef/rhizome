import pprint as pp
import traceback
from decimal import InvalidOperation

from django.db import IntegrityError
from django.core.exceptions import ValidationError

from source_data.etl_tasks.shared_utils import map_indicators,map_campaigns,map_regions
from datapoints.models import DataPoint


class MasterRefresh(object):


      def __init__(self,records,user_id):

          self.records = records
          self.user_id = user_id

          self.new_datapoints = []


      def main(self):

          print 'getting mappppingssss!!!'

          self.mappings = self.get_mappings()

          print 'mappppingssss gt!!!'

          for record in self.records:

              err, datapoint_id = self.process_source_datapoint_record(record)

              if err:
                  record.error_msg = err
                  record.save()


      def get_mappings(self):

          # THIS IS FLAWED make sure there are no dupe sources for the sdps
          source_id = self.records[0].source_id

          mappings = {}

          mappings['regions'] = map_regions([sdp.region_string for sdp in self.records],source_id)
          mappings['indicators'] = map_indicators([sdp.indicator_string for sdp in self.records],source_id)
          mappings['campaigns'] = map_campaigns([sdp.campaign_string for sdp in self.records],source_id)

          return mappings


      def process_source_datapoint_record(self,record):

          try:
              indicator_id = self.mappings['indicators'][record.indicator_string]
              region_id = self.mappings['regions'][record.region_string]
              campaign_id = self.mappings['campaigns'][record.campaign_string]
          except KeyError:
              err = traceback.format_exc()
              return err, None

          try:
              datapoint,created = DataPoint.objects.get_or_create(
                  indicator_id = indicator_id,
                  region_id = region_id,
                  campaign_id = campaign_id,
                  value = record.cell_value,
                  changed_by_id = self.user_id,
                  source_datapoint_id = record.id
              )
              self.new_datapoints.append(datapoint.id)

              if not created:
                  self.handle_dupe_record(record, datapoint)

          except ValidationError:
              err = traceback.format_exc()
              return err, None
          except InvalidOperation:
              err = traceback.format_exc()
              return err, None
          except Exception:
              err = traceback.format_exc()
              return err, None

          return None, datapoint.id

      def handle_dupe_record(self,record,datapoint):

          datapoint.value = record.value
          datapoint.source_datapoint_id = record.id

          datapoint.save()

          record.status = Status.objects.get(status_text= "SUCESS_UPDATE").id
          record.save()
