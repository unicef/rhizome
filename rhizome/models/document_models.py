import hashlib
import random
import json
import locale
import re
from collections import defaultdict
import math
from dateutil.parser import parse

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from pandas import read_csv
from pandas import notnull
from pandas import DataFrame
from pandas import to_datetime

from bulk_update.helper import bulk_update
from jsonfield import JSONField

from rhizome.models.location_models import Location
from rhizome.models.indicator_models import Indicator
from rhizome.models.campaign_models import Campaign

class CacheJob(models.Model):
    '''
    A table that shows the start/end time of each cache job, as well as the
    response message of the job itself.  This allows a DBA to track what is
    happening with our cache jobs and how long they are taking.
    '''

    date_attempted = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True)
    is_error = models.BooleanField()
    response_msg = models.CharField(max_length=255)

    class Meta:
        db_table = 'cache_job'
        ordering = ('-date_attempted',)


class Document(models.Model):
    # (D)

    docfile = models.FileField(upload_to='documents/%Y/%m/%d', null=True)
    file_type = models.CharField(max_length=10)
    doc_title = models.TextField(unique=True)
    file_header = JSONField(null=True)
    created_by = models.ForeignKey(User, null=True)
    guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'source_doc'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        super(Document, self).save(*args, **kwargs)

    ###############################
    ###### TRANSFORM UPLOAD #######
    ###############################

    def transform_upload(self):
        self.build_csv_df()
        self.process_file()
        self.upsert_source_object_map()

    def build_csv_df(self):

        self.location_column, self.campaign_column, self.uq_id_column = \
            ['geocode', 'campaign', 'unique_key']

        self.date_column = 'data_date'

        raw_csv_df = read_csv(settings.MEDIA_ROOT + str(self.docfile))

        csv_df = raw_csv_df.where((notnull(raw_csv_df)), None)
        # if there is no uq id column -- make one #
        if self.uq_id_column not in raw_csv_df.columns:

            try:
                csv_df[self.uq_id_column] = csv_df[self.location_column].map(
                    str) + csv_df[self.campaign_column]
            except Exception as err: ## FIXME # clean this
                if self.date_column not in csv_df.columns:
                    error_message = '%s is a required column.' % err.message
                    raise Exception(error_message)

        self.csv_df = csv_df
        self.file_header = csv_df.columns

        self.meta_lookup = {
            'location': {},
            'indicator': {},
            'campaign': {}
        }
        self.indicator_ids_to_exclude = set([-1])
        self.existing_submission_keys = SourceSubmission.objects.filter(
            document_id=self.id).values_list('instance_guid', flat=True)

    def process_file(self):
        '''
        Takes a file and dumps the data into the source submission table.
        Returns a list of source_submission_ids
        '''

        # transform the raw data based on the documents configurations #
        # doc_df = self.apply_doc_config_to_csv_df(self.csv_df)
        # doc_df = self.process_date_column(doc_df)

        # doc_obj = Document.objects.get(id=self.document.id)
        # doc_obj.file_header = list(doc_df.columns.values)
        # doc_obj.save()

        batch = {}

        for submission in self.csv_df.itertuples():

            ss, instance_guid = self.process_raw_source_submission(submission)

            if ss is not None and instance_guid is not None:
                ss['instance_guid'] = instance_guid
                batch[instance_guid] = ss

        object_list = [SourceSubmission(**v) for k, v in batch.iteritems()]
        ss = SourceSubmission.objects.bulk_create(object_list)
        return [x.id for x in ss]

    def upsert_source_object_map(self):
        '''
        TODO: save the source_strings so i dont have to iterate through
        the source_submission json.
        endpoint: api/v2/doc_mapping/?document=66
        '''

        if DocumentSourceObjectMap.objects\
            .filter(document_id=self.id):

            return

        source_dp_json = SourceSubmission.objects.filter(
            document_id=self.id).values_list('submission_json')

        if len(source_dp_json) == 0:
            return

        all_codes = [('indicator', k)
                     for k, v in json.loads(source_dp_json[0][0]).iteritems()]
        rg_codes, cp_codes = [], []

        for row in source_dp_json:
            row_dict = json.loads(row[0])
            rg_codes.append(row_dict[self.location_column])
            if self.campaign_column and self.campaign_column in row_dict:
                cp_codes.append(row_dict[self.campaign_column])

        for r in list(set(rg_codes)):
            all_codes.append(('location', r))

        for c in list(set(cp_codes)):
            all_codes.append(('campaign', c))

        doc_som_df = DataFrame(all_codes, columns=[
                               'content_type', 'source_object_code'])

        som_columns = ['id', 'source_object_code', 'master_object_id',
                       'content_type']

        existing_som_df = DataFrame(list(SourceObjectMap.objects.all()
                                         .values_list(*som_columns)), columns=som_columns)

        merged_df = doc_som_df.merge(existing_som_df, on=['content_type',
                                                          'source_object_code'], how='left')

        to_insert_df = merged_df[merged_df.isnull().any(axis=1)]

        to_insert_dict = to_insert_df.transpose().to_dict()

        to_insert_batch = [SourceObjectMap(** {
            'source_object_code': data['source_object_code'],
            'master_object_id': -1,
            'content_type': data['content_type']
        }) for ix, data in to_insert_dict.iteritems()]

        batch_result = SourceObjectMap.objects.bulk_create(to_insert_batch)

        all_som_df = DataFrame(list(SourceObjectMap.objects.all()
                                    .values_list(*som_columns)), columns=som_columns)

        # TODO some exception if number of rows not equal to rows in submission
        # #
        post_insert_som_df = doc_som_df.merge(all_som_df, on=['content_type',
                                                              'source_object_code'], how='inner')

        som_ids_for_doc = list(post_insert_som_df['id'].unique())

        dsom_to_insert = [DocumentSourceObjectMap(** {
            'document_id': self.id,
            'source_object_map_id': som_id,
        }) for som_id in som_ids_for_doc]

        dsom_batch_result = DocumentSourceObjectMap.objects.bulk_create(
            dsom_to_insert)


    def process_raw_source_submission(self, submission):

        submission_ix, submission_data = submission[0], submission[1:]

        submission_data = dict(zip(self.file_header, submission_data))
        instance_guid = submission_data[self.uq_id_column]

        if instance_guid == '' or instance_guid in self.existing_submission_keys:
            return None, None

        submission_dict = {
            'submission_json': submission_data,
            'document_id': self.id,
            'row_number': submission_ix,
            'location_code': submission_data[self.location_column],
            'instance_guid': submission_data[self.uq_id_column],
            'process_status': 'TO_PROCESS',
        }

        if self.file_type == 'date':
            submission_dict['data_date'] =\
                parse(submission_data[self.date_column])
        else:
            submission_dict['campaign_code'] =\
                submission_data[self.campaign_column]

        return submission_dict, instance_guid


    #############################
    ###### REFRESH MASTER #######
    #############################

    def refresh_master(self):

        self.db_doc_deets = self.get_document_config()

        self.refresh_submission_details()
        self.submissions_to_doc_datapoints()
        self.delete_unmapped()
        self.sync_datapoint()

    def get_document_config(self):
        '''
        When ingesting a file the user must set the following configurtions:
            - unique_id_column
            - location_code_column
            - data_date
        The user can in addition add a number of optional configurations in order to both
        set up ingestion ( ex. odk_form_name, odk_host ) as well as enhance reporting
        of the data ( photo_column, uploaded_by_column, lat_column, lon_column )
        When the MasterRefresh object is intialized this method is called which queries
        the table containing these configurations and makes it available for use within
        this module.
        '''

        detail_types, document_details = {}, {}
        ddt_qs = DocDetailType.objects.all().values()

        for row in ddt_qs:
            detail_types[row['id']] = row['name']

        dd_qs = DocumentDetail.objects\
            .filter(document_id=self.id)\
            .values()

        for row in dd_qs:
            document_details[detail_types[row['doc_detail_type_id']]] =\
                row['doc_detail_value']

        return document_details

    def get_document_meta_mappings(self):
        '''
        Depending on the configuration of the required location and campagin column,
        query the source object map table and find the equivelant master_object_id_ids
        needed to go through the remainder of the ETL process.
        '''

        # during the DocTransform process we associate new AND existing mappings between
        # the metadata assoicated with this doucment.

        # sm_ids = DocumentSourceObjectMap.objects.filter(document_id =\
        #     self.document_id).values_list('source_object_map_id',flat=True)

        # create a tuple dict ex: {('location': "PAK") : 3 , ('location':
        # "PAK") : 3}
        source_map_dict = DataFrame(list(SourceObjectMap.objects
                         .filter(
                             master_object_id__gt=0)\
                         # id__in = sm_ids)\
                         .values_list(*['master_object_id']))
                    , columns=['master_object_id']\
                    , index=SourceObjectMap.objects.filter(master_object_id__gt=0)
                    # ,id__in = sm_ids)\
                    .values_list(*['content_type', 'source_object_code']))\


        source_map_dict = source_map_dict.to_dict()['master_object_id']

        return source_map_dict


    def delete_unmapped(self):
        '''
        if a user re-maps data, we need to delete the
        old data and make way for the new
        '''

        som_data = SourceObjectMap.objects.filter(master_object_id__gt=0,
              id__in=DocumentSourceObjectMap.objects
              .filter(document_id=self.id)
              .values_list('source_object_map_id', flat=True))\
              .values_list('content_type', 'master_object_id')

        som_lookup = defaultdict(list)

        for content_type, master_object_id in som_data:
            som_lookup[content_type].append(master_object_id)

        ## delete bad_indicator_data ##
        DataPoint.objects.filter(
            source_submission_id__document_id=self.id,
        ).exclude(indicator_id__in=som_lookup['indicator']).delete()

        ## delete bad_location_data ##
        DataPoint.objects.filter(
            source_submission_id__document_id=self.id,
        ).exclude(location_id__in=som_lookup['location']).delete()

        ## delete bad_campaign_data ##
        DataPoint.objects.filter(
            source_submission_id__document_id=self.id,
        ).exclude(location_id__in=som_lookup['campaign']).delete()

    def refresh_submission_details(self):
        '''
        Based on new and existing mappings, upsert the cooresponding master_object_id_ids
        and determine which rows are ready to process.. since we need a master_location
        and a master_campaign in order to have a successful submission this method helps
        us filter the data that we need to process.
        Would like to be more careful here about what i delete as most things wont be
        touched when it comes to this re-processing, and thus the delete and re-insert
        will be for not.. however the benefit is that it's a clean upsert.. dont have to
        worry about old data that should have been blown away hanging around.
        '''

        ss_id_list_to_process, all_ss_ids = [], []

        # find soure_submission_ids based of location_codes to process
        # then get the json of all of the related submissions .
        submission_qs = SourceSubmission.objects\
            .filter(document_id=self.id)

        for submission in submission_qs:
            all_ss_ids.append(submission.id)

            location_id = submission.get_location_id()
            campaign_id = submission.get_campaign_id()

            if location_id > 0:
                ss_id_list_to_process.append(submission.id)
                submission.location_id = location_id
                submission.campaign_id = campaign_id

        if len(submission_qs) > 0:
            bulk_update(submission_qs)

        return ss_id_list_to_process, all_ss_ids

    def submissions_to_doc_datapoints(self):
        '''
        Send all rows queued for processing to the process_source_submission method.
        '''

        self.source_map_dict = self.get_document_meta_mappings()

        # ss_ids_in_batch = self.submission_data.keys()

        for row in SourceSubmission.objects.filter(document_id=self.id):

            row.location_id = row.get_location_id()
            row.campaign_id = row.get_campaign_id()

            # if no mapping for campaign / location -- dont process
            if (not row.campaign_id or row.campaign_id == -1) and not row.data_date:
                row.process_status = 'missing campaign or data_date'
            elif not row.location_id or row.location_id == -1:
                row.process_status = 'missing location'
            else:
                doc_dps = self.process_source_submission(row)

    def add_unique_index(self, x):
        if x['campaign_id'] and not math.isnan(x['campaign_id']):
            x['unique_index'] = str(
                x['location_id']) + '_' + str(x['indicator_id']) + '_' + str(int(x['campaign_id']))
        else:
            x['unique_index'] = str(x['location_id']) + '_' + str(
                x['indicator_id']) + '_' + str(to_datetime(x['data_date'], utc=True))
        return x

    def filter_data_frame_conflicts(self, df):
        '''
        These are CONFLICTS and should be returned to the user.  For now,
        we simply take the datapoint with the max soruce_submission_id
        when there are two datapoints in one document for which exist the same
        location, indicator, campaign combo.
        '''

        filtered_df = df.sort(['source_submission_id'], ascending=False)\
            .groupby('unique_index').first().reset_index()

        return filtered_df

    def sync_datapoint(self, ss_id_list=None):

        # ./manage.py test rhizome.tests.test_refresh_master.RefreshMasterTestCase.test_latest_data_gets_synced --settings=rhizome.settings.test
        dp_batch = []
        if not ss_id_list:
            ss_id_list = SourceSubmission.objects\
                .filter(document_id=self.id).values_list('id', flat=True)

        doc_dp_df = DataFrame(list(DocDataPoint.objects.filter(
            document_id=self.id).values()))

        if len(doc_dp_df) == 0:
            return

        doc_dp_df = doc_dp_df.apply(self.add_unique_index, axis=1)
        doc_dp_df = self.filter_data_frame_conflicts(doc_dp_df)

        doc_dp_unique_keys = doc_dp_df['unique_index'].unique()

        dp_ids_to_delete = DataPoint\
            .objects.filter(unique_index__in=doc_dp_unique_keys)\
            .values_list('id', flat=True)

        for ix, row in doc_dp_df.iterrows():
            dp_batch.append(DataPoint(**{
                'indicator_id': row.indicator_id,
                'location_id': row.location_id,
                'campaign_id': row.campaign_id,
                'data_date': row.data_date,
                'value': row.value,
                'unique_index': row.unique_index,
                'source_submission_id': row.source_submission_id,
            }))

        DataPoint.objects.filter(id__in=dp_ids_to_delete).delete()
        DataPoint.objects.bulk_create(dp_batch)

    def process_source_submission(self, row):
        doc_dp_batch = []
        submission = row.submission_json

        for k, v in submission.iteritems():
            doc_dp = self.source_submission_cell_to_doc_datapoint(row, k, v,
                                                                  row.data_date)
            if doc_dp:
                doc_dp_batch.append(doc_dp)
        DocDataPoint.objects.filter(source_submission_id=row.id).delete()
        DocDataPoint.objects.bulk_create(doc_dp_batch)

    # helper function to sync_datapoints
    def add_unique_index(self, x):
        if x['campaign_id'] and not math.isnan(x['campaign_id']):
            x['unique_index'] = str(
                x['location_id']) + '_' + str(x['indicator_id']) + '_' + str(x['campaign_id'])
        else:
            x['unique_index'] = str(x['location_id']) + '_' + str(
                x['indicator_id']) + '_' + str(to_datetime(x['data_date'], utc=True))
        return x

    def source_submission_cell_to_doc_datapoint(self, row, indicator_string,
                                                value, data_date):
        '''
        This method prepares a batch insert into docdatapoint by creating a list of
        docdatapoint objects.  The Database handles all docdatapoitns in a submission
        row at once in process_source_submission.
        '''

        ## if no indicator row dont process ##
        try:
            indicator_id = self.source_map_dict[
                ('indicator', indicator_string)]
        except KeyError:
            return None

        cleaned_val = None

        try:
            cleaned_val = self.clean_val(value)
        except ValueError:
            return None

        if not cleaned_val == None: #FIXME sloppy syntax
            doc_dp = DocDataPoint(**{
                'indicator_id':  indicator_id,
                'value': cleaned_val,
                'location_id': row.location_id,
                'campaign_id': row.campaign_id,
                'data_date': data_date,
                'document_id': self.id,
                'source_submission_id': row.id,
                'agg_on_location': True,
            })
            return doc_dp
        else:
            return None

    def clean_val(self, val):
        '''
        This needs alot of work but basically determines if a particular submission
        cell is alllowed.
        '''
        str_lookup = {'yes': 1, 'no': 0}
        if val is None:
            return None

        # deal with percentages
        convert_percent = False
        if type(val) == unicode and '%' in val:
            try:
                val = float(re.sub('%', '', val))
                convert_percent = True
            except ValueError:
                pass
        ## clean!  i am on a deadline rn :-/  ##

        try:
            cleaned_val = locale.atoi(val)  # 100,000 -> 100000.oo
        except AttributeError:
            cleaned_val = float(val)
        except ValueError:
            try:
                cleaned_val = float(val)
            except ValueError:
                try:
                    cleaned_val = str_lookup[val.lower()]
                except KeyError:
                    raise ValueError('Bad Value!')

        if convert_percent:
            cleaned_val = cleaned_val / 100.0
        return cleaned_val

class SourceObjectMap(models.Model):
    # FIXME -> need to check what would be foreign keys
    # so region_maps / campaign_maps are valid

    master_object_id = models.IntegerField()  # need to think about to FK this.
    master_object_name = models.CharField(max_length=255, null=True)
    source_object_code = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20)
    mapped_by = models.ForeignKey(User, null=True)
    # mapped_by is only null so that i can initialize the database with #
    # mappings without a user_id created #

    class Meta:
        db_table = 'source_object_map'
        unique_together = (('content_type', 'source_object_code'))

    def save(self, **kwargs):

        if self.master_object_id == -1:
            return super(SourceObjectMap, self).save(**kwargs)


        if self.content_type == 'indicator':
            self.master_object_name = Indicator.objects\
                .get(id=self.master_object_id).short_name

        if self.content_type == 'location':
            self.master_object_name = Location.objects\
                .get(id=self.master_object_id).name

        if self.content_type == 'campaign':
            self.master_object_name = Campaign.objects\
                .get(id=self.master_object_id).name

        return super(SourceObjectMap, self).save(**kwargs)

class DocumentSourceObjectMap(models.Model):

    document = models.ForeignKey(Document)
    source_object_map = models.ForeignKey(SourceObjectMap)

    class Meta:

        unique_together = (('document', 'source_object_map'))
        db_table = 'doc_object_map'


class DocDetailType(models.Model):
    '''
    '''
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'doc_detail_type'

class DocumentDetail(models.Model):
    '''
    '''

    document = models.ForeignKey(Document)
    doc_detail_type = models.ForeignKey(DocDetailType)
    doc_detail_value = models.CharField(max_length=255)

    class Meta:
        db_table = 'doc_detail'
        unique_together = (('document', 'doc_detail_type'))

class SourceSubmission(models.Model):

    document = models.ForeignKey(Document)
    instance_guid = models.CharField(max_length=255)
    row_number = models.IntegerField()
    data_date = models.DateTimeField(null=True)
    location_code = models.CharField(max_length=1000)
    campaign_code = models.CharField(max_length=1000)
    location_display = models.CharField(max_length=1000)
    submission_json = JSONField()
    created_at = models.DateTimeField(auto_now=True)
    process_status = models.CharField(max_length=25)  # should be a FK

    class Meta:
        db_table = 'source_submission'
        unique_together = (('document', 'instance_guid'))

    def get_location_id(self):

        try:
            l_id = SourceObjectMap.objects.get(content_type='location',
                   source_object_code=self.location_code).master_object_id
        except SourceObjectMap.DoesNotExist :
            l_id = None

        return l_id

    def get_campaign_id(self):

        try:
            c_id = SourceObjectMap.objects.get(content_type='campaign',
                                               source_object_code=self.campaign_code).master_object_id
        except SourceObjectMap.DoesNotExist:
            c_id = None

        return c_id


class DocDataPoint(models.Model):
    '''
    For Validation of upload rhizome.
    '''

    document = models.ForeignKey(Document)  # redundant
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign, null=True)
    data_date = models.DateTimeField(null=True)
    value = models.FloatField(null=True)
    source_submission = models.ForeignKey(SourceSubmission)
    agg_on_location = models.BooleanField()

    class Meta:
        db_table = 'doc_datapoint'


class DataPoint(models.Model):
    '''
    The core table of the application.  This is where the raw data is stored
    and brought together from data entry, ODK and csv upload.

    Note that this table does not store the aggregated or calculated data, only
    the raw data that we get from the source.

    The source_submission shows the original source of the data in the
    source_submission.  The source_submission is -1 in the case of data
    entry.

    The cache_job_id column allows us to find out when and why a particular
    datapoint was refreshed.  New datapoints have a cache_job_id = -1 which
    tells the system that it needs to be refreshed.
    '''

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign, null=True)
    data_date = models.DateTimeField(null=True)
    value = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    source_submission = models.ForeignKey(SourceSubmission)
    cache_job = models.ForeignKey(CacheJob, default=-1)
    unique_index = models.CharField(max_length=255, unique=True, default=-1)

    def get_val(self):
        return self.value

    class Meta:
        db_table = 'datapoint'


# Exceptions #
class BadFileHeaderException(Exception):
    '''
    If a user uploads a file, and one of the column headers has a comma in it
    it makes it impossible for us to parse the data.  So when we find out that
    the length of header.split(',') is greater than first_line.split(',')
    we throw this exception
    '''
    defaultMessage = "Your Header Has Commas in it, please fix and re-upload"
    defaultCode = -2
