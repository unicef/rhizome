# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ClusterSupervisor.supervision_location_Accuracy'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_Accuracy')

        # Deleting field 'ClusterSupervisor.supervision_location_Altitude'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_Altitude')

        # Deleting field 'ClusterSupervisor.SubmissionDate'
        db.delete_column(u'source_data_clustersupervisor', 'SubmissionDate')

        # Deleting field 'ClusterSupervisor.meta_instanceID'
        db.delete_column(u'source_data_clustersupervisor', 'meta_instanceID')

        # Deleting field 'ClusterSupervisor.supervision_location_Latitude'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_Latitude')

        # Deleting field 'ClusterSupervisor.DateRecorded'
        db.delete_column(u'source_data_clustersupervisor', 'DateRecorded')

        # Deleting field 'ClusterSupervisor.supervision_location_Longitude'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_Longitude')

        # Deleting field 'ClusterSupervisor.num_LGAC'
        db.delete_column(u'source_data_clustersupervisor', 'num_LGAC')

        # Deleting field 'ClusterSupervisor.KEY'
        db.delete_column(u'source_data_clustersupervisor', 'KEY')

        # Adding field 'ClusterSupervisor.submissiondate'
        db.add_column(u'source_data_clustersupervisor', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.daterecorded'
        db.add_column(u'source_data_clustersupervisor', 'daterecorded',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.supervision_location_latitude'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_latitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.supervision_location_longitude'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_longitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.supervision_location_altitude'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_altitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.supervision_location_accuracy'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_accuracy',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.num_lgac'
        db.add_column(u'source_data_clustersupervisor', 'num_lgac',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.meta_instanceid'
        db.add_column(u'source_data_clustersupervisor', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClusterSupervisor.key'
        db.add_column(u'source_data_clustersupervisor', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)

        # Deleting field 'PhoneInventory.Asset_number'
        db.delete_column(u'source_data_phoneinventory', 'Asset_number')

        # Deleting field 'PhoneInventory.Colour_phone'
        db.delete_column(u'source_data_phoneinventory', 'Colour_phone')

        # Deleting field 'PhoneInventory.meta_instanceID'
        db.delete_column(u'source_data_phoneinventory', 'meta_instanceID')

        # Deleting field 'PhoneInventory.SubmissionDate'
        db.delete_column(u'source_data_phoneinventory', 'SubmissionDate')

        # Deleting field 'PhoneInventory.State'
        db.delete_column(u'source_data_phoneinventory', 'State')

        # Deleting field 'PhoneInventory.DeviceID'
        db.delete_column(u'source_data_phoneinventory', 'DeviceID')

        # Deleting field 'PhoneInventory.Name'
        db.delete_column(u'source_data_phoneinventory', 'Name')

        # Deleting field 'PhoneInventory.LGA'
        db.delete_column(u'source_data_phoneinventory', 'LGA')

        # Deleting field 'PhoneInventory.KEY'
        db.delete_column(u'source_data_phoneinventory', 'KEY')

        # Adding field 'PhoneInventory.submissiondate'
        db.add_column(u'source_data_phoneinventory', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.meta_instanceid'
        db.add_column(u'source_data_phoneinventory', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.name'
        db.add_column(u'source_data_phoneinventory', 'name',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.state'
        db.add_column(u'source_data_phoneinventory', 'state',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.lga'
        db.add_column(u'source_data_phoneinventory', 'lga',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.colour_phone'
        db.add_column(u'source_data_phoneinventory', 'colour_phone',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.asset_number'
        db.add_column(u'source_data_phoneinventory', 'asset_number',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.deviceid'
        db.add_column(u'source_data_phoneinventory', 'deviceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.key'
        db.add_column(u'source_data_phoneinventory', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.supervision_location_Accuracy'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.supervision_location_Accuracy' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.supervision_location_Accuracy'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_Accuracy',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.supervision_location_Altitude'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.supervision_location_Altitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.supervision_location_Altitude'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_Altitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.SubmissionDate'
        db.add_column(u'source_data_clustersupervisor', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.meta_instanceID'
        db.add_column(u'source_data_clustersupervisor', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.supervision_location_Latitude'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.supervision_location_Latitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.supervision_location_Latitude'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_Latitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.DateRecorded'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.DateRecorded' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.DateRecorded'
        db.add_column(u'source_data_clustersupervisor', 'DateRecorded',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.supervision_location_Longitude'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.supervision_location_Longitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.supervision_location_Longitude'
        db.add_column(u'source_data_clustersupervisor', 'supervision_location_Longitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.num_LGAC'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.num_LGAC' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.num_LGAC'
        db.add_column(u'source_data_clustersupervisor', 'num_LGAC',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ClusterSupervisor.KEY'
        raise RuntimeError("Cannot reverse this migration. 'ClusterSupervisor.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ClusterSupervisor.KEY'
        db.add_column(u'source_data_clustersupervisor', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)

        # Deleting field 'ClusterSupervisor.submissiondate'
        db.delete_column(u'source_data_clustersupervisor', 'submissiondate')

        # Deleting field 'ClusterSupervisor.daterecorded'
        db.delete_column(u'source_data_clustersupervisor', 'daterecorded')

        # Deleting field 'ClusterSupervisor.supervision_location_latitude'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_latitude')

        # Deleting field 'ClusterSupervisor.supervision_location_longitude'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_longitude')

        # Deleting field 'ClusterSupervisor.supervision_location_altitude'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_altitude')

        # Deleting field 'ClusterSupervisor.supervision_location_accuracy'
        db.delete_column(u'source_data_clustersupervisor', 'supervision_location_accuracy')

        # Deleting field 'ClusterSupervisor.num_lgac'
        db.delete_column(u'source_data_clustersupervisor', 'num_lgac')

        # Deleting field 'ClusterSupervisor.meta_instanceid'
        db.delete_column(u'source_data_clustersupervisor', 'meta_instanceid')

        # Deleting field 'ClusterSupervisor.key'
        db.delete_column(u'source_data_clustersupervisor', 'key')

        # Adding field 'PhoneInventory.Asset_number'
        db.add_column(u'source_data_phoneinventory', 'Asset_number',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.Colour_phone'
        db.add_column(u'source_data_phoneinventory', 'Colour_phone',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.meta_instanceID'
        db.add_column(u'source_data_phoneinventory', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.SubmissionDate'
        db.add_column(u'source_data_phoneinventory', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.State'
        db.add_column(u'source_data_phoneinventory', 'State',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.DeviceID'
        db.add_column(u'source_data_phoneinventory', 'DeviceID',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.Name'
        db.add_column(u'source_data_phoneinventory', 'Name',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.LGA'
        db.add_column(u'source_data_phoneinventory', 'LGA',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PhoneInventory.KEY'
        db.add_column(u'source_data_phoneinventory', 'KEY',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255, unique=True),
                      keep_default=False)

        # Deleting field 'PhoneInventory.submissiondate'
        db.delete_column(u'source_data_phoneinventory', 'submissiondate')

        # Deleting field 'PhoneInventory.meta_instanceid'
        db.delete_column(u'source_data_phoneinventory', 'meta_instanceid')

        # Deleting field 'PhoneInventory.name'
        db.delete_column(u'source_data_phoneinventory', 'name')

        # Deleting field 'PhoneInventory.state'
        db.delete_column(u'source_data_phoneinventory', 'state')

        # Deleting field 'PhoneInventory.lga'
        db.delete_column(u'source_data_phoneinventory', 'lga')

        # Deleting field 'PhoneInventory.colour_phone'
        db.delete_column(u'source_data_phoneinventory', 'colour_phone')

        # Deleting field 'PhoneInventory.asset_number'
        db.delete_column(u'source_data_phoneinventory', 'asset_number')

        # Deleting field 'PhoneInventory.deviceid'
        db.delete_column(u'source_data_phoneinventory', 'deviceid')

        # Deleting field 'PhoneInventory.key'
        db.delete_column(u'source_data_phoneinventory', 'key')


    models = {
        'source_data.activityreport': {
            'DateRecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'ActivityReport'},
            'SettlementGPS_Accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'activity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_attendance': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_hh_pending_issues': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_iec': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_local_leadership_present': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_num_hh_affected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_num_vaccinated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_pro_opv_cd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_resolved': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_VCM_present': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_VCM_sett': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_attendance': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_iec': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_caregiver_issues': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_husband_issues': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_positive': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_vaccinated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'endtime': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_appropriate_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_clinician1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_clinician2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_crowdcontroller': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_nc_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_num_measles': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_num_opv': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_num_patients': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_num_penta': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_opvvaccinator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_recorder_opv': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_recorder_ri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_separatetally': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_stockout': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_team_allowances': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_townannouncer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipds_community_leader_present': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_issue_reported': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_issue_resolved': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_num_children': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_num_hh': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_other_issue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_team': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ipds_team_allowances': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'names': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.clustersupervisor': {
            'Meta': {'object_name': 'ClusterSupervisor'},
            'coord_rfp_meeting': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord_smwg_meetings': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord_vcm_meeting': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'daterecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fund_transparency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_activities_conducted': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_activities_planned': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_endorsed': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_implementation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_socialdata': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_special_pop': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hrop_workplan_aligned': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_lgac': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ri_supervision': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervisee_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervisor_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervisor_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcm_birthtracking': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcm_data': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcm_supervision': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'source_data.etljob': {
            'Meta': {'object_name': 'EtlJob'},
            'date_attempted': ('django.db.models.fields.DateTimeField', [], {}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'source_data.healthcamp': {
            'DateRecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'HealthCamp'},
            'SettlementGPS_Accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'agencyname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'appropriate_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clinician1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clinician2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'crowdcontroller': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'endtime': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'formhub_uuid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_photo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_stockout': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'megaphone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'names': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nc_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_measles': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_opv': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_patients': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_penta': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opvvaccinator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'recorder_opv': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recorder_ri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'separatetally': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'townannouncer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.knowthepeople': {
            'Brothers': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CitiesVisited': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DOB': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'KnowThePeople'},
            'NameOfPax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'PrefferedCity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Sisters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'State_country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.paxlistreporttraining': {
            'EmailAddr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'PaxListReportTraining'},
            'NameOfParticipant': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'PhoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'State': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'TimeStamp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.phoneinventory': {
            'Meta': {'object_name': 'PhoneInventory'},
            'asset_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'colour_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone_no': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.practicevcmbirthrecord': {
            'DOB': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'HouseHoldNumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'PracticeVCMBirthRecord'},
            'NameOfChild': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCM0Dose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMNameCAttended': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMRILink': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.practicevcmsettcoordinates': {
            'DateRecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'PracticeVCMSettCoordinates'},
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementGPS_Longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VCMPhone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.practicevcmsummary': {
            'Census12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Date_Implement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'PracticeVCMSummary'},
            'Msd_grp_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SettlementCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Vax2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VaxNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'VaxNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'group_msd_chd_Msd_NoReasonF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_Msd_NoReasonM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        },
        'source_data.processstatus': {
            'Meta': {'object_name': 'ProcessStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status_text': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'source_data.vcmbirthrecord': {
            'Meta': {'object_name': 'VCMBirthRecord'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'dateofreport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'datereport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dob': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'householdnumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nameofchild': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcm0dose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcmnamecattended': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vcmrilink': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.vcmsettlement': {
            'Meta': {'object_name': 'VCMSettlement'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
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
        },
        'source_data.vcmsummarynew': {
            'Meta': {'object_name': 'VCMSummaryNew'},
            'census12_59mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'census12_59mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'census2_11mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'census2_11mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'censusnewbornsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'censusnewbornsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'date_implement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dateofreport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'group_msd_chd_display_msd3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_agedoutf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_agedoutm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childdiedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childdiedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childsickf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childsickm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_familymovedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_familymovedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_farmf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_farmm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_hhnotvisitedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_hhnotvisitedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_marketf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_marketm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noconsentf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noconsentm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nofeltneedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nofeltneedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nogovtservicesf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nogovtservicesm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noplusesf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noplusesm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_otherprotectionf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_otherprotectionm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_playgroundf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_playgroundm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poldiffsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poldiffsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliohascuref': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliohascurem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliouncommonf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliouncommonm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_relbeliefsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_relbeliefsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_schoolf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_schoolm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_securityf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_securitym': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_sideeffectsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_sideeffectsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_soceventf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_soceventm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_toomanyroundsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_toomanyroundsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_unhappywteamf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_unhappywteamm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_tot_missed_check': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_afpcase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_cmamreferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_fic': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_mslscase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_newborn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_otherdisease': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_pregnantmother': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_rireferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_vcmattendedncer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_zerodose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spec_grp_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_12_59months': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_2_11months': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_census': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_missed': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_newborns': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_vax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_vax12_59mo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_vax2_11mo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tot_vaxnewborn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax12_59mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax12_59mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax2_11mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax2_11mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vaxnewbornsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vaxnewbornsm': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.vcmsummaryold': {
            'Meta': {'object_name': 'VCMSummaryOld'},
            'census12_59mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'census12_59mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'census2_11mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'census2_11mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'censusnewbornsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'censusnewbornsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'date_implement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dateofreport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_agedoutf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_agedoutm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childdiedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childdiedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childsickf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_childsickm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_familymovedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_familymovedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_farmf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_farmm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_hhnotvisitedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_hhnotvisitedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_marketf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_marketm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noconsentf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noconsentm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nofeltneedf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nofeltneedm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nogovtservicesf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_nogovtservicesm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noplusesf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noplusesm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noreasonf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_noreasonm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_otherprotectionf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_otherprotectionm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_playgroundf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_playgroundm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poldiffsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poldiffsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliohascuref': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliohascurem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliouncommonf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_poliouncommonm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_relbeliefsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_relbeliefsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_schoolf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_schoolm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_securityf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_securitym': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_sideeffectsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_sideeffectsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_soceventf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_soceventm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_toomanyroundsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_toomanyroundsm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_unhappywteamf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_msd_chd_msd_unhappywteamm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_afpcase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_cmamreferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_fic': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_mslscase': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_newborn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_otherdisease': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_pregnantmother': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_rireferral': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_vcmattendedncer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_spec_events_spec_zerodose': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'msd_grp_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spec_grp_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax12_59mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax12_59mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax2_11mof': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vax2_11mom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vaxnewbornsf': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vaxnewbornsm': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.vwsregister': {
            'AcceptPhoneResponsibility': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DatePhoneCollected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'FName_VWS': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'LName_VWS': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'VWSRegister'},
            'Personal_Phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'WardCode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['source_data']