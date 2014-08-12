# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'IndicatorPct'
        db.create_table('indicator_pct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indicator_part', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ind_part', to=orm['datapoints.Indicator'])),
            ('indicator_whole', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ind_whole', to=orm['datapoints.Indicator'])),
            ('indicator_pct_display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'datapoints', ['IndicatorPct'])

    models = {
        u'datapoints.indicator': {
            'Meta': {'object_name': 'Indicator', 'db_table': "'indicator'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reported': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        u'datapoints.indicatorpct': {
            'Meta': {'object_name': 'IndicatorPct', 'db_table': "'indicator_pct'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator_part': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ind_part'", 'to': u"orm['datapoints.Indicator']"}),
            'indicator_pct_display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'indicator_whole': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ind_whole'", 'to': u"orm['datapoints.Indicator']"})
        },
    }

    complete_apps = ['datapoints']