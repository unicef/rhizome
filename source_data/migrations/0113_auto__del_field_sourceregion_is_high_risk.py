# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SourceRegion.is_high_risk'
        db.execute('''
        ALTER TABLE source_region
        DROP COLUMN is_high_risk;
        ''')


    def backwards(self, orm):
        # Adding field 'SourceRegion.is_high_risk'
        pass

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'datapoints.campaign': {
            'Meta': {'ordering': "('-start_date',)", 'unique_together': "(('office', 'start_date'),)", 'object_name': 'Campaign', 'db_table': "'campaign'"},
            'campaign_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.CampaignType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'get_full_name'", 'unique_with': '()'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'datapoints.campaigntype': {
            'Meta': {'object_name': 'CampaignType', 'db_table': "'campaign_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.indicator': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Indicator', 'db_table': "'indicator'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reported': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'unique_with': '()'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"})
        },
        u'datapoints.office': {
            'Meta': {'object_name': 'Office', 'db_table': "'office'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.region': {
            'Meta': {'unique_together': "(('name', 'region_type', 'office'),)", 'object_name': 'Region', 'db_table': "'region'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']", 'null': 'True'}),
            'region_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'region_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.RegionType']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'unique_with': '()'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"})
        },
        u'datapoints.regiontype': {
            'Meta': {'object_name': 'RegionType', 'db_table': "'region_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        u'datapoints.source': {
            'Meta': {'object_name': 'Source', 'db_table': "'source'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        u'source_data.campaignmap': {
            'Meta': {'object_name': 'CampaignMap', 'db_table': "'campaign_map'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapped_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'master_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            'source_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.SourceCampaign']", 'unique': 'True'})
        },
        u'source_data.document': {
            'Meta': {'ordering': "('-id',)", 'unique_together': "(('docfile', 'doc_text'),)", 'object_name': 'Document'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'doc_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'master_datapoint_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_datapoint_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'source_data.documentdetail': {
            'Meta': {'object_name': 'DocumentDetail', 'db_table': "'document_detail'"},
            'db_model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_id': ('django.db.models.fields.IntegerField', [], {}),
            'master_dp_count': ('django.db.models.fields.IntegerField', [], {}),
            'master_object_id': ('django.db.models.fields.IntegerField', [], {}),
            'source_dp_count': ('django.db.models.fields.IntegerField', [], {}),
            'source_object_id': ('django.db.models.fields.IntegerField', [], {}),
            'source_string': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'source_data.etljob': {
            'Meta': {'ordering': "('-date_attempted',)", 'object_name': 'EtlJob'},
            'cron_guid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_attempted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 5, 0, 0)'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'error_msg': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'success_msg': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'source_data.indicatormap': {
            'Meta': {'object_name': 'IndicatorMap', 'db_table': "'indicator_map'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapped_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'master_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'source_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.SourceIndicator']", 'unique': 'True'})
        },
        u'source_data.odkform': {
            'Meta': {'object_name': 'ODKForm', 'db_table': "'odk_form'"},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']", 'null': 'True'}),
            'form_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_processed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'master_datapoint_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'response_msg': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'source_datapoint_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'source_data.processstatus': {
            'Meta': {'object_name': 'ProcessStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status_text': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'source_data.regionmap': {
            'Meta': {'object_name': 'RegionMap', 'db_table': "'region_map'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapped_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'master_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'source_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.SourceRegion']", 'unique': 'True'})
        },
        u'source_data.sourcecampaign': {
            'Meta': {'object_name': 'SourceCampaign', 'db_table': "'source_campaign'"},
            'campaign_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.sourcedatapoint': {
            'Meta': {'unique_together': "(('source', 'source_guid', 'indicator_string'),)", 'object_name': 'SourceDataPoint', 'db_table': "'source_datapoint'"},
            'campaign_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cell_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 5, 0, 0)'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'row_number': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"})
        },
        u'source_data.sourceindicator': {
            'Meta': {'object_name': 'SourceIndicator', 'db_table': "'source_indicator'"},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'source_data.sourceregion': {
            'Meta': {'object_name': 'SourceRegion', 'db_table': "'source_region'"},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'lon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'parent_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'parent_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'region_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'region_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'source_data.sourceregionpolygon': {
            'Meta': {'object_name': 'SourceRegionPolygon', 'db_table': "'source_region_polygon'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polygon': ('django.db.models.fields.TextField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_len': ('django.db.models.fields.FloatField', [], {}),
            'source_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.SourceRegion']", 'unique': 'True'})
        },
        'source_data.vcmsettlement': {
            'Meta': {'object_name': 'VCMSettlement', 'db_table': "'odk_vcm_settlement'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 5, 0, 0)'}),
            'daterecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcmname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcmphone': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['source_data']
