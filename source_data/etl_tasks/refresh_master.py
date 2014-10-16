import pprint as pp
import traceback
import datetime
from decimal import InvalidOperation

from django.db import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError

from source_data.etl_tasks.shared_utils import map_indicators,map_campaigns,map_regions
from source_data.models import ProcessStatus,SourceDataPoint
from datapoints.models import DataPoint


class MasterRefresh(object):


      def __init__(self,records,user_id):

          self.records = records
          self.user_id = user_id

          self.new_datapoints = []


      def main(self):

          self.mappings = self.get_mappings()
          for record in self.records:

              err, datapoint = self.process_source_datapoint_record(record)

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
          print 'TRYING \n' *10


          try:
              indicator_id = self.mappings['indicators'][record.indicator_string]
              region_id = self.mappings['regions'][record.region_string]
              campaign_id = self.mappings['campaigns'][record.campaign_string]
          except KeyError:
              err = traceback.format_exc()
              return err, None

          try:
              with transaction.atomic():
                  datapoint = DataPoint.objects.create(
                      indicator_id = indicator_id,
                      region_id = region_id,
                      campaign_id = campaign_id,
                      value = record.cell_value,
                      changed_by_id = self.user_id,
                      source_datapoint_id = record.id
                  )
              record.status_id = ProcessStatus.objects.get(status_text='SUCCESS_INSERT').id
              self.new_datapoints.append(datapoint.id)

          except IntegrityError:
              err, datapoint = self.handle_dupe_record(record,indicator_id,region_id,campaign_id)
              return err, datapoint

          except ValidationError:
              err = traceback.format_exc()
              return err, None
          except InvalidOperation:
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

          print original_sdp.created_at
          print sdp.created_at


          if original_sdp.created_at.replace(tzinfo=None) <= sdp.created_at.replace(tzinfo=None):

              datapoint.value = sdp.cell_value
              datapoint.source_datapoint_id = sdp.id

              datapoint.save()

              sdp.status = ProcessStatus.objects.get(status_text= "SUCCESS_UPDATE")
              sdp.save()

              original_sdp.status = ProcessStatus.objects.get(status_text= "OVERRIDEN")
              original_sdp.save()

              return None, datapoint

          else:
              print 'wudddup\n' *10

              sdp.status = Status.objects.get(status_text= "OVERRIDEN")
              record.save()

              return None, datapoint
