# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'VCM_Birth_Record'
        db.delete_table(u'odk_source_vcm_birth_record')

        # Adding model 'VCMBirthRecord'
        db.create_table(u'odk_source_vcmbirthrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SubmissionDate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('deviceid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('simserial', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phonenumber', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('DateOfReport', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('DateReport', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('SettlementCode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('HouseHoldNumber', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('DOB', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('NameOfChild', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('VCM0Dose', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('VCMRILink', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('VCMNameCAttended', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_instanceID', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('KEY', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'odk_source', ['VCMBirthRecord'])


    def backwards(self, orm):
        # Adding model 'VCM_Birth_Record'
        db.create_table(u'odk_source_vcm_birth_record', (
            ('SettlementCode', self.gf('django.db.models.fields.IntegerField')()),
            ('simserial', self.gf('django.db.models.fields.IntegerField')()),
            ('HouseHoldNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('VCMRILink', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('NameOfChild', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('DOB', self.gf('django.db.models.fields.DateField')()),
            ('VCMNameCAttended', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('meta_instanceID', self.gf('django.db.models.fields.CharField')(max_length=55, unique=True)),
            ('VCM0Dose', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('SubmissionDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('phonenumber', self.gf('django.db.models.fields.IntegerField')()),
            ('DateOfReport', self.gf('django.db.models.fields.DateField')()),
            ('KEY', self.gf('django.db.models.fields.CharField')(max_length=55, unique=True)),
            ('DateReport', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deviceid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'odk_source', ['VCM_Birth_Record'])

        # Deleting model 'VCMBirthRecord'
        db.delete_table(u'odk_source_vcmbirthrecord')


    models = {
        u'odk_source.vcmbirthrecord': {
            'DOB': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'HouseHoldNumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'VCMBirthRecord'},
            'NameOfChild': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCM0Dose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMNameCAttended': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMRILink': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['odk_source']