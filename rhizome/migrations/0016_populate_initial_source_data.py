# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models
from django.db.utils import IntegrityError
import pandas as pd

from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.models import Location, LocationPolygon, Indicator, Campaign,\
    LocationType, Office, CampaignType, IndicatorTag, SourceObjectMap,\
    DataPointComputed

from rhizome.models import *
from rhizome.etl_tasks.transform_upload import DateDocTransform
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
    xl = pd.ExcelFile('iraq_data.xlsx')

    source_sheet_df = xl.parse(odk_form_sheet_name)

    mdf = MetaDataGenerator(source_sheet_df)
    mdf.main()

    datapoint_id_list = DataPoint.objects.all().values_list('id', flat=True)

    iraq_data = DataPointComputed.objects.filter(
        location__name = 'Iraq'
    ).values()

    if len(datapoint_id_list) == 0:
        raise Exception('No data for Iraq')

class MetaDataGenerator:

    def __init__(self, source_sheet_df):

        self.country = 'Iraq'
        # self.campaign_type = CampaignType.objects.get(name='IDP Survey')
        self.tag, created = IndicatorTag.objects.get_or_create(tag_name='IDP Survey')
        self.source_sheet_df = source_sheet_df
        self.source_sheet_df['COUNTRY'] = self.country
        self.office = Office.objects\
            .get(name = self.country)

        self.top_lvl_location = Location.objects\
            .get(name = self.country)

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

        ## the names in the shape file are different from ODK ##
        # { ODK_NAME: HIGH_CHART_NAME }
        self.location_lookup = {'Anbar':'Al-Anbar',
            'Basrah':'Al-Basrah',
            'Muthanna':'Al-Muthannia',
            'Qadissiya':'Al-Qadisiyah',
            'An-Najaf':'An-Najaf',
            'Erbil':'Arbil',
            'Sulaymaniyah':'As-Sulaymaniyah',
            'Kirkuk': "At-Ta'mim",
            'Babylon':'Babil',
            'Baghdad':'Baghdad',
            'Thi_Qar':'Dhi-Qar',
            'Dahuk':'Dihok',
            'Diyala':'Diyala',
            'Karbala''':'Karbala',
            'Missan':'Maysan',
            'Ninewa':'Ninawa',
            'Salah_al_Din':'Sala ad-Din',
            'Wassit':'Wasit'
        }

        self.indicator_lookup = {
            'RRM_Distribution/group_distribution/rrm_kits': 'RRM Kits Distributed',
            'RRM_Distribution/group_distribution/plumpy' : 'Plumpy Bars Distributed',
            'RRM_Distribution/group_distribution/families': 'Families Seen',
            'RRM_Distribution/group_distribution/singles': 'Singles Seen'
        }

    def main(self):

        self.create_doc()
        self.build_meta_data_from_source()

        ## hack - fixme ##
        self.source_sheet_df['month_and_year'] = \
            self.source_sheet_df[self.odk_file_map['date_column']]\
            .apply(lambda x: unicode(x.year) + '-' + unicode(x.month))

        self.process_source_sheet()

        # indicators = Indicator.objects.all()
        # if len(indicators) < 10:
        #     raise Exception()

    def build_meta_data_from_source(self):

        indicator_ids = self.build_indicator_meta()
        location_ids = self.build_location_meta()

    def build_indicator_meta(self):

        batch = []

        df_columns = self.source_sheet_df.columns
        config_columns = self.odk_file_map.values()
        indicators = df_columns #set(df_columns).intersection(set(config_columns))

        for ind in indicators:

            try:
                ind_name = self.indicator_lookup[ind]
                ind_obj = Indicator.objects.create(**{
                    'name':ind_name,
                    'short_name':ind_name,
                    'description':ind_name
                })
                som_obj = SourceObjectMap.objects.create(**{
                    'master_object_id': ind_obj.id,
                    'content_type': 'indicator',
                    'source_object_code': ind
                })

                doc_som = DocumentSourceObjectMap.objects.create(
                    document_id = self.document.id,
                    source_object_map_id = som_obj.id
                )

            except KeyError:
                pass

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

            source_code = str(month_dict['month_and_year'])[:7]
            SourceObjectMap.objects.create(
                master_object_id = c.id,
                source_object_code = source_code,
                content_type = 'campaign'
            )

    def build_location_meta(self):

        ## PROVINCE ##
        ## since we ingested the shapes first, we lookup the province name,
        ## then change it to what the ODK form has.. this allows us to attach
        ## the shapes to the location IDS from ODK so that they are familiar
        ## to the owners of the data

        province_column = self.odk_file_map['province_column']
        province_df = pd.DataFrame(self.source_sheet_df[province_column])

        province_column = self.odk_file_map['province_column']
        for ix, row in province_df.iterrows():

            row_dict = row.to_dict()

            province_name = row_dict[province_column]

            try:

                existing_location_name = self.location_lookup[province_name]

                location_obj = Location.objects\
                    .get(name = existing_location_name)

            except KeyError:
                location_obj, created = Location.objects.get_or_create(
                    name = province_name,
                    defaults = {
                    'location_code': province_name,
                    'office_id': self.office.id,
                    'parent_location_id': self.top_lvl_location.id,
                    'location_type_id': LocationType.objects\
                        .get(name = 'Province').id
                })
            self.existing_location_map[province_name] = location_obj.id

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
        # SourceObjectMap.objects.bulk_create(source_object_map_batch)

        ## now let me change the names of the locations
        ##  so that they are familiar to the progam

        for k,v in self.location_lookup.iteritems():

            try:
                l = Location.objects.get(name=v)
                l.name = k
                l.location_code = k
                l.save()
            except Location.DoesNotExist:  ## LOOK INTO THIS....
                pass

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
                location_code = str(loc[location_name_column]) + ' - ' + \
                    str(admin_level)
            except KeyError:
                location_code = loc[location_name_column]

            batch.append(Location(**{
                'name': location_code,
                'location_code': location_code,
                'parent_location_id': self.existing_location_map[loc['parent']],
                'location_type_id': location_type_id,
                'office_id': self.office.id
            }))

        # Location.objects.filter(location_type__name=admin_level).delete()
        Location.objects.bulk_create(batch)

        ## now add these ids to the parent map for later lookups ##
        location_name_to_id_list_of_lists = list(Location.objects\
            .filter(location_type_id=location_type_id)\
            .values_list('location_code','id'))

        for locName, locId in location_name_to_id_list_of_lists:
            self.existing_location_map[locName] = locId

        for k,v in self.existing_location_map.iteritems():
            som_obj, created = SourceObjectMap.objects.get_or_create(
                content_type = 'location',
                source_object_code = k,
                defaults = {'master_object_id': v}
            )
            doc_som_obj, created = DocumentSourceObjectMap.objects.get_or_create(
                source_object_map_id = som_obj.id,
                document_id = self.document.id
            )
    ## make source object maps ##
    def model_df_to_data(model_df,model):

        meta_ids = []

        non_null_df = model_df.where((pd.notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids

    def create_doc(self):

        self.user_id = -1
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

        self.document = new_doc

    def process_source_sheet(self):

        create_doc_details(self.document.id)

        ## document -> source_submissions ##
        dt = DateDocTransform(self.user_id, self.document.id, self.source_sheet_df)
        dt.process_file()

        ## source_submissions -> datapoints ##
        mr = MasterRefresh(self.user_id, self.document.id)
        mr.main()


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
        ('rhizome', '0014_unique_index_agg_refresh'),
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
# u'RRM_Distribution/group_distribution/irr_kits',
# u'RRM_Distribution/group_distribution/dignity_kits',
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
