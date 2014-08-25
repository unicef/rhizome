# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VCM_Birth_Record'
        db.create_table(u'odk_source_vcm_birth_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SubmissionDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('deviceid', self.gf('django.db.models.fields.IntegerField')()),
            ('simserial', self.gf('django.db.models.fields.IntegerField')()),
            ('phonenumber', self.gf('django.db.models.fields.IntegerField')()),
            ('DateOfReport', self.gf('django.db.models.fields.DateField')()),
            ('DateReport', self.gf('django.db.models.fields.DateField')()),
            ('SettlementCode', self.gf('django.db.models.fields.IntegerField')()),
            ('HouseHoldNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('DOB', self.gf('django.db.models.fields.DateField')()),
            ('NameOfChild', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('VCM0Dose', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('VCMRILink', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('VCMNameCAttended', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('meta_instanceID', self.gf('django.db.models.fields.CharField')(unique=True, max_length=55)),
            ('KEY', self.gf('django.db.models.fields.CharField')(unique=True, max_length=55)),
        ))
        db.send_create_signal(u'odk_source', ['VCM_Birth_Record'])


    def backwards(self, orm):
        # Deleting model 'VCM_Birth_Record'
        db.delete_table(u'odk_source_vcm_birth_record')


    models = {
        u'odk_source.vcm_birth_record': {
            'DOB': ('django.db.models.fields.DateField', [], {}),
            'DateOfReport': ('django.db.models.fields.DateField', [], {}),
            'DateReport': ('django.db.models.fields.DateField', [], {}),
            'HouseHoldNumber': ('django.db.models.fields.IntegerField', [], {}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'}),
            'Meta': {'object_name': 'VCM_Birth_Record'},
            'NameOfChild': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'SettlementCode': ('django.db.models.fields.IntegerField', [], {}),
            'SubmissionDate': ('django.db.models.fields.DateTimeField', [], {}),
            'VCM0Dose': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'VCMNameCAttended': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'VCMRILink': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'deviceid': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'}),
            'phonenumber': ('django.db.models.fields.IntegerField', [], {}),
            'simserial': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['odk_source']