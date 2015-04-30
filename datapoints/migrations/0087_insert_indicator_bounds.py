# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute('''

        TRUNCATE TABLE indicator_bound;

        /*
        INSERT INTO indicator_bound
        (indicator_id,mn_val,mx_val,bound_name,direction)


        SELECT 168,NULL,-1,'invalid', 1 UNION ALL
        SELECT 168,-1,0,'good', 1 UNION ALL
        SELECT 168,0,NULL,'bad', 1 UNION ALL
        SELECT 431,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 431,0.0,0.05,'good', 1 UNION ALL
        SELECT 431,0.05,0.09,'okay', 1 UNION ALL
        SELECT 431,0.09,1,'bad', 1 UNION ALL
        SELECT 431,1,NULL,'invalid', 1 UNION ALL
        SELECT 432,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 432,0.0,0.05,'good', 1 UNION ALL
        SELECT 432,0.05,0.09,'okay', 1 UNION ALL
        SELECT 432,0.09,1,'bad', 1 UNION ALL
        SELECT 432,1,NULL,'invalid', 1 UNION ALL
        SELECT 169,1,NULL,'invalid', 1 UNION ALL
        SELECT 169,0.9,1,'good', 1 UNION ALL
        SELECT 169,0.75,0.89,'okay', 1 UNION ALL
        SELECT 169,0.0,0.75,'bad', 1 UNION ALL
        SELECT 169,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 233,1,NULL,'invalid', 1 UNION ALL
        SELECT 233,0.9,1,'good', 1 UNION ALL
        SELECT 233,0.75,0.89,'okay', 1 UNION ALL
        SELECT 233,0.0,0.75,'bad', 1 UNION ALL
        SELECT 233,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 172,1,NULL,'invalid', 1 UNION ALL
        SELECT 172,0.79,1,'good', 1 UNION ALL
        SELECT 172,0.49,0.79,'okay', 1 UNION ALL
        SELECT 172,0.0,0.49,'bad', 1 UNION ALL
        SELECT 172,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 219,1,NULL,'invalid', 1 UNION ALL
        SELECT 219,0.1,0.15,'okay', 1 UNION ALL
        SELECT 219,0.05,0.1,'good', 1 UNION ALL
        SELECT 219,0,0.05,'okay', 1 UNION ALL
        SELECT 219,-1,0,'bad', 1 UNION ALL
        SELECT 219,NULL,-1,'invalid', 1 UNION ALL
        SELECT 174,1,NULL,'invalid', 1 UNION ALL
        SELECT 174,0.95,1,'good', 1 UNION ALL
        SELECT 174,0.85,0.95,'okay', 1 UNION ALL
        SELECT 174,0.0,0.85,'bad', 1 UNION ALL
        SELECT 174,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 178,1,NULL,'invalid', 1 UNION ALL
        SELECT 178,0.75,1,'good', 1 UNION ALL
        SELECT 178,0.5,0.75,'okay', 1 UNION ALL
        SELECT 178,0.0,0.5,'bad', 1 UNION ALL
        SELECT 178,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 179,1,NULL,'invalid', 1 UNION ALL
        SELECT 179,0.9,1,'good', 1 UNION ALL
        SELECT 179,0.75,0.89,'okay', 1 UNION ALL
        SELECT 179,0.0,0.75,'bad', 1 UNION ALL
        SELECT 179,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 180,1,NULL,'invalid', 1 UNION ALL
        SELECT 180,0.9,1,'good', 1 UNION ALL
        SELECT 180,0.75,0.89,'okay', 1 UNION ALL
        SELECT 180,0.0,0.75,'bad', 1 UNION ALL
        SELECT 180,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 230,1,NULL,'invalid', 1 UNION ALL
        SELECT 230,0.9,1,'good', 1 UNION ALL
        SELECT 230,0.75,0.89,'okay', 1 UNION ALL
        SELECT 230,0.0,0.75,'bad', 1 UNION ALL
        SELECT 230,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 239,1,NULL,'invalid', 1 UNION ALL
        SELECT 239,0.75,1,'good', 1 UNION ALL
        SELECT 239,0.5,0.75,'okay', 1 UNION ALL
        SELECT 239,0.0,0.5,'bad', 1 UNION ALL
        SELECT 239,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 228,1,NULL,'invalid', 1 UNION ALL
        SELECT 228,0.9,1,'good', 1 UNION ALL
        SELECT 228,0.75,0.89,'okay', 1 UNION ALL
        SELECT 228,0.0,0.75,'bad', 1 UNION ALL
        SELECT 228,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 184,1,NULL,'invalid', 1 UNION ALL
        SELECT 184,0.9,1,'good', 1 UNION ALL
        SELECT 184,0.75,0.89,'okay', 1 UNION ALL
        SELECT 184,0.0,0.75,'bad', 1 UNION ALL
        SELECT 184,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 185,1,NULL,'invalid', 1 UNION ALL
        SELECT 185,0.9,1,'good', 1 UNION ALL
        SELECT 185,0.75,0.89,'okay', 1 UNION ALL
        SELECT 185,0.0,0.75,'bad', 1 UNION ALL
        SELECT 185,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 226,1,NULL,'invalid', 1 UNION ALL
        SELECT 226,0.9,1,'good', 1 UNION ALL
        SELECT 226,0.75,0.89,'okay', 1 UNION ALL
        SELECT 226,0.0,0.75,'bad', 1 UNION ALL
        SELECT 226,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 222,1,NULL,'invalid', 1 UNION ALL
        SELECT 222,0.9,1,'good', 1 UNION ALL
        SELECT 222,0.75,0.9,'okay', 1 UNION ALL
        SELECT 222,0.0,0.75,'bad', 1 UNION ALL
        SELECT 222,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 166,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 166,0.0,0.0049,'good', 1 UNION ALL
        SELECT 166,0.0049,0.01,'okay', 1 UNION ALL
        SELECT 166,0.01,1,'bad', 1 UNION ALL
        SELECT 166,1,NULL,'invalid', 1 UNION ALL
        SELECT 187,1,NULL,'invalid', 1 UNION ALL
        SELECT 187,0.9,1,'good', 1 UNION ALL
        SELECT 187,0.74,0.9,'okay', 1 UNION ALL
        SELECT 187,0.0,0.74,'bad', 1 UNION ALL
        SELECT 187,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 164,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 164,0.0,0.009,'good', 1 UNION ALL
        SELECT 164,0.009,0.02,'okay', 1 UNION ALL
        SELECT 164,0.02,1,'bad', 1 UNION ALL
        SELECT 164,1,NULL,'invalid', 1 UNION ALL
        SELECT 189,1,NULL,'invalid', 1 UNION ALL
        SELECT 189,0.8,1,'good', 1 UNION ALL
        SELECT 189,0.59,0.8,'okay', 1 UNION ALL
        SELECT 189,0.0,0.59,'bad', 1 UNION ALL
        SELECT 189,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 245,1,NULL,'invalid', 1 UNION ALL
        SELECT 245,0.79,1,'good', 1 UNION ALL
        SELECT 245,0.6,0.79,'okay', 1 UNION ALL
        SELECT 245,0.0,0.6,'bad', 1 UNION ALL
        SELECT 245,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 236,1,NULL,'invalid', 1 UNION ALL
        SELECT 236,0.79,1,'good', 1 UNION ALL
        SELECT 236,0.6,0.79,'okay', 1 UNION ALL
        SELECT 236,0.0,0.6,'bad', 1 UNION ALL
        SELECT 236,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 191,NULL,0.0,'invalid', 1 UNION ALL
        SELECT 191,0.0,0.75,'good', 1 UNION ALL
        SELECT 191,0.75,0.89,'okay', 1 UNION ALL
        SELECT 191,0.89,1,'bad', 1 UNION ALL
        SELECT 191,1,NULL,'invalid', 1 UNION ALL
        SELECT 193,1,NULL,'invalid', 1 UNION ALL
        SELECT 193,0.79,1,'good', 1 UNION ALL
        SELECT 193,0.6,0.79,'okay', 1 UNION ALL
        SELECT 193,0.0,0.6,'bad', 1 UNION ALL
        SELECT 193,NULL,0.0,'invalid', 1;

        */

        ''')


    def backwards(self, orm):
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
        u'datapoints.aggdatapoint': {
            'Meta': {'unique_together': "(('region_id', 'campaign_id', 'indicator_id'),)", 'object_name': 'AggDataPoint', 'db_table': "'agg_datapoint'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.baddata': {
            'Meta': {'object_name': 'BadData', 'db_table': "'bad_data'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.CacheJob']"}),
            'datapoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.DataPoint']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            'error_type': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datapoints.cachejob': {
            'Meta': {'ordering': "('-date_attempted',)", 'object_name': 'CacheJob', 'db_table': "'cache_job'"},
            'date_attempted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 20, 0, 0)'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {}),
            'response_msg': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.calculatedindicatorcomponent': {
            'Meta': {'object_name': 'CalculatedIndicatorComponent', 'db_table': "'calculated_indicator_component'"},
            'calculation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicator_master'", 'to': u"orm['datapoints.Indicator']"}),
            'indicator_component': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicator_component'", 'to': u"orm['datapoints.Indicator']"})
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
        u'datapoints.datapoint': {
            'Meta': {'ordering': "['region', 'campaign']", 'unique_together': "(('indicator', 'region', 'campaign'),)", 'object_name': 'DataPoint', 'db_table': "'datapoint'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'source_datapoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.SourceDataPoint']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.datapointabstracted': {
            'Meta': {'unique_together': "(('region', 'campaign'),)", 'object_name': 'DataPointAbstracted', 'db_table': "'datapoint_abstracted'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_json': ('jsonfield.fields.JSONField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"})
        },
        u'datapoints.datapointcomputed': {
            'Meta': {'unique_together': "(('region_id', 'campaign_id', 'indicator_id'),)", 'object_name': 'DataPointComputed', 'db_table': "'datapoint_with_computed'"},
            'cache_job': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['datapoints.CacheJob']"}),
            'campaign_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.expecteddata': {
            'Meta': {'unique_together': "(('region', 'campaign'),)", 'object_name': 'ExpectedData', 'db_table': "'expected_data'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ex_parent_region'", 'to': u"orm['datapoints.Region']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ex_child_region'", 'to': u"orm['datapoints.Region']"})
        },
        u'datapoints.historicaldatapointentry': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalDataPointEntry'},
            'cache_job_id': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'campaign_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'indicator_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'source_datapoint_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
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
        u'datapoints.indicatorbound': {
            'Meta': {'object_name': 'IndicatorBound', 'db_table': "'indicator_bound'"},
            'bound_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'direction': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'mn_val': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'mx_val': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'datapoints.missingmapping': {
            'Meta': {'object_name': 'MissingMapping', 'db_table': "'vw_missing_mappings'", 'managed': 'False'},
            'datapoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.DataPoint']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.SourceDataPoint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'what_is_missing': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.office': {
            'Meta': {'object_name': 'Office', 'db_table': "'office'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.recondata': {
            'Meta': {'unique_together': "(('region', 'campaign', 'indicator'),)", 'object_name': 'ReconData', 'db_table': "'recon_data'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'is_raw': ('django.db.models.fields.BooleanField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'success_flag': ('django.db.models.fields.BooleanField', [], {}),
            'target_value': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.region': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'region_type', 'office'),)", 'object_name': 'Region', 'db_table': "'region'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_high_risk': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']", 'null': 'True'}),
            'region_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'region_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.RegionType']"}),
            'shape_file_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'unique_with': '()'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"})
        },
        u'datapoints.regionheirarchy': {
            'Meta': {'object_name': 'RegionHeirarchy', 'db_table': "'region_heirarchy_cache'", 'managed': 'False'},
            'contained_by_region_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_type_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'datapoints.regionpolygon': {
            'Meta': {'object_name': 'RegionPolygon', 'db_table': "'region_polygon'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polygon': ('jsonfield.fields.JSONField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']", 'unique': 'True'}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_len': ('django.db.models.fields.FloatField', [], {})
        },
        u'datapoints.regiontype': {
            'Meta': {'object_name': 'RegionType', 'db_table': "'region_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        u'datapoints.responsibility': {
            'Meta': {'ordering': "('indicator',)", 'unique_together': "(('user', 'indicator', 'region'),)", 'object_name': 'Responsibility', 'db_table': "'responsibility'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'datapoints.source': {
            'Meta': {'object_name': 'Source', 'db_table': "'source'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
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
        'source_data.processstatus': {
            'Meta': {'object_name': 'ProcessStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status_text': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'source_data.sourcedatapoint': {
            'Meta': {'unique_together': "(('source', 'source_guid', 'indicator_string'),)", 'object_name': 'SourceDataPoint', 'db_table': "'source_datapoint'"},
            'campaign_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cell_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 20, 0, 0)'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['source_data.Document']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'row_number': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"})
        }
    }

    complete_apps = ['datapoints']
