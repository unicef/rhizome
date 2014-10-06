import sys,os
import pandas as pd
import traceback

sys.path.append('/Users/johndingee_seed/code/UF04/polio')
sys.path.append('/Users/johndingee_seed/code/UF04/polio/polio')

os.environ['DJANGO_SETTINGS_MODULE'] = 'prod_settings'

from source_data.models import VCMSettlement, SourceRegion
from datapoints.models import Indicator,Region,Source,Office,RegionRelationshipType,RegionRelationship
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

def seed_regions():

    to_process_df = pd.DataFrame(list(VCMSettlement.objects.values()))
    cols = [col.lower() for col in to_process_df]

    for row in to_process_df.values:
        row_dict = {}

        row_dict['full_name'] = row[cols.index('settlementname')]
        row_dict['region_code'] = row[cols.index('settlementcode')]
        row_dict['latitude'] = row[cols.index('settlementgps_latitude')]
        row_dict['longitude'] = row[cols.index('settlementgps_longitude')]
        row_dict['source_guid'] = row[cols.index('key')]
        row_dict['source_id'] = Source.objects.get(source_name='data entry').id
        row_dict['office_id'] = Office.objects.get(name='Nigeria').id

        try:
            Region.objects.create(**row_dict)
        except IntegrityError:
            err = traceback.format_exc()
            print err

def seed_indicators():

    df = pd.read_csv('/Users/johndingee_seed/Desktop/johns_inds.csv')

    for row in df.values:
        to_create = {}

        to_create['name'] =  row[0]
        to_create['description'] =  row[1]
        to_create['is_reported'] =  1

        try:
            Indicator.objects.create(**to_create)

        except Exception as e:
            print e

def create_region_heirarchy():

    df = pd.read_csv('/Users/johndingee_seed/code/UF04/polio/source_data/nigeria_regions.csv')

    cols = df.columns
    cols = list(cols)

    for row in df.values:
        print row

    ## CREATE STATES ##

        state_dict = {}
        state_dict['full_name'] = row[cols.index('State')]
        state_dict['region_type'] = 'STATE'
        state_dict['region_code'] = row[cols.index('StateCode')]
        state_dict['source_guid'] = row[cols.index('State')] + ' - ' + row[cols.index('LGAName')]
        state_dict['source_id'] = Source.objects.get(source_name='data entry').id
        state_dict['office_id'] = Office.objects.get(name='Nigeria').id

        try:
            state, created = Region.objects.get_or_create(**state_dict)
            print state.id
        except IntegrityError as e:
              print e

    ## CREATE LGAS ##

        lga_dict = {}
        lga_dict['full_name'] = row[cols.index('LGAName')]
        lga_dict['region_type'] = 'LGA'
        lga_dict['region_code'] = row[cols.index('LGACodetxt')]
        lga_dict['source_guid'] = row[cols.index('LGAName')] + ' - ' + str(row[cols.index('LGACodetxt')])
        lga_dict['source_id'] = Source.objects.get(source_name='data entry').id
        lga_dict['office_id'] = Office.objects.get(name='Nigeria').id

        try:
            lga, created = Region.objects.get_or_create(**lga_dict)
            print state.id
        except IntegrityError as e:
              print e


    ## CREATE STATE -> LGA RELATIONSHIP ##

        state_to_lga_dict = {}

        state_to_lga_dict['region_0'] = Region.objects.get(full_name=row[cols.index('State')])
        state_to_lga_dict['region_1'] = Region.objects.get(full_name=row[cols.index('LGAName')])
        state_to_lga_dict['region_relationship_type'] = RegionRelationshipType.objects.get(display_name = 'contains')

        try:
            rr, created = RegionRelationship.objects.get_or_create(**state_to_lga_dict)
            print rr.id
        except IntegrityError as e:
              print e

    ## CREATE LGA -> SETTLEMENT RELATIONSHIP

def lga_sett_relationships():
    setts = Region.objects.filter(region_type='SETTLEMENT')
    for sett in setts:

        sett_first_four = sett.region_code[:4]
        print sett.region_code

        try:
            lga = Region.objects.get(region_type='LGA',region_code=sett_first_four)
            print lga.id

            rr_dict = {}
            rr_dict['region_0'] = lga
            rr_dict['region_1'] = sett
            rr_dict['region_relationship_type'] = RegionRelationshipType.objects.get(display_name = 'contains')

            rr, created = RegionRelationship.objects.get_or_create(**rr_dict)

            print "CREATED!"
            print rr.id

        except ObjectDoesNotExist as e:
            print e

        except IntegrityError as e:
              print e





if __name__ == "__main__":
    create_region_heirarchy()
    lga_sett_relationships()
