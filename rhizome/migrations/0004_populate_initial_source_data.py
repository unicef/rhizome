# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models

import pandas as pd

from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.models import Location, LocationPolygon, Indicator, Campaign,\
    LocationType, Office, CampaignType, IndicatorTag, SourceObjectMap,\
    DataPointComputed

from rhizome.models import Document, DocumentDetail, DocDetailType
from rhizome.etl_tasks.transform_upload import ComplexDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh

from pprint import pprint

def populate_source_data(apps, schema_editor):
    '''
    Here, we take an excel file that has the same schema as the database
    we lookup the approriate model and bulk insert.

    We need to ingest the data itself in the same order as the excel
    sheet otherwise we will have foreign key constraint issues.
    '''

    odk_form_sheet_name = 'source-data_idp_odk_form'
    xl = pd.ExcelFile('initial_data.xlsx')

    source_sheet_df = xl.parse(odk_form_sheet_name)

    mdf = MetaDataGenerator(source_sheet_df)
    mdf.main()


class MetaDataGenerator:

    def __init__(self, source_sheet_df):

        self.country = 'Iraq'
        self.campaign_type = CampaignType.objects.create(name='IDP Survey')
        self.tag = IndicatorTag.objects.create(tag_name='IDP Survey')
        self.source_sheet_df = source_sheet_df
        self.source_sheet_df['COUNTRY'] = self.country
        self.office = Office.objects\
            .create(name = self.country)
        self.top_lvl_location = Location.objects\
            .create(
                name = self.country,
                location_code = self.country,
                office_id = self.office.id,
                location_type_id = LocationType.objects.get(name='Country').id,
        )

        self.odk_file_map = {
            'date_column': 'RRM_Distribution/date_assessdistro',
            'lat_column': '',
            'lon_column': '',
            'province_column': 'RRM_Distribution/Governorate',
            'district_column': 'RRM_Distribution/District',
            'city_column': 'RRM_Distribution/Site_City'
        }

        self.admin_level_parent_lookup = {
            # 'Province' : 'COUNTRY',
            'District' : 'RRM_Distribution/Governorate',
            'City' : 'RRM_Distribution/District'
        }

        ## add location_ids here when inserting and use to find the parent ##
        self.existing_location_map = {self.country : self.top_lvl_location.id}

    def main(self):

        self.build_meta_data_from_source()

        ## hack - fixme ##
        self.source_sheet_df['month_and_year'] = \
            self.source_sheet_df[self.odk_file_map['date_column']]\
            .apply(lambda x: unicode(x.year) + '-' + unicode(x.month))

        self.process_source_sheet()

    def build_meta_data_from_source(self):

        indicator_ids = self.build_indicator_meta()
        campaign_ids = self.build_campaign_meta()
        location_ids = self.build_location_meta()

    def build_indicator_meta(self):

        batch = []

        df_columns = self.source_sheet_df.columns
        config_columns = self.odk_file_map.values()
        indicators = df_columns #set(df_columns).intersection(set(config_columns))

        for ind in indicators:

            batch.append(Indicator(**{
                'name':ind,
                'short_name':ind,
                'description':ind
            }))

        Indicator.objects.all().delete()
        Indicator.objects.bulk_create(batch)

        source_object_map_batch = [SourceObjectMap(**{
            'master_object_id': ind.id,
            'content_type': 'indicator',
            'source_object_code': ind.name
        }) for ind in Indicator.objects.all()]
        SourceObjectMap.objects.bulk_create(source_object_map_batch)

    def build_campaign_meta(self):

        date_column = self.odk_file_map['date_column']

        all_date_df = pd.DataFrame(self.source_sheet_df[date_column], columns = [date_column])

        all_date_df['month_and_year'] = all_date_df[date_column]\
            .apply(lambda x: unicode(x.year) + '-' + unicode(x.month))

        gb_df = pd.DataFrame(all_date_df\
            .groupby(['month_and_year'])[date_column].min())
        gb_df.reset_index(level=0, inplace=True)

        for ix, month in gb_df.iterrows():

            month_dict = month.to_dict()
            c = Campaign.objects.create(**{
                'start_date':month_dict[date_column] ,
                'end_date':month_dict[date_column] ,
                'name': month_dict['month_and_year'],
                'campaign_type_id': self.campaign_type.id,
                'office_id': self.office.id,
                'top_lvl_indicator_tag_id': self.tag.id,
                'top_lvl_location_id': self.top_lvl_location.id
            })

            SourceObjectMap.objects.create(
                master_object_id = c.id,
                source_object_code = month_dict['month_and_year'],
                content_type = 'campaign'
            )

    def build_location_meta(self):

        ## PROVINCE ##
        province_column = self.odk_file_map['province_column']
        province_df = pd.DataFrame(self.source_sheet_df[province_column])
        province_df['parent'] = self.country
        province_df.drop_duplicates(inplace=True)

        self.process_location_df(province_df, 'Province')

        # DISTRICT ##
        district_column = self.odk_file_map['district_column']
        district_df = pd.DataFrame(\
            self.source_sheet_df[[district_column,province_column]])
        district_df.drop_duplicates(inplace=True)
        self.process_location_df(district_df, 'District')

        ## CITY ##
        city_column = self.odk_file_map['city_column']
        city_df = pd.DataFrame(\
            self.source_sheet_df[[city_column,district_column]])

        city_df.drop_duplicates(inplace=True,subset=[city_column])
        self.process_location_df(city_df, 'City')

        ## this wil lmake it so we can ingest data
        source_object_map_batch = [SourceObjectMap(**{
            'master_object_id': loc.id,
            'content_type': 'location',
            'source_object_code': loc.location_code
        }) for loc in Location.objects.all()]
        SourceObjectMap.objects.bulk_create(source_object_map_batch)

    def process_location_df(self, location_df, admin_level):

        location_type_id = LocationType.objects.get(name = admin_level).id
        location_name_column = self.odk_file_map[admin_level.lower() + '_column']

        batch = []

        try:
            parent_column = self.admin_level_parent_lookup[admin_level]
            location_df['parent'] = location_df[parent_column]
        except KeyError:
            location_df['parent'] == self.country

        for ix, loc in location_df.iterrows():

            loc_dict = loc.to_dict()

            try:
                ## If a district comes in but there is a province with that
                ## name as well, we concat the name with the admin level in the
                ## except.
                existing_location_id = \
                    self.existing_location_map[loc[location_name_column]]
                location_code = loc[location_name_column] + ' - ' + \
                    admin_level
            except KeyError:
                location_code = loc[location_name_column]

            batch.append(Location(**{
                'name': location_code,
                'location_code': location_code,
                'parent_location_id': self.existing_location_map[loc['parent']],
                'location_type_id': location_type_id,
                'office_id': self.office.id
            }))

        Location.objects.filter(location_type__name=admin_level).delete()
        Location.objects.bulk_create(batch)

        ## now add these ids to the parent map for later lookups ##
        location_name_to_id_list_of_lists = list(Location.objects\
            .filter(location_type_id=location_type_id)\
            .values_list('location_code','id'))

        for locName, locId in location_name_to_id_list_of_lists:
            self.existing_location_map[locName] = locId

    ## make source object maps ##
    def model_df_to_data(model_df,model):

        meta_ids = []

        non_null_df = model_df.where((pd.notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids


    def process_source_sheet(self):

        user_id = -1
        sheet_name = 'source-data_idp_odk_form'
        # file_loc = settings.MEDIA_ROOT + sheet_name
        # saved_csv_file_location = settings.MEDIA_ROOT + sheet_name + '.csv'

        doc_file_text = sheet_name + '.csv'
        # self.source_sheet_df.to_csv(doc_file_text)
        # doc_file_text = sheet_name + '.csv'

        new_doc = Document.objects.create(
            doc_title = doc_file_text,
            guid = 'test'
        )

        create_doc_details(new_doc.id)

        ## document -> source_submissions ##
        dt = ComplexDocTransform(user_id, new_doc.id, self.source_sheet_df)
        dt.main()

        ## source_submissions -> datapoints ##
        mr = MasterRefresh(user_id, new_doc.id)
        mr.main()

        ## datapoints -> computed datapoints ##
        for c in Campaign.objects.all():
            print 'processing campaign id: %s' % c.id
            ar = AggRefresh(c.id)
            print 'DWC COUNT %s' % len(DataPointComputed.objects\
                .filter(campaign_id = c.id))

def create_doc_details(doc_id):

    doc_detail_types = ['uq_id_column', 'date_column', 'location_column']

    for dd_type in doc_detail_types:
        DocumentDetail.objects.create(
            document_id = doc_id,
            doc_detail_type_id = DocDetailType.objects.get(name = dd_type).id,
            doc_detail_value = dd_type ## this implies that the source columns
                                        ## are named with the above convention
        )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0003_reset_sql_sequence'),
    ]

    operations = [
        migrations.RunPython(populate_source_data),
    ]

# u'start',
# u'end',
# u'deviceid',
# u'RRM_Distribution/date_assessdistro',
# u'RRM_Distribution/Governorate',
# u'RRM_Distribution/District',
# u'RRM_Distribution/Site_City',
# u'RRM_Distribution/Enumerator',
# u'RRM_Distribution/Enumerator_Organisation',
# u'RRM_Distribution/Enumerator_LocalOrg',
# u'RRM_Distribution/Enumerator_Phone',
# u'RRM_Distribution/GPS_coord',
# u'RRM_Distribution/_GPS_coord_latitude',
# u'RRM_Distribution/_GPS_coord_longitude',
# u'RRM_Distribution/_GPS_coord_altitude',
# u'RRM_Distribution/_GPS_coord_precision',
# u'RRM_Distribution/group_photo/photoreceiver',
# u'RRM_Distribution/group_photo/onemorephoto',
# u'RRM_Distribution/group_photo/photoreceiver2',
# u'RRM_Distribution/community_focal_person/Name_community_focalp',
# u'RRM_Distribution/community_focal_person/telephone_number',
# u'RRM_Distribution/community_origin/Governorate_origin1',
# u'RRM_Distribution/community_origin/District_origin1',
# u'RRM_Distribution/community_origin/Site_City_origin1',
# u'RRM_Distribution/community_origin/Governorate_origin2',
# u'RRM_Distribution/community_origin/District_origin2',
# u'RRM_Distribution/community_origin/Site_City_origin2',
# u'RRM_Distribution/community_origin/leave_Date',
# u'RRM_Distribution/group_distribution/idp_refugee',
# u'RRM_Distribution/group_distribution/area',
# u'RRM_Distribution/group_distribution/rrmtype/RRM_IRR',
# u'RRM_Distribution/group_distribution/rrmtype/RRM_only',
# u'RRM_Distribution/group_distribution/rrmtype/IRR_only',
# u'RRM_Distribution/group_distribution/rrmtype/Dignity_kits',
# u'RRM_Distribution/group_distribution/rrm_kits',
# u'RRM_Distribution/group_distribution/irr_kits',
# u'RRM_Distribution/group_distribution/dignity_kits',
# u'RRM_Distribution/group_distribution/plumpy',
# u'RRM_Distribution/group_distribution/families',
# u'RRM_Distribution/group_distribution/singles',
# u'RRM_Distribution/other_needs/the_1st_Need',
# u'RRM_Distribution/other_needs/the_2nd_Need',
# u'RRM_Distribution/other_needs/the_3rd_Need',
# u'RRM_Distribution/other_needs/other_need',
# u'RRM_Distribution/group_destination/moving1',
# u'RRM_Distribution/group_destination/moving1_gov',
# u'RRM_Distribution/group_destination/moving1_dist',
# u'RRM_Distribution/group_destination/moving1_loc',
# u'RRM_Distribution/group_destination/moving2',
# u'RRM_Distribution/group_destination/moving2_gov',
# u'RRM_Distribution/group_destination/moving2_dist',
# u'RRM_Distribution/group_destination/moving2_loc',
# u'RRM_Distribution/group_destination/moving_why/safety',
# u'RRM_Distribution/group_destination/moving_why/services',
# u'RRM_Distribution/group_destination/moving_why/family_friends',
# u'RRM_Distribution/group_destination/moving_why/job',
# u'RRM_Distribution/group_destination/moving_why/othermov',
# u'RRM_Distribution/group_destination/moving_whyot',
# u'RRM_Distribution/group_comments/comments',
# u'meta/instanceID',
# u'_uuid',
# u'_submission_time',
# u'_tags',
# u'_notes',
# u'_version',
# u'_duration',
# u'_submitted_by'],
