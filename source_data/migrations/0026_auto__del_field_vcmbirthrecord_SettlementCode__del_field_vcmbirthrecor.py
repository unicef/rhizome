# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'VCMBirthRecord.SettlementCode'
        db.delete_column(u'source_data_vcmbirthrecord', 'SettlementCode')

        # Deleting field 'VCMBirthRecord.HouseHoldNumber'
        db.delete_column(u'source_data_vcmbirthrecord', 'HouseHoldNumber')

        # Deleting field 'VCMBirthRecord.VCMRILink'
        db.delete_column(u'source_data_vcmbirthrecord', 'VCMRILink')

        # Deleting field 'VCMBirthRecord.NameOfChild'
        db.delete_column(u'source_data_vcmbirthrecord', 'NameOfChild')

        # Deleting field 'VCMBirthRecord.DOB'
        db.delete_column(u'source_data_vcmbirthrecord', 'DOB')

        # Deleting field 'VCMBirthRecord.VCMNameCAttended'
        db.delete_column(u'source_data_vcmbirthrecord', 'VCMNameCAttended')

        # Deleting field 'VCMBirthRecord.meta_instanceID'
        db.delete_column(u'source_data_vcmbirthrecord', 'meta_instanceID')

        # Deleting field 'VCMBirthRecord.VCM0Dose'
        db.delete_column(u'source_data_vcmbirthrecord', 'VCM0Dose')

        # Deleting field 'VCMBirthRecord.SubmissionDate'
        db.delete_column(u'source_data_vcmbirthrecord', 'SubmissionDate')

        # Deleting field 'VCMBirthRecord.DateOfReport'
        db.delete_column(u'source_data_vcmbirthrecord', 'DateOfReport')

        # Deleting field 'VCMBirthRecord.KEY'
        db.delete_column(u'source_data_vcmbirthrecord', 'KEY')

        # Deleting field 'VCMBirthRecord.DateReport'
        db.delete_column(u'source_data_vcmbirthrecord', 'DateReport')

        # Adding field 'VCMBirthRecord.submissiondate'
        db.add_column(u'source_data_vcmbirthrecord', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.dateofreport'
        db.add_column(u'source_data_vcmbirthrecord', 'dateofreport',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.datereport'
        db.add_column(u'source_data_vcmbirthrecord', 'datereport',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.settlementcode'
        db.add_column(u'source_data_vcmbirthrecord', 'settlementcode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.householdnumber'
        db.add_column(u'source_data_vcmbirthrecord', 'householdnumber',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.dob'
        db.add_column(u'source_data_vcmbirthrecord', 'dob',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.nameofchild'
        db.add_column(u'source_data_vcmbirthrecord', 'nameofchild',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.vcm0dose'
        db.add_column(u'source_data_vcmbirthrecord', 'vcm0dose',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.vcmrilink'
        db.add_column(u'source_data_vcmbirthrecord', 'vcmrilink',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.vcmnamecattended'
        db.add_column(u'source_data_vcmbirthrecord', 'vcmnamecattended',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.meta_instanceid'
        db.add_column(u'source_data_vcmbirthrecord', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMBirthRecord.key'
        db.add_column(u'source_data_vcmbirthrecord', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)

        # Deleting field 'VCMSummaryNew.Tot_2_11Months'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_2_11Months')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_AgedOutM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_AgedOutM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_RelBeliefsF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_RelBeliefsF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_AgedOutF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_AgedOutF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_RelBeliefsM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_RelBeliefsM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SideEffectsF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SideEffectsF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SideEffectsM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SideEffectsM')

        # Deleting field 'VCMSummaryNew.CensusNewBornsF'
        db.delete_column(u'source_data_vcmsummarynew', 'CensusNewBornsF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SocEventM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SocEventM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_UnhappyWTeamM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_UnhappyWTeamM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoPlusesF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoPlusesF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoFeltNeedF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoFeltNeedF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SocEventF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SocEventF')

        # Deleting field 'VCMSummaryNew.CensusNewBornsM'
        db.delete_column(u'source_data_vcmsummarynew', 'CensusNewBornsM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoFeltNeedM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoFeltNeedM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_UnhappyWTeamF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_UnhappyWTeamF')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_AFPCase'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_AFPCase')

        # Deleting field 'VCMSummaryNew.Census2_11MoM'
        db.delete_column(u'source_data_vcmsummarynew', 'Census2_11MoM')

        # Deleting field 'VCMSummaryNew.Census2_11MoF'
        db.delete_column(u'source_data_vcmsummarynew', 'Census2_11MoF')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_OtherDisease'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_OtherDisease')

        # Deleting field 'VCMSummaryNew.Date_Implement'
        db.delete_column(u'source_data_vcmsummarynew', 'Date_Implement')

        # Deleting field 'VCMSummaryNew.meta_instanceID'
        db.delete_column(u'source_data_vcmsummarynew', 'meta_instanceID')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoGovtServicesM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Tot_Missed_Check'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Tot_Missed_Check')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoGovtServicesF')

        # Deleting field 'VCMSummaryNew.Tot_Newborns'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_Newborns')

        # Deleting field 'VCMSummaryNew.Tot_Vax12_59Mo'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_Vax12_59Mo')

        # Deleting field 'VCMSummaryNew.Vax12_59MoM'
        db.delete_column(u'source_data_vcmsummarynew', 'Vax12_59MoM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SchoolF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SchoolF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SchoolM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SchoolM')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_VCMAttendedNCer'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_VCMAttendedNCer')

        # Deleting field 'VCMSummaryNew.Vax2_11MoF'
        db.delete_column(u'source_data_vcmsummarynew', 'Vax2_11MoF')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_PregnantMother'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_PregnantMother')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PlaygroundM')

        # Deleting field 'VCMSummaryNew.Vax2_11MoM'
        db.delete_column(u'source_data_vcmsummarynew', 'Vax2_11MoM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PlaygroundF')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_RIReferral'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_RIReferral')

        # Deleting field 'VCMSummaryNew.SubmissionDate'
        db.delete_column(u'source_data_vcmsummarynew', 'SubmissionDate')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_OtherProtectionF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_OtherProtectionM')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_Newborn'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_Newborn')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_ZeroDose'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_ZeroDose')

        # Deleting field 'VCMSummaryNew.Tot_Vax2_11Mo'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_Vax2_11Mo')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_CMAMReferral'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_CMAMReferral')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SecurityM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SecurityM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_SecurityF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SecurityF')

        # Deleting field 'VCMSummaryNew.Tot_Missed'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_Missed')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_TooManyRoundsF')

        # Deleting field 'VCMSummaryNew.Tot_Vax'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_Vax')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_TooManyRoundsM')

        # Deleting field 'VCMSummaryNew.KEY'
        db.delete_column(u'source_data_vcmsummarynew', 'KEY')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_FIC'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_FIC')

        # Deleting field 'VCMSummaryNew.Vax12_59MoF'
        db.delete_column(u'source_data_vcmsummarynew', 'Vax12_59MoF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_MarketM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_MarketM')

        # Deleting field 'VCMSummaryNew.Tot_Census'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_Census')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_MarketF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_MarketF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_HHNotVisitedF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_HHNotVisitedM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoConsentM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoConsentM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioUncommonM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildDiedF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolDiffsM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioUncommonF')

        # Deleting field 'VCMSummaryNew.Tot_VaxNewBorn'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_VaxNewBorn')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolDiffsF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildDiedM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoPlusesM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoPlusesM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_FarmM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FarmM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_FarmF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FarmF')

        # Deleting field 'VCMSummaryNew.SettlementCode'
        db.delete_column(u'source_data_vcmsummarynew', 'SettlementCode')

        # Deleting field 'VCMSummaryNew.VaxNewBornsM'
        db.delete_column(u'source_data_vcmsummarynew', 'VaxNewBornsM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FamilyMovedF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FamilyMovedM')

        # Deleting field 'VCMSummaryNew.VaxNewBornsF'
        db.delete_column(u'source_data_vcmsummarynew', 'VaxNewBornsF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_NoConsentF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoConsentF')

        # Deleting field 'VCMSummaryNew.Tot_12_59Months'
        db.delete_column(u'source_data_vcmsummarynew', 'Tot_12_59Months')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioHasCureM')

        # Deleting field 'VCMSummaryNew.Census12_59MoM'
        db.delete_column(u'source_data_vcmsummarynew', 'Census12_59MoM')

        # Deleting field 'VCMSummaryNew.DateOfReport'
        db.delete_column(u'source_data_vcmsummarynew', 'DateOfReport')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_ChildSickM'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildSickM')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioHasCureF')

        # Deleting field 'VCMSummaryNew.group_msd_chd_Msd_ChildSickF'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildSickF')

        # Deleting field 'VCMSummaryNew.group_spec_events_Spec_MslsCase'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_MslsCase')

        # Deleting field 'VCMSummaryNew.Census12_59MoF'
        db.delete_column(u'source_data_vcmsummarynew', 'Census12_59MoF')

        # Adding field 'VCMSummaryNew.submissiondate'
        db.add_column(u'source_data_vcmsummarynew', 'submissiondate',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.dateofreport'
        db.add_column(u'source_data_vcmsummarynew', 'dateofreport',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.date_implement'
        db.add_column(u'source_data_vcmsummarynew', 'date_implement',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.settlementcode'
        db.add_column(u'source_data_vcmsummarynew', 'settlementcode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.censusnewbornsf'
        db.add_column(u'source_data_vcmsummarynew', 'censusnewbornsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.censusnewbornsm'
        db.add_column(u'source_data_vcmsummarynew', 'censusnewbornsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_newborns'
        db.add_column(u'source_data_vcmsummarynew', 'tot_newborns',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.census2_11mof'
        db.add_column(u'source_data_vcmsummarynew', 'census2_11mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.census2_11mom'
        db.add_column(u'source_data_vcmsummarynew', 'census2_11mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_2_11months'
        db.add_column(u'source_data_vcmsummarynew', 'tot_2_11months',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.census12_59mof'
        db.add_column(u'source_data_vcmsummarynew', 'census12_59mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.census12_59mom'
        db.add_column(u'source_data_vcmsummarynew', 'census12_59mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_12_59months'
        db.add_column(u'source_data_vcmsummarynew', 'tot_12_59months',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_census'
        db.add_column(u'source_data_vcmsummarynew', 'tot_census',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.vaxnewbornsf'
        db.add_column(u'source_data_vcmsummarynew', 'vaxnewbornsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.vaxnewbornsm'
        db.add_column(u'source_data_vcmsummarynew', 'vaxnewbornsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_vaxnewborn'
        db.add_column(u'source_data_vcmsummarynew', 'tot_vaxnewborn',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.vax2_11mof'
        db.add_column(u'source_data_vcmsummarynew', 'vax2_11mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.vax2_11mom'
        db.add_column(u'source_data_vcmsummarynew', 'vax2_11mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_vax2_11mo'
        db.add_column(u'source_data_vcmsummarynew', 'tot_vax2_11mo',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.vax12_59mof'
        db.add_column(u'source_data_vcmsummarynew', 'vax12_59mof',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.vax12_59mom'
        db.add_column(u'source_data_vcmsummarynew', 'vax12_59mom',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_vax12_59mo'
        db.add_column(u'source_data_vcmsummarynew', 'tot_vax12_59mo',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_vax'
        db.add_column(u'source_data_vcmsummarynew', 'tot_vax',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.tot_missed'
        db.add_column(u'source_data_vcmsummarynew', 'tot_missed',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_playgroundf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_playgroundf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_playgroundm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_playgroundm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_soceventf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_soceventf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_soceventm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_soceventm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_marketf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_marketf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_marketm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_marketm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_farmf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_farmf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_farmm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_farmm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_schoolf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_schoolf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_schoolm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_schoolm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_childsickf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childsickf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_childsickm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childsickm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_sideeffectsf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_sideeffectsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_sideeffectsm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_sideeffectsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_nofeltneedf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nofeltneedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_nofeltneedm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nofeltneedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_toomanyroundsf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_toomanyroundsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_toomanyroundsm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_toomanyroundsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_relbeliefsf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_relbeliefsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_relbeliefsm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_relbeliefsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_poldiffsf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poldiffsf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_poldiffsm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poldiffsm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_unhappywteamf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_unhappywteamf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_unhappywteamm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_unhappywteamm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_noplusesf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noplusesf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_noplusesm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noplusesm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_nogovtservicesf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nogovtservicesf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_nogovtservicesm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nogovtservicesm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_poliouncommonf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliouncommonf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_poliouncommonm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliouncommonm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_poliohascuref'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliohascuref',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_poliohascurem'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliohascurem',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_otherprotectionf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_otherprotectionf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_otherprotectionm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_otherprotectionm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_noconsentf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noconsentf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_noconsentm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noconsentm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_hhnotvisitedf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_hhnotvisitedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_hhnotvisitedm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_hhnotvisitedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_securityf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_securityf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_securitym'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_securitym',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_agedoutf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_agedoutf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_agedoutm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_agedoutm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_familymovedf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_familymovedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_familymovedm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_familymovedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_childdiedf'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childdiedf',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_msd_childdiedm'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childdiedm',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_tot_missed_check'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_tot_missed_check',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_zerodose'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_zerodose',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_pregnantmother'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_pregnantmother',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_newborn'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_newborn',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_vcmattendedncer'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_vcmattendedncer',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_cmamreferral'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_cmamreferral',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_rireferral'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_rireferral',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_afpcase'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_afpcase',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_mslscase'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_mslscase',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_otherdisease'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_otherdisease',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_spec_events_spec_fic'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_fic',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.meta_instanceid'
        db.add_column(u'source_data_vcmsummarynew', 'meta_instanceid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.key'
        db.add_column(u'source_data_vcmsummarynew', 'key',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=255),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.SettlementCode'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.SettlementCode' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.SettlementCode'
        db.add_column(u'source_data_vcmbirthrecord', 'SettlementCode',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.HouseHoldNumber'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.HouseHoldNumber' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.HouseHoldNumber'
        db.add_column(u'source_data_vcmbirthrecord', 'HouseHoldNumber',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.VCMRILink'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.VCMRILink' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.VCMRILink'
        db.add_column(u'source_data_vcmbirthrecord', 'VCMRILink',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.NameOfChild'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.NameOfChild' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.NameOfChild'
        db.add_column(u'source_data_vcmbirthrecord', 'NameOfChild',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.DOB'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.DOB' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.DOB'
        db.add_column(u'source_data_vcmbirthrecord', 'DOB',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.VCMNameCAttended'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.VCMNameCAttended' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.VCMNameCAttended'
        db.add_column(u'source_data_vcmbirthrecord', 'VCMNameCAttended',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.meta_instanceID'
        db.add_column(u'source_data_vcmbirthrecord', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.VCM0Dose'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.VCM0Dose' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.VCM0Dose'
        db.add_column(u'source_data_vcmbirthrecord', 'VCM0Dose',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.SubmissionDate'
        db.add_column(u'source_data_vcmbirthrecord', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.DateOfReport'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.DateOfReport' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.DateOfReport'
        db.add_column(u'source_data_vcmbirthrecord', 'DateOfReport',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.KEY'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.KEY'
        db.add_column(u'source_data_vcmbirthrecord', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMBirthRecord.DateReport'
        raise RuntimeError("Cannot reverse this migration. 'VCMBirthRecord.DateReport' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMBirthRecord.DateReport'
        db.add_column(u'source_data_vcmbirthrecord', 'DateReport',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'VCMBirthRecord.submissiondate'
        db.delete_column(u'source_data_vcmbirthrecord', 'submissiondate')

        # Deleting field 'VCMBirthRecord.dateofreport'
        db.delete_column(u'source_data_vcmbirthrecord', 'dateofreport')

        # Deleting field 'VCMBirthRecord.datereport'
        db.delete_column(u'source_data_vcmbirthrecord', 'datereport')

        # Deleting field 'VCMBirthRecord.settlementcode'
        db.delete_column(u'source_data_vcmbirthrecord', 'settlementcode')

        # Deleting field 'VCMBirthRecord.householdnumber'
        db.delete_column(u'source_data_vcmbirthrecord', 'householdnumber')

        # Deleting field 'VCMBirthRecord.dob'
        db.delete_column(u'source_data_vcmbirthrecord', 'dob')

        # Deleting field 'VCMBirthRecord.nameofchild'
        db.delete_column(u'source_data_vcmbirthrecord', 'nameofchild')

        # Deleting field 'VCMBirthRecord.vcm0dose'
        db.delete_column(u'source_data_vcmbirthrecord', 'vcm0dose')

        # Deleting field 'VCMBirthRecord.vcmrilink'
        db.delete_column(u'source_data_vcmbirthrecord', 'vcmrilink')

        # Deleting field 'VCMBirthRecord.vcmnamecattended'
        db.delete_column(u'source_data_vcmbirthrecord', 'vcmnamecattended')

        # Deleting field 'VCMBirthRecord.meta_instanceid'
        db.delete_column(u'source_data_vcmbirthrecord', 'meta_instanceid')

        # Deleting field 'VCMBirthRecord.key'
        db.delete_column(u'source_data_vcmbirthrecord', 'key')

        # Adding field 'VCMSummaryNew.Tot_2_11Months'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_2_11Months',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_AgedOutM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_AgedOutM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_RelBeliefsF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_RelBeliefsF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_AgedOutF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_AgedOutF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_RelBeliefsM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_RelBeliefsM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SideEffectsF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SideEffectsF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SideEffectsM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SideEffectsM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.CensusNewBornsF'
        db.add_column(u'source_data_vcmsummarynew', 'CensusNewBornsF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SocEventM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SocEventM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_UnhappyWTeamM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_UnhappyWTeamM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoPlusesF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoPlusesF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoFeltNeedF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoFeltNeedF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SocEventF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SocEventF',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.CensusNewBornsM'
        db.add_column(u'source_data_vcmsummarynew', 'CensusNewBornsM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoFeltNeedM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoFeltNeedM',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_UnhappyWTeamF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_UnhappyWTeamF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_UnhappyWTeamF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_UnhappyWTeamF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_AFPCase'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_AFPCase' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_AFPCase'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_AFPCase',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Census2_11MoM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Census2_11MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Census2_11MoM'
        db.add_column(u'source_data_vcmsummarynew', 'Census2_11MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Census2_11MoF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Census2_11MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Census2_11MoF'
        db.add_column(u'source_data_vcmsummarynew', 'Census2_11MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_OtherDisease'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_OtherDisease' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_OtherDisease'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_OtherDisease',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Date_Implement'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Date_Implement' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Date_Implement'
        db.add_column(u'source_data_vcmsummarynew', 'Date_Implement',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.meta_instanceID'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.meta_instanceID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.meta_instanceID'
        db.add_column(u'source_data_vcmsummarynew', 'meta_instanceID',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoGovtServicesM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Tot_Missed_Check'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Tot_Missed_Check' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Tot_Missed_Check'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Tot_Missed_Check',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoGovtServicesF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoGovtServicesF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_Newborns'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_Newborns' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_Newborns'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_Newborns',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_Vax12_59Mo'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_Vax12_59Mo' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_Vax12_59Mo'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_Vax12_59Mo',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Vax12_59MoM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Vax12_59MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Vax12_59MoM'
        db.add_column(u'source_data_vcmsummarynew', 'Vax12_59MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_SchoolF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_SchoolF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SchoolF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SchoolF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_SchoolM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_SchoolM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SchoolM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SchoolM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_VCMAttendedNCer'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_VCMAttendedNCer' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_VCMAttendedNCer'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_VCMAttendedNCer',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Vax2_11MoF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Vax2_11MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Vax2_11MoF'
        db.add_column(u'source_data_vcmsummarynew', 'Vax2_11MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_PregnantMother'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_PregnantMother' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_PregnantMother'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_PregnantMother',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PlaygroundM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Vax2_11MoM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Vax2_11MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Vax2_11MoM'
        db.add_column(u'source_data_vcmsummarynew', 'Vax2_11MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PlaygroundF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PlaygroundF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_RIReferral'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_RIReferral' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_RIReferral'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_RIReferral',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.SubmissionDate'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.SubmissionDate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.SubmissionDate'
        db.add_column(u'source_data_vcmsummarynew', 'SubmissionDate',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_OtherProtectionF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_OtherProtectionM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_OtherProtectionM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_Newborn'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_Newborn' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_Newborn'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_Newborn',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_ZeroDose'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_ZeroDose' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_ZeroDose'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_ZeroDose',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_Vax2_11Mo'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_Vax2_11Mo' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_Vax2_11Mo'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_Vax2_11Mo',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_CMAMReferral'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_CMAMReferral' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_CMAMReferral'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_CMAMReferral',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_SecurityM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_SecurityM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SecurityM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SecurityM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_SecurityF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_SecurityF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_SecurityF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_SecurityF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_Missed'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_Missed' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_Missed'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_Missed',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_TooManyRoundsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_Vax'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_Vax' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_Vax'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_Vax',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_TooManyRoundsM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_TooManyRoundsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.KEY'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.KEY' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.KEY'
        db.add_column(u'source_data_vcmsummarynew', 'KEY',
                      self.gf('django.db.models.fields.CharField')(max_length=255, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_FIC'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_FIC' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_FIC'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_FIC',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Vax12_59MoF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Vax12_59MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Vax12_59MoF'
        db.add_column(u'source_data_vcmsummarynew', 'Vax12_59MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_MarketM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_MarketM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_MarketM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_MarketM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_Census'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_Census' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_Census'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_Census',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_MarketF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_MarketF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_MarketF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_MarketF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_HHNotVisitedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_HHNotVisitedM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_HHNotVisitedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_NoConsentM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_NoConsentM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoConsentM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoConsentM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioUncommonM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildDiedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolDiffsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PolioUncommonF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioUncommonF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_VaxNewBorn'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_VaxNewBorn' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_VaxNewBorn'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_VaxNewBorn',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PolDiffsF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolDiffsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_ChildDiedM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildDiedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_NoPlusesM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_NoPlusesM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoPlusesM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoPlusesM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_FarmM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_FarmM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_FarmM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FarmM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_FarmF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_FarmF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_FarmF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FarmF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.SettlementCode'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.SettlementCode' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.SettlementCode'
        db.add_column(u'source_data_vcmsummarynew', 'SettlementCode',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.VaxNewBornsM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.VaxNewBornsM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.VaxNewBornsM'
        db.add_column(u'source_data_vcmsummarynew', 'VaxNewBornsM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FamilyMovedF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_FamilyMovedM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_FamilyMovedM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.VaxNewBornsF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.VaxNewBornsF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.VaxNewBornsF'
        db.add_column(u'source_data_vcmsummarynew', 'VaxNewBornsF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_NoConsentF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_NoConsentF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_NoConsentF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_NoConsentF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Tot_12_59Months'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Tot_12_59Months' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Tot_12_59Months'
        db.add_column(u'source_data_vcmsummarynew', 'Tot_12_59Months',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioHasCureM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Census12_59MoM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Census12_59MoM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Census12_59MoM'
        db.add_column(u'source_data_vcmsummarynew', 'Census12_59MoM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.DateOfReport'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.DateOfReport' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.DateOfReport'
        db.add_column(u'source_data_vcmsummarynew', 'DateOfReport',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_ChildSickM'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_ChildSickM' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_ChildSickM'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildSickM',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_PolioHasCureF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_PolioHasCureF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_msd_chd_Msd_ChildSickF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_msd_chd_Msd_ChildSickF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_msd_chd_Msd_ChildSickF'
        db.add_column(u'source_data_vcmsummarynew', 'group_msd_chd_Msd_ChildSickF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.group_spec_events_Spec_MslsCase'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.group_spec_events_Spec_MslsCase' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.group_spec_events_Spec_MslsCase'
        db.add_column(u'source_data_vcmsummarynew', 'group_spec_events_Spec_MslsCase',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VCMSummaryNew.Census12_59MoF'
        raise RuntimeError("Cannot reverse this migration. 'VCMSummaryNew.Census12_59MoF' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VCMSummaryNew.Census12_59MoF'
        db.add_column(u'source_data_vcmsummarynew', 'Census12_59MoF',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Deleting field 'VCMSummaryNew.submissiondate'
        db.delete_column(u'source_data_vcmsummarynew', 'submissiondate')

        # Deleting field 'VCMSummaryNew.dateofreport'
        db.delete_column(u'source_data_vcmsummarynew', 'dateofreport')

        # Deleting field 'VCMSummaryNew.date_implement'
        db.delete_column(u'source_data_vcmsummarynew', 'date_implement')

        # Deleting field 'VCMSummaryNew.settlementcode'
        db.delete_column(u'source_data_vcmsummarynew', 'settlementcode')

        # Deleting field 'VCMSummaryNew.censusnewbornsf'
        db.delete_column(u'source_data_vcmsummarynew', 'censusnewbornsf')

        # Deleting field 'VCMSummaryNew.censusnewbornsm'
        db.delete_column(u'source_data_vcmsummarynew', 'censusnewbornsm')

        # Deleting field 'VCMSummaryNew.tot_newborns'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_newborns')

        # Deleting field 'VCMSummaryNew.census2_11mof'
        db.delete_column(u'source_data_vcmsummarynew', 'census2_11mof')

        # Deleting field 'VCMSummaryNew.census2_11mom'
        db.delete_column(u'source_data_vcmsummarynew', 'census2_11mom')

        # Deleting field 'VCMSummaryNew.tot_2_11months'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_2_11months')

        # Deleting field 'VCMSummaryNew.census12_59mof'
        db.delete_column(u'source_data_vcmsummarynew', 'census12_59mof')

        # Deleting field 'VCMSummaryNew.census12_59mom'
        db.delete_column(u'source_data_vcmsummarynew', 'census12_59mom')

        # Deleting field 'VCMSummaryNew.tot_12_59months'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_12_59months')

        # Deleting field 'VCMSummaryNew.tot_census'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_census')

        # Deleting field 'VCMSummaryNew.vaxnewbornsf'
        db.delete_column(u'source_data_vcmsummarynew', 'vaxnewbornsf')

        # Deleting field 'VCMSummaryNew.vaxnewbornsm'
        db.delete_column(u'source_data_vcmsummarynew', 'vaxnewbornsm')

        # Deleting field 'VCMSummaryNew.tot_vaxnewborn'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_vaxnewborn')

        # Deleting field 'VCMSummaryNew.vax2_11mof'
        db.delete_column(u'source_data_vcmsummarynew', 'vax2_11mof')

        # Deleting field 'VCMSummaryNew.vax2_11mom'
        db.delete_column(u'source_data_vcmsummarynew', 'vax2_11mom')

        # Deleting field 'VCMSummaryNew.tot_vax2_11mo'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_vax2_11mo')

        # Deleting field 'VCMSummaryNew.vax12_59mof'
        db.delete_column(u'source_data_vcmsummarynew', 'vax12_59mof')

        # Deleting field 'VCMSummaryNew.vax12_59mom'
        db.delete_column(u'source_data_vcmsummarynew', 'vax12_59mom')

        # Deleting field 'VCMSummaryNew.tot_vax12_59mo'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_vax12_59mo')

        # Deleting field 'VCMSummaryNew.tot_vax'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_vax')

        # Deleting field 'VCMSummaryNew.tot_missed'
        db.delete_column(u'source_data_vcmsummarynew', 'tot_missed')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_playgroundf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_playgroundf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_playgroundm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_playgroundm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_soceventf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_soceventf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_soceventm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_soceventm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_marketf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_marketf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_marketm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_marketm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_farmf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_farmf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_farmm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_farmm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_schoolf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_schoolf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_schoolm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_schoolm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_childsickf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childsickf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_childsickm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childsickm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_sideeffectsf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_sideeffectsf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_sideeffectsm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_sideeffectsm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_nofeltneedf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nofeltneedf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_nofeltneedm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nofeltneedm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_toomanyroundsf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_toomanyroundsf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_toomanyroundsm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_toomanyroundsm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_relbeliefsf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_relbeliefsf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_relbeliefsm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_relbeliefsm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_poldiffsf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poldiffsf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_poldiffsm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poldiffsm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_unhappywteamf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_unhappywteamf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_unhappywteamm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_unhappywteamm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_noplusesf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noplusesf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_noplusesm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noplusesm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_nogovtservicesf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nogovtservicesf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_nogovtservicesm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_nogovtservicesm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_poliouncommonf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliouncommonf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_poliouncommonm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliouncommonm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_poliohascuref'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliohascuref')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_poliohascurem'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_poliohascurem')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_otherprotectionf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_otherprotectionf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_otherprotectionm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_otherprotectionm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_noconsentf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noconsentf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_noconsentm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_noconsentm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_hhnotvisitedf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_hhnotvisitedf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_hhnotvisitedm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_hhnotvisitedm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_securityf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_securityf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_securitym'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_securitym')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_agedoutf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_agedoutf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_agedoutm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_agedoutm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_familymovedf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_familymovedf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_familymovedm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_familymovedm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_childdiedf'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childdiedf')

        # Deleting field 'VCMSummaryNew.group_msd_chd_msd_childdiedm'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_msd_childdiedm')

        # Deleting field 'VCMSummaryNew.group_msd_chd_tot_missed_check'
        db.delete_column(u'source_data_vcmsummarynew', 'group_msd_chd_tot_missed_check')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_zerodose'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_zerodose')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_pregnantmother'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_pregnantmother')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_newborn'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_newborn')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_vcmattendedncer'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_vcmattendedncer')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_cmamreferral'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_cmamreferral')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_rireferral'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_rireferral')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_afpcase'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_afpcase')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_mslscase'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_mslscase')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_otherdisease'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_otherdisease')

        # Deleting field 'VCMSummaryNew.group_spec_events_spec_fic'
        db.delete_column(u'source_data_vcmsummarynew', 'group_spec_events_spec_fic')

        # Deleting field 'VCMSummaryNew.meta_instanceid'
        db.delete_column(u'source_data_vcmsummarynew', 'meta_instanceid')

        # Deleting field 'VCMSummaryNew.key'
        db.delete_column(u'source_data_vcmsummarynew', 'key')


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
            'DateRecorded': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'ClusterSupervisor'},
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord_rfp_meeting': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord_smwg_meetings': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord_vcm_meeting': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
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
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_LGAC': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ri_supervision': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervisee_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_Accuracy': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_Altitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_Latitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervision_location_Longitude': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'Asset_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Colour_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DeviceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'LGA': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'PhoneInventory'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'State': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SubmissionDate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 11, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_instanceID': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'process_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['source_data.ProcessStatus']"}),
            'request_guid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'Census12_59MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census12_59MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Census2_11MoM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsF': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CensusNewBornsM': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'DateOfReport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Date_Implement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'KEY': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'Meta': {'object_name': 'VCMSummaryOld'},
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