# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Indicator'
        db.create_table('indicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=55)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_reported', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=55, populate_from='name', unique_with=())),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['Indicator'])

        # Adding model 'Office'
        db.create_table('office', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['Office'])

        # Adding model 'Region'
        db.create_table('region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=55)),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Office'])),
            ('shape_file_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=10, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=55, populate_from='full_name')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['Region'])

        # Adding model 'Campaign'
        db.create_table('campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Office'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='get_full_name')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['Campaign'])

        # Adding model 'HistoricalDataPoint'
        db.create_table(u'datapoints_historicaldatapoint', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('indicator_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('region_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('campaign_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')()),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'datapoints', ['HistoricalDataPoint'])

        # Adding model 'DataPoint'
        db.create_table('datapoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indicator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Indicator'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Region'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.Campaign'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['DataPoint'])

        # Adding unique constraint on 'DataPoint', fields ['indicator', 'region', 'campaign']
        db.create_unique('datapoint', ['indicator_id', 'region_id', 'campaign_id'])

        # Adding model 'RegionRelationshipType'
        db.create_table('region_relationship_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('inverse_display_name', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['RegionRelationshipType'])

        # Adding model 'RegionRelationship'
        db.create_table('region_relationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region_0', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ind_0', to=orm['datapoints.Region'])),
            ('region_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ind_1', to=orm['datapoints.Region'])),
            ('region_relationship_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.RegionRelationshipType'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['RegionRelationship'])

        # Adding model 'Document'
        db.create_table('document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'datapoints', ['Document'])

        # Adding model 'AggregationType'
        db.create_table('aggregation_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('display_name_w_sub', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['AggregationType'])

        # Adding model 'AggregationExpectedData'
        db.create_table('aggregation_expected_data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aggregation_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datapoints.AggregationType'])),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('param_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=55, populate_from=('aggregation_type', 'content_type'), unique_with=())),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['AggregationExpectedData'])


    def backwards(self, orm):
        # Removing unique constraint on 'DataPoint', fields ['indicator', 'region', 'campaign']
        db.delete_unique('datapoint', ['indicator_id', 'region_id', 'campaign_id'])

        # Deleting model 'Indicator'
        db.delete_table('indicator')

        # Deleting model 'Office'
        db.delete_table('office')

        # Deleting model 'Region'
        db.delete_table('region')

        # Deleting model 'Campaign'
        db.delete_table('campaign')

        # Deleting model 'HistoricalDataPoint'
        db.delete_table(u'datapoints_historicaldatapoint')

        # Deleting model 'DataPoint'
        db.delete_table('datapoint')

        # Deleting model 'RegionRelationshipType'
        db.delete_table('region_relationship_type')

        # Deleting model 'RegionRelationship'
        db.delete_table('region_relationship')

        # Deleting model 'Document'
        db.delete_table('document')

        # Deleting model 'AggregationType'
        db.delete_table('aggregation_type')

        # Deleting model 'AggregationExpectedData'
        db.delete_table('aggregation_expected_data')


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
        u'datapoints.aggregationexpecteddata': {
            'Meta': {'object_name': 'AggregationExpectedData', 'db_table': "'aggregation_expected_data'"},
            'aggregation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.AggregationType']"}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'param_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '55', 'populate_from': "('aggregation_type', 'content_type')", 'unique_with': '()'})
        },
        u'datapoints.aggregationtype': {
            'Meta': {'object_name': 'AggregationType', 'db_table': "'aggregation_type'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'display_name_w_sub': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'datapoints.campaign': {
            'Meta': {'object_name': 'Campaign', 'db_table': "'campaign'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'get_full_name'"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'datapoints.datapoint': {
            'Meta': {'unique_together': "(('indicator', 'region', 'campaign'),)", 'object_name': 'DataPoint', 'db_table': "'datapoint'"},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Campaign']"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Indicator']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Region']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'})
        },
        u'datapoints.document': {
            'Meta': {'object_name': 'Document', 'db_table': "'document'"},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'datapoints.historicaldatapoint': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalDataPoint'},
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
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'})
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
        u'datapoints.office': {
            'Meta': {'object_name': 'Office', 'db_table': "'office'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'region'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.Office']"}),
            'shape_file_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '55', 'populate_from': "'full_name'"})
        },
        u'datapoints.regionrelationship': {
            'Meta': {'object_name': 'RegionRelationship', 'db_table': "'region_relationship'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region_0': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ind_0'", 'to': u"orm['datapoints.Region']"}),
            'region_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ind_1'", 'to': u"orm['datapoints.Region']"}),
            'region_relationship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datapoints.RegionRelationshipType']"})
        },
        u'datapoints.regionrelationshiptype': {
            'Meta': {'object_name': 'RegionRelationshipType', 'db_table': "'region_relationship_type'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inverse_display_name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        }
    }

    complete_apps = ['datapoints']