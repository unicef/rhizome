import hashlib
import random
import json

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from pandas import read_csv
from pandas import notnull
from pandas import DataFrame

from jsonfield import JSONField

from rhizome.models.location_models import Location
from rhizome.models.campaign_models import Campaign
from rhizome.models.indicator_models import Indicator


class Document(models.Model):
    # ./manage.py test rhizome.tests.test_api_doc_transform.DocTransformResourceTest.test_doc_transform --settings=rhizome.settings.test

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
            except Exception as err:
                if self.date_column not in csv_df.columns:
                    dp_error_message = '%s is a required column.' % err.message
                    raise RhizomeApiException(message=dp_error_message)

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
            'campaign_code': submission_data[self.campaign_column],
            # 'data_date': submission_data['data_date'],
            'instance_guid': submission_data[self.uq_id_column],
            'process_status': 'TO_PROCESS',
        }
        return submission_dict, instance_guid

    def refresh_master(self):
        pass


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
        except ObjectDoesNotExist:
            l_id = None

        return l_id

    def get_campaign_id(self):

        try:
            c_id = SourceObjectMap.objects.get(content_type='campaign',
                                               source_object_code=self.campaign_code).master_object_id
        except ObjectDoesNotExist:
            c_id = None

        return c_id

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
