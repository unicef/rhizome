# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'HealthCamp.meta_instanceID'
        db.delete_column(u'source_data_healthcamp', 'meta_instanceID')

        # Deleting field 'HealthCamp.SettlementGPS_Accuracy'
        db.delete_column(u'source_data_healthcamp', 'SettlementGPS_Accuracy')

        # Deleting field 'HealthCamp.SubmissionDate'
        db.delete_column(u'source_data_healthcamp', 'SubmissionDate')

        # Deleting field 'HealthCamp.SettlementGPS_Latitude'
        db.delete_column(u'source_data_healthcamp', 'SettlementGPS_Latitude')

        # Deleting field 'HealthCamp.DateRecorded'
        db.delete_column(u'source_data_healthcamp', 'DateRecorded')

        # Deleting field 'HealthCamp.SettlementGPS_Longitude'
        db.delete_column(u'source_data_healthcamp', 'SettlementGPS_Longitude')

        # Deleting field 'HealthCamp.SettlementGPS_Altitude'
        db.delete_column(u'source_data_healthcamp', 'SettlementGPS_Altitude')

        # Deleting field 'HealthCamp.KEY'
        db.delete_column(u'source_data_healthcamp', 'KEY')

        # Adding field 'HealthCamp.submissiondate'
        db.add_column(u'source_data_healthcamp', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.daterecorded'
        db.add_column(u'source_data_healthcamp', 'daterecorded',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.settlementgps_latitude'
        db.add_column(u'source_data_healthcamp', 'settlementgps_latitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.settlementgps_longitude'
        db.add_column(u'source_data_healthcamp', 'settlementgps_longitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.settlementgps_altitude'
        db.add_column(u'source_data_healthcamp', 'settlementgps_altitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.settlementgps_accuracy'
        db.add_column(u'source_data_healthcamp', 'settlementgps_accuracy',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.meta_instanceid'
        db.add_column(u'source_data_healthcamp', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'HealthCamp.key'
        db.add_column(u'source_data_healthcamp', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)

        # Deleting field 'PaxListReportTraining.Title'
        db.delete_column(u'source_data_paxlistreporttraining', 'Title')

        # Deleting field 'PaxListReportTraining.TimeStamp'
        db.delete_column(u'source_data_paxlistreporttraining', 'TimeStamp')

        # Deleting field 'PaxListReportTraining.meta_instanceID'
        db.delete_column(u'source_data_paxlistreporttraining', 'meta_instanceID')

        # Deleting field 'PaxListReportTraining.SubmissionDate'
        db.delete_column(u'source_data_paxlistreporttraining', 'SubmissionDate')

        # Deleting field 'PaxListReportTraining.State'
        db.delete_column(u'source_data_paxlistreporttraining', 'State')

        # Deleting field 'PaxListReportTraining.PhoneNumber'
        db.delete_column(u'source_data_paxlistreporttraining', 'PhoneNumber')

        # Deleting field 'PaxListReportTraining.EmailAddr'
        db.delete_column(u'source_data_paxlistreporttraining', 'EmailAddr')

        # Deleting field 'PaxListReportTraining.KEY'
        db.delete_column(u'source_data_paxlistreporttraining', 'KEY')

        # Deleting field 'PaxListReportTraining.NameOfParticipant'
        db.delete_column(u'source_data_paxlistreporttraining', 'NameOfParticipant')

        # Adding field 'PaxListReportTraining.submissiondate'
        db.add_column(u'source_data_paxlistreporttraining', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.meta_instanceid'
        db.add_column(u'source_data_paxlistreporttraining', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.state'
        db.add_column(u'source_data_paxlistreporttraining', 'state',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.nameofparticipant'
        db.add_column(u'source_data_paxlistreporttraining', 'nameofparticipant',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.title'
        db.add_column(u'source_data_paxlistreporttraining', 'title',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.phonenumber'
        db.add_column(u'source_data_paxlistreporttraining', 'phonenumber',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.emailaddr'
        db.add_column(u'source_data_paxlistreporttraining', 'emailaddr',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.timestamp'
        db.add_column(u'source_data_paxlistreporttraining', 'timestamp',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PaxListReportTraining.key'
        db.add_column(u'source_data_paxlistreporttraining', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)

        # Deleting field 'PracticeVCMSettCoordinates.SettlementCode'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SettlementCode')

        # Deleting field 'PracticeVCMSettCoordinates.DateRecorded'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'DateRecorded')

        # Deleting field 'PracticeVCMSettCoordinates.VCMPhone'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'VCMPhone')

        # Deleting field 'PracticeVCMSettCoordinates.SettlementName'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SettlementName')

        # Deleting field 'PracticeVCMSettCoordinates.SettlementGPS_Accuracy'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Accuracy')

        # Deleting field 'PracticeVCMSettCoordinates.VCMName'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'VCMName')

        # Deleting field 'PracticeVCMSettCoordinates.meta_instanceID'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'meta_instanceID')

        # Deleting field 'PracticeVCMSettCoordinates.SettlementGPS_Longitude'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Longitude')

        # Deleting field 'PracticeVCMSettCoordinates.SettlementGPS_Altitude'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Altitude')

        # Deleting field 'PracticeVCMSettCoordinates.SubmissionDate'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SubmissionDate')

        # Deleting field 'PracticeVCMSettCoordinates.KEY'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'KEY')

        # Deleting field 'PracticeVCMSettCoordinates.SettlementGPS_Latitude'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Latitude')

        # Adding field 'PracticeVCMSettCoordinates.submissiondate'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.daterecorded'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'daterecorded',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.settlementcode'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'settlementcode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.settlementname'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'settlementname',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.vcmname'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'vcmname',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.vcmphone'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'vcmphone',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.settlementgps_latitude'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_latitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.settlementgps_longitude'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_longitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.settlementgps_altitude'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_altitude',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.settlementgps_accuracy'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_accuracy',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.meta_instanceid'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSettCoordinates.key'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoPlusesM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoPlusesM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoPlusesF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoPlusesF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_AgedOutM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_RelBeliefsF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_AgedOutF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_RelBeliefsM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SideEffectsF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SideEffectsM')

        # Deleting field 'PracticeVCMSummary.CensusNewBornsF'
        db.delete_column(u'source_data_practicevcmsummary', 'CensusNewBornsF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SocEventM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SocEventM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_UnhappyWTeamM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoFeltNeedF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SocEventF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SocEventF')

        # Deleting field 'PracticeVCMSummary.CensusNewBornsM'
        db.delete_column(u'source_data_practicevcmsummary', 'CensusNewBornsM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoFeltNeedM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_UnhappyWTeamF')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_AFPCase'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_AFPCase')

        # Deleting field 'PracticeVCMSummary.Census2_11MoM'
        db.delete_column(u'source_data_practicevcmsummary', 'Census2_11MoM')

        # Deleting field 'PracticeVCMSummary.Msd_grp_choice'
        db.delete_column(u'source_data_practicevcmsummary', 'Msd_grp_choice')

        # Deleting field 'PracticeVCMSummary.Census2_11MoF'
        db.delete_column(u'source_data_practicevcmsummary', 'Census2_11MoF')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_OtherDisease'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_OtherDisease')

        # Deleting field 'PracticeVCMSummary.Date_Implement'
        db.delete_column(u'source_data_practicevcmsummary', 'Date_Implement')

        # Deleting field 'PracticeVCMSummary.meta_instanceID'
        db.delete_column(u'source_data_practicevcmsummary', 'meta_instanceID')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoGovtServicesM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoGovtServicesF')

        # Deleting field 'PracticeVCMSummary.Vax12_59MoM'
        db.delete_column(u'source_data_practicevcmsummary', 'Vax12_59MoM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SchoolF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SchoolF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SchoolM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SchoolM')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_VCMAttendedNCer'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_VCMAttendedNCer')

        # Deleting field 'PracticeVCMSummary.Vax2_11MoF'
        db.delete_column(u'source_data_practicevcmsummary', 'Vax2_11MoF')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_PregnantMother'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_PregnantMother')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PlaygroundM')

        # Deleting field 'PracticeVCMSummary.Vax2_11MoM'
        db.delete_column(u'source_data_practicevcmsummary', 'Vax2_11MoM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PlaygroundF')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_RIReferral'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_RIReferral')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoReasonM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoReasonF')

        # Deleting field 'PracticeVCMSummary.SubmissionDate'
        db.delete_column(u'source_data_practicevcmsummary', 'SubmissionDate')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_OtherProtectionF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_OtherProtectionM')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_Newborn'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_Newborn')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_ZeroDose'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_ZeroDose')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_CMAMReferral'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_CMAMReferral')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SecurityM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SecurityM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_SecurityF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SecurityF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_TooManyRoundsF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_TooManyRoundsM')

        # Deleting field 'PracticeVCMSummary.KEY'
        db.delete_column(u'source_data_practicevcmsummary', 'KEY')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_FIC'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_FIC')

        # Deleting field 'PracticeVCMSummary.Vax12_59MoF'
        db.delete_column(u'source_data_practicevcmsummary', 'Vax12_59MoF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_MarketM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_MarketM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_MarketF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_MarketF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_HHNotVisitedF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_HHNotVisitedM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoConsentM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioUncommonM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildDiedF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolDiffsM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioUncommonF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolDiffsF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildDiedM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_FarmM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FarmM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_FarmF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FarmF')

        # Deleting field 'PracticeVCMSummary.SettlementCode'
        db.delete_column(u'source_data_practicevcmsummary', 'SettlementCode')

        # Deleting field 'PracticeVCMSummary.VaxNewBornsM'
        db.delete_column(u'source_data_practicevcmsummary', 'VaxNewBornsM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FamilyMovedF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FamilyMovedM')

        # Deleting field 'PracticeVCMSummary.VaxNewBornsF'
        db.delete_column(u'source_data_practicevcmsummary', 'VaxNewBornsF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoConsentF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioHasCureM')

        # Deleting field 'PracticeVCMSummary.Census12_59MoM'
        db.delete_column(u'source_data_practicevcmsummary', 'Census12_59MoM')

        # Deleting field 'PracticeVCMSummary.DateOfReport'
        db.delete_column(u'source_data_practicevcmsummary', 'DateOfReport')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickM'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildSickM')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioHasCureF')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickF'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildSickF')

        # Deleting field 'PracticeVCMSummary.group_spec_events_Spec_MslsCase'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_MslsCase')

        # Deleting field 'PracticeVCMSummary.Census12_59MoF'
        db.delete_column(u'source_data_practicevcmsummary', 'Census12_59MoF')

        # Adding field 'PracticeVCMSummary.submissiondate'
        db.add_column(u'source_data_practicevcmsummary', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.dateofreport'
        db.add_column(u'source_data_practicevcmsummary', 'dateofreport',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.date_implement'
        db.add_column(u'source_data_practicevcmsummary', 'date_implement',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.settlementcode'
        db.add_column(u'source_data_practicevcmsummary', 'settlementcode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.censusnewbornsf'
        db.add_column(u'source_data_practicevcmsummary', 'censusnewbornsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.censusnewbornsm'
        db.add_column(u'source_data_practicevcmsummary', 'censusnewbornsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.census2_11mof'
        db.add_column(u'source_data_practicevcmsummary', 'census2_11mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.census2_11mom'
        db.add_column(u'source_data_practicevcmsummary', 'census2_11mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.census12_59mof'
        db.add_column(u'source_data_practicevcmsummary', 'census12_59mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.census12_59mom'
        db.add_column(u'source_data_practicevcmsummary', 'census12_59mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.vaxnewbornsf'
        db.add_column(u'source_data_practicevcmsummary', 'vaxnewbornsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.vaxnewbornsm'
        db.add_column(u'source_data_practicevcmsummary', 'vaxnewbornsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.vax2_11mof'
        db.add_column(u'source_data_practicevcmsummary', 'vax2_11mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.vax2_11mom'
        db.add_column(u'source_data_practicevcmsummary', 'vax2_11mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.vax12_59mof'
        db.add_column(u'source_data_practicevcmsummary', 'vax12_59mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.vax12_59mom'
        db.add_column(u'source_data_practicevcmsummary', 'vax12_59mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.msd_grp_choice'
        db.add_column(u'source_data_practicevcmsummary', 'msd_grp_choice',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_playgroundf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_playgroundf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_playgroundm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_playgroundm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_soceventf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_soceventf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_soceventm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_soceventm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_marketf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_marketf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_marketm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_marketm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_farmf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_farmf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_farmm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_farmm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_schoolf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_schoolf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_schoolm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_schoolm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_childsickf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childsickf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_childsickm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childsickm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_sideeffectsf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_sideeffectsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_sideeffectsm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_sideeffectsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_nofeltneedf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nofeltneedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_nofeltneedm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nofeltneedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_toomanyroundsf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_toomanyroundsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_toomanyroundsm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_toomanyroundsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_relbeliefsf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_relbeliefsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_relbeliefsm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_relbeliefsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_poldiffsf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poldiffsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_poldiffsm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poldiffsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_unhappywteamf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_unhappywteamf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_unhappywteamm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_unhappywteamm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_noplusesf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noplusesf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_noplusesm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noplusesm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_nogovtservicesf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nogovtservicesf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_nogovtservicesm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nogovtservicesm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_poliouncommonf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliouncommonf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_poliouncommonm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliouncommonm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_poliohascuref'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliohascuref',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_poliohascurem'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliohascurem',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_otherprotectionf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_otherprotectionf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_otherprotectionm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_otherprotectionm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_noconsentf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noconsentf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_noconsentm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noconsentm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_hhnotvisitedf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_hhnotvisitedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_hhnotvisitedm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_hhnotvisitedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_noreasonf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noreasonf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_noreasonm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noreasonm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_securityf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_securityf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_securitym'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_securitym',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_agedoutf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_agedoutf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_agedoutm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_agedoutm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_familymovedf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_familymovedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_familymovedm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_familymovedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_childdiedf'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childdiedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_msd_chd_msd_childdiedm'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childdiedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_zerodose'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_zerodose',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_pregnantmother'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_pregnantmother',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_newborn'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_newborn',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_vcmattendedncer'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_vcmattendedncer',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_cmamreferral'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_cmamreferral',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_rireferral'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_rireferral',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_afpcase'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_afpcase',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_mslscase'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_mslscase',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_otherdisease'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_otherdisease',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.group_spec_events_spec_fic'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_fic',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.meta_instanceid'
        db.add_column(u'source_data_practicevcmsummary', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'PracticeVCMSummary.key'
        db.add_column(u'source_data_practicevcmsummary', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'HealthCamp.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.meta_instanceID'
        db.add_column(u'source_data_healthcamp', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.SettlementGPS_Accuracy'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.SettlementGPS_Accuracy' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.SettlementGPS_Accuracy'
        db.add_column(u'source_data_healthcamp', 'SettlementGPS_Accuracy',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.SubmissionDate'
        db.add_column(u'source_data_healthcamp', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.SettlementGPS_Latitude'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.SettlementGPS_Latitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.SettlementGPS_Latitude'
        db.add_column(u'source_data_healthcamp', 'SettlementGPS_Latitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.DateRecorded'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.DateRecorded' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.DateRecorded'
        db.add_column(u'source_data_healthcamp', 'DateRecorded',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.SettlementGPS_Longitude'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.SettlementGPS_Longitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.SettlementGPS_Longitude'
        db.add_column(u'source_data_healthcamp', 'SettlementGPS_Longitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.SettlementGPS_Altitude'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.SettlementGPS_Altitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.SettlementGPS_Altitude'
        db.add_column(u'source_data_healthcamp', 'SettlementGPS_Altitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HealthCamp.KEY'
        raise RuntimeError("Cannot reverse this migration. 'HealthCamp.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HealthCamp.KEY'
        db.add_column(u'source_data_healthcamp', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)

        # Deleting field 'HealthCamp.submissiondate'
        db.delete_column(u'source_data_healthcamp', 'submissiondate')

        # Deleting field 'HealthCamp.daterecorded'
        db.delete_column(u'source_data_healthcamp', 'daterecorded')

        # Deleting field 'HealthCamp.settlementgps_latitude'
        db.delete_column(u'source_data_healthcamp', 'settlementgps_latitude')

        # Deleting field 'HealthCamp.settlementgps_longitude'
        db.delete_column(u'source_data_healthcamp', 'settlementgps_longitude')

        # Deleting field 'HealthCamp.settlementgps_altitude'
        db.delete_column(u'source_data_healthcamp', 'settlementgps_altitude')

        # Deleting field 'HealthCamp.settlementgps_accuracy'
        db.delete_column(u'source_data_healthcamp', 'settlementgps_accuracy')

        # Deleting field 'HealthCamp.meta_instanceid'
        db.delete_column(u'source_data_healthcamp', 'meta_instanceid')

        # Deleting field 'HealthCamp.key'
        db.delete_column(u'source_data_healthcamp', 'key')

        # Adding field 'PaxListReportTraining.Title'
        db.add_column(u'source_data_paxlistreporttraining', 'Title',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.TimeStamp'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.TimeStamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.TimeStamp'
        db.add_column(u'source_data_paxlistreporttraining', 'TimeStamp',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.meta_instanceID'
        db.add_column(u'source_data_paxlistreporttraining', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.SubmissionDate'
        db.add_column(u'source_data_paxlistreporttraining', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.State'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.State' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.State'
        db.add_column(u'source_data_paxlistreporttraining', 'State',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.PhoneNumber'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.PhoneNumber' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.PhoneNumber'
        db.add_column(u'source_data_paxlistreporttraining', 'PhoneNumber',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.EmailAddr'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.EmailAddr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.EmailAddr'
        db.add_column(u'source_data_paxlistreporttraining', 'EmailAddr',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.KEY'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.KEY'
        db.add_column(u'source_data_paxlistreporttraining', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PaxListReportTraining.NameOfParticipant'
        raise RuntimeError("Cannot reverse this migration. 'PaxListReportTraining.NameOfParticipant' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PaxListReportTraining.NameOfParticipant'
        db.add_column(u'source_data_paxlistreporttraining', 'NameOfParticipant',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'PaxListReportTraining.submissiondate'
        db.delete_column(u'source_data_paxlistreporttraining', 'submissiondate')

        # Deleting field 'PaxListReportTraining.meta_instanceid'
        db.delete_column(u'source_data_paxlistreporttraining', 'meta_instanceid')

        # Deleting field 'PaxListReportTraining.state'
        db.delete_column(u'source_data_paxlistreporttraining', 'state')

        # Deleting field 'PaxListReportTraining.nameofparticipant'
        db.delete_column(u'source_data_paxlistreporttraining', 'nameofparticipant')

        # Deleting field 'PaxListReportTraining.title'
        db.delete_column(u'source_data_paxlistreporttraining', 'title')

        # Deleting field 'PaxListReportTraining.phonenumber'
        db.delete_column(u'source_data_paxlistreporttraining', 'phonenumber')

        # Deleting field 'PaxListReportTraining.emailaddr'
        db.delete_column(u'source_data_paxlistreporttraining', 'emailaddr')

        # Deleting field 'PaxListReportTraining.timestamp'
        db.delete_column(u'source_data_paxlistreporttraining', 'timestamp')

        # Deleting field 'PaxListReportTraining.key'
        db.delete_column(u'source_data_paxlistreporttraining', 'key')

        # Adding field 'PracticeVCMSettCoordinates.SettlementCode'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SettlementCode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.DateRecorded'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.DateRecorded' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.DateRecorded'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'DateRecorded',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.VCMPhone'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.VCMPhone' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.VCMPhone'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'VCMPhone',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.SettlementName'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.SettlementName' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.SettlementName'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SettlementName',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.SettlementGPS_Accuracy'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.SettlementGPS_Accuracy' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.SettlementGPS_Accuracy'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Accuracy',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.VCMName'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.VCMName' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.VCMName'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'VCMName',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.meta_instanceID'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.SettlementGPS_Longitude'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.SettlementGPS_Longitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.SettlementGPS_Longitude'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Longitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.SettlementGPS_Altitude'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.SettlementGPS_Altitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.SettlementGPS_Altitude'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Altitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.SubmissionDate'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.KEY'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.KEY'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSettCoordinates.SettlementGPS_Latitude'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSettCoordinates.SettlementGPS_Latitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSettCoordinates.SettlementGPS_Latitude'
        db.add_column(u'source_data_practicevcmsettcoordinates', 'SettlementGPS_Latitude',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'PracticeVCMSettCoordinates.submissiondate'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'submissiondate')

        # Deleting field 'PracticeVCMSettCoordinates.daterecorded'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'daterecorded')

        # Deleting field 'PracticeVCMSettCoordinates.settlementcode'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'settlementcode')

        # Deleting field 'PracticeVCMSettCoordinates.settlementname'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'settlementname')

        # Deleting field 'PracticeVCMSettCoordinates.vcmname'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'vcmname')

        # Deleting field 'PracticeVCMSettCoordinates.vcmphone'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'vcmphone')

        # Deleting field 'PracticeVCMSettCoordinates.settlementgps_latitude'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_latitude')

        # Deleting field 'PracticeVCMSettCoordinates.settlementgps_longitude'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_longitude')

        # Deleting field 'PracticeVCMSettCoordinates.settlementgps_altitude'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_altitude')

        # Deleting field 'PracticeVCMSettCoordinates.settlementgps_accuracy'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'settlementgps_accuracy')

        # Deleting field 'PracticeVCMSettCoordinates.meta_instanceid'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'meta_instanceid')

        # Deleting field 'PracticeVCMSettCoordinates.key'
        db.delete_column(u'source_data_practicevcmsettcoordinates', 'key')

        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoPlusesM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoPlusesM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoPlusesF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoPlusesF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoPlusesF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoPlusesF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_AgedOutM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_RelBeliefsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_AgedOutF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_AgedOutF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_RelBeliefsM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_RelBeliefsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SideEffectsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SideEffectsM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SideEffectsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.CensusNewBornsF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.CensusNewBornsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.CensusNewBornsF'
        db.add_column(u'source_data_practicevcmsummary', 'CensusNewBornsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SocEventM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SocEventM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SocEventM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SocEventM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_UnhappyWTeamM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoFeltNeedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SocEventF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SocEventF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SocEventF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SocEventF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.CensusNewBornsM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.CensusNewBornsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.CensusNewBornsM'
        db.add_column(u'source_data_practicevcmsummary', 'CensusNewBornsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoFeltNeedM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoFeltNeedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_UnhappyWTeamF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_UnhappyWTeamF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_AFPCase'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_AFPCase' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_AFPCase'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_AFPCase',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Census2_11MoM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Census2_11MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Census2_11MoM'
        db.add_column(u'source_data_practicevcmsummary', 'Census2_11MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Msd_grp_choice'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Msd_grp_choice' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Msd_grp_choice'
        db.add_column(u'source_data_practicevcmsummary', 'Msd_grp_choice',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Census2_11MoF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Census2_11MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Census2_11MoF'
        db.add_column(u'source_data_practicevcmsummary', 'Census2_11MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_OtherDisease'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_OtherDisease' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_OtherDisease'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_OtherDisease',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Date_Implement'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Date_Implement' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Date_Implement'
        db.add_column(u'source_data_practicevcmsummary', 'Date_Implement',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.meta_instanceID'
        db.add_column(u'source_data_practicevcmsummary', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoGovtServicesM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoGovtServicesF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoGovtServicesF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Vax12_59MoM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Vax12_59MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Vax12_59MoM'
        db.add_column(u'source_data_practicevcmsummary', 'Vax12_59MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SchoolF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SchoolF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SchoolF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SchoolF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SchoolM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SchoolM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SchoolM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SchoolM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_VCMAttendedNCer'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_VCMAttendedNCer' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_VCMAttendedNCer'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_VCMAttendedNCer',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Vax2_11MoF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Vax2_11MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Vax2_11MoF'
        db.add_column(u'source_data_practicevcmsummary', 'Vax2_11MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_PregnantMother'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_PregnantMother' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_PregnantMother'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_PregnantMother',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PlaygroundM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Vax2_11MoM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Vax2_11MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Vax2_11MoM'
        db.add_column(u'source_data_practicevcmsummary', 'Vax2_11MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PlaygroundF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PlaygroundF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_RIReferral'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_RIReferral' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_RIReferral'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_RIReferral',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoReasonM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoReasonF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoReasonF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.SubmissionDate'
        db.add_column(u'source_data_practicevcmsummary', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_OtherProtectionF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_OtherProtectionM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_OtherProtectionM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_Newborn'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_Newborn' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_Newborn'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_Newborn',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_ZeroDose'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_ZeroDose' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_ZeroDose'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_ZeroDose',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_CMAMReferral'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_CMAMReferral' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_CMAMReferral'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_CMAMReferral',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SecurityM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SecurityM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SecurityM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SecurityM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_SecurityF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_SecurityF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_SecurityF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_SecurityF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_TooManyRoundsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_TooManyRoundsM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_TooManyRoundsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.KEY'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.KEY'
        db.add_column(u'source_data_practicevcmsummary', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_FIC'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_FIC' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_FIC'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_FIC',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Vax12_59MoF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Vax12_59MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Vax12_59MoF'
        db.add_column(u'source_data_practicevcmsummary', 'Vax12_59MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_MarketM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_MarketM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_MarketM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_MarketM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_MarketF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_MarketF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_MarketF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_MarketF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_HHNotVisitedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_HHNotVisitedM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_HHNotVisitedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoConsentM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioUncommonM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildDiedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolDiffsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PolioUncommonF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioUncommonF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PolDiffsF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolDiffsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_ChildDiedM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildDiedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_FarmM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_FarmM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_FarmM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FarmM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_FarmF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_FarmF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_FarmF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FarmF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.SettlementCode'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.SettlementCode' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.SettlementCode'
        db.add_column(u'source_data_practicevcmsummary', 'SettlementCode',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.VaxNewBornsM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.VaxNewBornsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.VaxNewBornsM'
        db.add_column(u'source_data_practicevcmsummary', 'VaxNewBornsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FamilyMovedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_FamilyMovedM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_FamilyMovedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.VaxNewBornsF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.VaxNewBornsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.VaxNewBornsF'
        db.add_column(u'source_data_practicevcmsummary', 'VaxNewBornsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_NoConsentF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_NoConsentF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioHasCureM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Census12_59MoM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Census12_59MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Census12_59MoM'
        db.add_column(u'source_data_practicevcmsummary', 'Census12_59MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.DateOfReport'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.DateOfReport' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.DateOfReport'
        db.add_column(u'source_data_practicevcmsummary', 'DateOfReport',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickM'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickM'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildSickM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_PolioHasCureF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_PolioHasCureF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_msd_chd_Msd_ChildSickF'
        db.add_column(u'source_data_practicevcmsummary', 'group_msd_chd_Msd_ChildSickF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.group_spec_events_Spec_MslsCase'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.group_spec_events_Spec_MslsCase' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.group_spec_events_Spec_MslsCase'
        db.add_column(u'source_data_practicevcmsummary', 'group_spec_events_Spec_MslsCase',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PracticeVCMSummary.Census12_59MoF'
        raise RuntimeError("Cannot reverse this migration. 'PracticeVCMSummary.Census12_59MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PracticeVCMSummary.Census12_59MoF'
        db.add_column(u'source_data_practicevcmsummary', 'Census12_59MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'PracticeVCMSummary.submissiondate'
        db.delete_column(u'source_data_practicevcmsummary', 'submissiondate')

        # Deleting field 'PracticeVCMSummary.dateofreport'
        db.delete_column(u'source_data_practicevcmsummary', 'dateofreport')

        # Deleting field 'PracticeVCMSummary.date_implement'
        db.delete_column(u'source_data_practicevcmsummary', 'date_implement')

        # Deleting field 'PracticeVCMSummary.settlementcode'
        db.delete_column(u'source_data_practicevcmsummary', 'settlementcode')

        # Deleting field 'PracticeVCMSummary.censusnewbornsf'
        db.delete_column(u'source_data_practicevcmsummary', 'censusnewbornsf')

        # Deleting field 'PracticeVCMSummary.censusnewbornsm'
        db.delete_column(u'source_data_practicevcmsummary', 'censusnewbornsm')

        # Deleting field 'PracticeVCMSummary.census2_11mof'
        db.delete_column(u'source_data_practicevcmsummary', 'census2_11mof')

        # Deleting field 'PracticeVCMSummary.census2_11mom'
        db.delete_column(u'source_data_practicevcmsummary', 'census2_11mom')

        # Deleting field 'PracticeVCMSummary.census12_59mof'
        db.delete_column(u'source_data_practicevcmsummary', 'census12_59mof')

        # Deleting field 'PracticeVCMSummary.census12_59mom'
        db.delete_column(u'source_data_practicevcmsummary', 'census12_59mom')

        # Deleting field 'PracticeVCMSummary.vaxnewbornsf'
        db.delete_column(u'source_data_practicevcmsummary', 'vaxnewbornsf')

        # Deleting field 'PracticeVCMSummary.vaxnewbornsm'
        db.delete_column(u'source_data_practicevcmsummary', 'vaxnewbornsm')

        # Deleting field 'PracticeVCMSummary.vax2_11mof'
        db.delete_column(u'source_data_practicevcmsummary', 'vax2_11mof')

        # Deleting field 'PracticeVCMSummary.vax2_11mom'
        db.delete_column(u'source_data_practicevcmsummary', 'vax2_11mom')

        # Deleting field 'PracticeVCMSummary.vax12_59mof'
        db.delete_column(u'source_data_practicevcmsummary', 'vax12_59mof')

        # Deleting field 'PracticeVCMSummary.vax12_59mom'
        db.delete_column(u'source_data_practicevcmsummary', 'vax12_59mom')

        # Deleting field 'PracticeVCMSummary.msd_grp_choice'
        db.delete_column(u'source_data_practicevcmsummary', 'msd_grp_choice')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_playgroundf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_playgroundf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_playgroundm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_playgroundm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_soceventf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_soceventf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_soceventm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_soceventm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_marketf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_marketf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_marketm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_marketm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_farmf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_farmf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_farmm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_farmm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_schoolf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_schoolf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_schoolm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_schoolm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_childsickf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childsickf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_childsickm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childsickm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_sideeffectsf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_sideeffectsf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_sideeffectsm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_sideeffectsm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_nofeltneedf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nofeltneedf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_nofeltneedm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nofeltneedm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_toomanyroundsf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_toomanyroundsf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_toomanyroundsm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_toomanyroundsm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_relbeliefsf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_relbeliefsf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_relbeliefsm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_relbeliefsm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_poldiffsf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poldiffsf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_poldiffsm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poldiffsm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_unhappywteamf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_unhappywteamf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_unhappywteamm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_unhappywteamm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_noplusesf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noplusesf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_noplusesm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noplusesm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_nogovtservicesf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nogovtservicesf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_nogovtservicesm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_nogovtservicesm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_poliouncommonf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliouncommonf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_poliouncommonm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliouncommonm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_poliohascuref'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliohascuref')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_poliohascurem'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_poliohascurem')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_otherprotectionf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_otherprotectionf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_otherprotectionm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_otherprotectionm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_noconsentf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noconsentf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_noconsentm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noconsentm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_hhnotvisitedf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_hhnotvisitedf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_hhnotvisitedm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_hhnotvisitedm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_noreasonf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noreasonf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_noreasonm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_noreasonm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_securityf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_securityf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_securitym'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_securitym')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_agedoutf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_agedoutf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_agedoutm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_agedoutm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_familymovedf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_familymovedf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_familymovedm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_familymovedm')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_childdiedf'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childdiedf')

        # Deleting field 'PracticeVCMSummary.group_msd_chd_msd_childdiedm'
        db.delete_column(u'source_data_practicevcmsummary', 'group_msd_chd_msd_childdiedm')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_zerodose'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_zerodose')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_pregnantmother'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_pregnantmother')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_newborn'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_newborn')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_vcmattendedncer'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_vcmattendedncer')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_cmamreferral'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_cmamreferral')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_rireferral'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_rireferral')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_afpcase'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_afpcase')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_mslscase'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_mslscase')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_otherdisease'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_otherdisease')

        # Deleting field 'PracticeVCMSummary.group_spec_events_spec_fic'
        db.delete_column(u'source_data_practicevcmsummary', 'group_spec_events_spec_fic')

        # Deleting field 'PracticeVCMSummary.meta_instanceid'
        db.delete_column(u'source_data_practicevcmsummary', 'meta_instanceid')

        # Deleting field 'PracticeVCMSummary.key'
        db.delete_column(u'source_data_practicevcmsummary', 'key')


    models = {
        'source_data.activityreport': {
            'Meta': {'object_name': 'ActivityReport'},
            'activity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_attendance': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_hh_pending_issues': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_iec': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_local_leadership_present': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_num_hh_affected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_num_vaccinated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_pro_opv_cd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cd_resolved': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_attendance': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_iec': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_caregiver_issues': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_husband_issues': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_positive': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_num_vaccinated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_vcm_present': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cm_vcm_sett': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'daterecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'names': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'Meta': {'object_name': 'HealthCamp'},
            'agencyname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'appropriate_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clinician1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clinician2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'crowdcontroller': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'daterecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'endtime': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'formhub_uuid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_photo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hc_stockout': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'megaphone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'settlementgps_accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementgps_longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settlementname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'townannouncer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.knowthepeople': {
            'Meta': {'object_name': 'KnowThePeople'},
            'brothers': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'citiesvisited': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'dob': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nameofpax': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prefferedcity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sisters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state_country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'source_data.paxlistreporttraining': {
            'Meta': {'object_name': 'PaxListReportTraining'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'emailaddr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nameofparticipant': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'Meta': {'object_name': 'PracticeVCMBirthRecord'},
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
        'source_data.practicevcmsettcoordinates': {
            'Meta': {'object_name': 'PracticeVCMSettCoordinates'},
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
        'source_data.practicevcmsummary': {
            'Meta': {'object_name': 'PracticeVCMSummary'},
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
            'Meta': {'object_name': 'VWSRegister'},
            'acceptphoneresponsibility': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            'datephonecollected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fname_vws': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lname_vws': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'personal_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'simserial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'submissiondate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wardcode': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['source_data']