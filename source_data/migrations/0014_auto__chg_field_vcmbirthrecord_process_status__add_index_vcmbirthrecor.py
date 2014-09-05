# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'VCMBirthRecord.process_status' to match new field type.
        db.rename_column(u'source_data_vcmbirthrecord', 'process_status', 'process_status_id')
        # Changing field 'VCMBirthRecord.process_status'
        db.alter_column(u'source_data_vcmbirthrecord', 'process_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['source_data.ProcessStatus']))
        # Adding index on 'VCMBirthRecord', fields ['process_status']
        db.create_index(u'source_data_vcmbirthrecord', ['process_status_id'])

        # Deleting field 'ProcessStatus.status_description'
        db.delete_column(u'source_data_processstatus', 'status_description')

        # Adding field 'ProcessStatus.status_description'
        db.add_column(u'source_data_processstatus', 'status_description',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


        # Changing field 'ProcessStatus.status_text'
        db.alter_column(u'source_data_processstatus', 'status_text', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Renaming column for 'VCMSettlement.process_status' to match new field type.
        db.rename_column(u'source_data_vcmsettlement', 'process_status', 'process_status_id')
        # Changing field 'VCMSettlement.process_status'
        db.alter_column(u'source_data_vcmsettlement', 'process_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['source_data.ProcessStatus']))
        # Adding index on 'VCMSettlement', fields ['process_status']
        db.create_index(u'source_data_vcmsettlement', ['process_status_id'])


        # Renaming column for 'VCMSummaryNew.process_status' to match new field type.
        db.rename_column(u'source_data_vcmsummarynew', 'process_status', 'process_status_id')
        # Changing field 'VCMSummaryNew.process_status'
        db.alter_column(u'source_data_vcmsummarynew', 'process_status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['source_data.ProcessStatus']))
        # Adding index on 'VCMSummaryNew', fields ['process_status']
        db.create_index(u'source_data_vcmsummarynew', ['process_status_id'])


    def backwards(self, orm):
        # Removing index on 'VCMSummaryNew', fields ['process_status']
        db.delete_index(u'source_data_vcmsummarynew', ['process_status_id'])

        # Removing index on 'VCMSettlement', fields ['process_status']
        db.delete_index(u'source_data_vcmsettlement', ['process_status_id'])

        # Removing index on 'VCMBirthRecord', fields ['process_status']
        db.delete_index(u'source_data_vcmbirthrecord', ['process_status_id'])


        # Renaming column for 'VCMBirthRecord.process_status' to match new field type.
        db.rename_column(u'source_data_vcmbirthrecord', 'process_status_id', 'process_status')
        # Changing field 'VCMBirthRecord.process_status'
        db.alter_column(u'source_data_vcmbirthrecord', 'process_status', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'ProcessStatus.status_description'
        raise RuntimeError("Cannot reverse this migration. 'ProcessStatus.status_description' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'ProcessStatus.status_description'
        db.add_column(u'source_data_processstatus', 'status_description',
                      self.gf('django.db.models.fields.CharField')(max_length=55),
                      keep_default=False)

        # Deleting field 'ProcessStatus.status_description'
        db.delete_column(u'source_data_processstatus', 'status_description')


        # Changing field 'ProcessStatus.status_text'
        db.alter_column(u'source_data_processstatus', 'status_text', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Renaming column for 'VCMSettlement.process_status' to match new field type.
        db.rename_column(u'source_data_vcmsettlement', 'process_status_id', 'process_status')
        # Changing field 'VCMSettlement.process_status'
        db.alter_column(u'source_data_vcmsettlement', 'process_status', self.gf('django.db.models.fields.IntegerField')())

        # Renaming column for 'VCMSummaryNew.process_status' to match new field type.
        db.rename_column(u'source_data_vcmsummarynew', 'process_status_id', 'process_status')
        # Changing field 'VCMSummaryNew.process_status'
        db.alter_column(u'source_data_vcmsummarynew', 'process_status', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'source_data.etljob': {
            'Meta': {'object_name': 'EtlJob'},
            'date_attempted': ('django.db.models.fields.DateTimeField', [], {}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'source_data.processstatus': {
            'Meta': {'object_name': 'ProcessStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status_text': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'source_data.vcmbirthrecord': {
            'DOB': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'HouseHoldNumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'VCMBirthRecord'},
            'NameOfChild': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCM0Dose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMNameCAttended': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMRILink': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 5, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.vcmsettlement': {
            'DateRecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'VCMSettlement'},
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMPhone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 5, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.vcmsummarynew': {
            'Census12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Date_Implement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'VCMSummaryNew'},
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_12_59Months': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_2_11Months': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Census': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Missed': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Newborns': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Vax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Vax12_59Mo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_Vax2_11Mo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Tot_VaxNewBorn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VaxNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VaxNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 5, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_msd1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_msd2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax6': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax7': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax8': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_vax9': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_AgedOutF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_AgedOutM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildDiedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildDiedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildSickF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_ChildSickM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FamilyMovedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FamilyMovedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FarmF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_FarmM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_HHNotVisitedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_HHNotVisitedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_MarketF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_MarketM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoConsentF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoConsentM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoFeltNeedF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoFeltNeedM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoGovtServicesF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoGovtServicesM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoPlusesF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoPlusesM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_OtherProtectionF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_OtherProtectionM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PlaygroundF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PlaygroundM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolDiffsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolDiffsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioHasCureF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioHasCureM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioUncommonF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_PolioUncommonM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_RelBeliefsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_RelBeliefsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SchoolF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SchoolM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SecurityF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SecurityM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SideEffectsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SideEffectsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SocEventF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_SocEventM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_TooManyRoundsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_TooManyRoundsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_UnhappyWTeamF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_UnhappyWTeamM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Tot_Missed_Check': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_display_msd3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_AFPCase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_CMAMReferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_FIC': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_MslsCase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_Newborn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_OtherDisease': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_PregnantMother': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_RIReferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_VCMAttendedNCer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_Spec_ZeroDose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spec_grp_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['source_data']
