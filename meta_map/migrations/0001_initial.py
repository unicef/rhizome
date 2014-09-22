# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SourceRegion'
        db.create_table(u'meta_map_sourceregion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region_string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Source'])),
            ('source_guid', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'meta_map', ['SourceRegion'])

        # Adding model 'SourceIndicator'
        db.create_table(u'meta_map_sourceindicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indicator_string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Source'])),
            ('source_guid', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'meta_map', ['SourceIndicator'])

        # Adding model 'SourceCampaign'
        db.create_table(u'meta_map_sourcecampaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign_string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Source'])),
            ('source_guid', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'meta_map', ['SourceCampaign'])

        # Adding model 'RegionMap'
        db.create_table(u'meta_map_regionmap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('master_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Indicator'])),
            ('source_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meta_map.SourceIndicator'])),
            ('mapped_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'meta_map', ['RegionMap'])

        # Adding model 'IndicatorMap'
        db.create_table(u'meta_map_indicatormap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('master_indicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Indicator'])),
            ('source_indicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meta_map.SourceIndicator'])),
            ('mapped_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'meta_map', ['IndicatorMap'])

        # Adding model 'CampaignMap'
        db.create_table(u'meta_map_campaignmap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('master_campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Indicator'])),
            ('source_campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meta_map.SourceIndicator'])),
            ('mapped_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'meta_map', ['CampaignMap'])


    def backwards(self, orm):
        # Deleting model 'SourceRegion'
        db.delete_table(u'meta_map_sourceregion')

        # Deleting model 'SourceIndicator'
        db.delete_table(u'meta_map_sourceindicator')

        # Deleting model 'SourceCampaign'
        db.delete_table(u'meta_map_sourcecampaign')

        # Deleting model 'RegionMap'
        db.delete_table(u'meta_map_regionmap')

        # Deleting model 'IndicatorMap'
        db.delete_table(u'meta_map_indicatormap')

        # Deleting model 'CampaignMap'
        db.delete_table(u'meta_map_campaignmap')


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
        u'datapoints.indicator': {
            'Meta': {'object_name': 'Indicator', 'db_table': "'indicator'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reported': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '55', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'datapoints.source': {
            'Meta': {'object_name': 'Source', 'db_table': "'source'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'source_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        u'meta_map.campaignmap': {
            'Meta': {'object_name': 'CampaignMap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapped_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'master_campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'source_campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meta_map.SourceIndicator']"})
        },
        u'meta_map.indicatormap': {
            'Meta': {'object_name': 'IndicatorMap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapped_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'master_indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'source_indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meta_map.SourceIndicator']"})
        },
        u'meta_map.regionmap': {
            'Meta': {'object_name': 'RegionMap'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapped_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'master_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'source_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meta_map.SourceIndicator']"})
        },
        u'meta_map.sourcecampaign': {
            'Meta': {'object_name': 'SourceCampaign'},
            'campaign_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'meta_map.sourceindicator': {
            'Meta': {'object_name': 'SourceIndicator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'meta_map.sourceregion': {
            'Meta': {'object_name': 'SourceRegion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Source']"}),
            'source_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['meta_map']