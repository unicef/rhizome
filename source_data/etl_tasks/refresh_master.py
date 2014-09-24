

from django.db import IntegrityError
from django.core.exceptions import ValidationError

from datapoints.models import DataPoint


class MasterRefresh(object):


      def __init__(self,mappings,records,user_id):

          self.mappings = mappings
          self.records = records
          self.user_id = user_id

          self.main()

      def main(self):

          for record in self.records:
              self.process_source_datapoint_record(record)


      def process_source_datapoint_record(self,record):

          try:
              indicator_id = self.mappings['indicators'][record.indicator_string]
          except KeyError:
              return

          try:
              region_id = self.mappings['regions'][record.region_string]
          except KeyError:
              return


          try:
              campaign_id = self.mappings['campaigns'][record.campaign_string]
          except KeyError:
              return


          try:
              datapoint, created = DataPoint.objects.get_or_create(
                  indicator_id = indicator_id,
                  region_id = region_id,
                  campaign_id = campaign_id,
                  value = record.cell_value,
                  changed_by_id = self.user_id,
                  source_datapoint_id = record.id
              )

          ## STORE THE ERROR MESSAGE SOMEWHERE FOR USER TO REVIEW ##
          except IntegrityError:
              pass
          except ValidationError:
              pass
              # NEEDS TO BE HANDLED BY GENERIC VALIDATION MODULE
