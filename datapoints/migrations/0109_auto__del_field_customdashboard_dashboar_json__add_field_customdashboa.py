# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        pass


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
            'date_attempted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 11, 0, 0)'}),
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
        u'datapoints.columnattributes': {
            'Meta': {'object_name': 'ColumnAttributes', 'db_table': "'column_attributes'"},
            'column_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_on_table_flag': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.customdashboard': {
            'Meta': {'object_name': 'CustomDashboard', 'db_table': "'custom_dashboard'"},
            'dashboard_json': ('jsonfield.fields.JSONField', [], {}),
            'default_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'})
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
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'})
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
        u'datapoints.indicatorabstracted': {
            'Meta': {'object_name': 'IndicatorAbstracted', 'db_table': "'indicator_abstracted'"},
            'bound_json': ('jsonfield.fields.JSONField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tag_json': ('jsonfield.fields.JSONField', [], {})
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
        u'datapoints.indicatorpermission': {
            'Meta': {'unique_together': "(('group', 'indicator'),)", 'object_name': 'IndicatorPermission', 'db_table': "'indicator_permission'"},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"})
        },
        u'datapoints.indicatortag': {
            'Meta': {'object_name': 'IndicatorTag', 'db_table': "'indicator_tag'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.IndicatorTag']", 'null': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.indicatortotag': {
            'Meta': {'object_name': 'IndicatorToTag', 'db_table': "'indicator_to_tag'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'indicator_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.IndicatorTag']"})
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
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'target_value': ('django.db.models.fields.FloatField', [], {})
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
        u'datapoints.regionheirarchy': {
            'Meta': {'object_name': 'RegionHeirarchy', 'db_table': "'region_heirarchy_cache'", 'managed': 'False'},
            'contained_by_region_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_type_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'datapoints.regionpermission': {
            'Meta': {'unique_together': "(('user', 'region', 'read_write'),)", 'object_name': 'RegionPermission', 'db_table': "'region_permission'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_write': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        u'datapoints.userabstracted': {
            'Meta': {'object_name': 'UserAbstracted', 'db_table': "'user_abstracted'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_json': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_name': ('django.db.models.fields.BooleanField', [], {}),
            'region_permission_json': ('jsonfield.fields.JSONField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'datapoints.usergroup': {
            'Meta': {'object_name': 'UserGroup', 'db_table': "'auth_user_groups'", 'managed': 'False'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'source_data.document': {
            'Meta': {'ordering': "('-id',)", 'unique_together': "(('docfile', 'doc_text'),)", 'object_name': 'Document'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 11, 0, 0)'}),
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
            'cell_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 11, 0, 0)'}),
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
