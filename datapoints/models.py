from datetime import datetime

from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords
from jsonfield import JSONField

class CacheJob(models.Model):
    '''
    A table that shows the start/end time of each cache job, as well as the
    response message of the job itself.  This allows a DBA to track what is
    happening with our cache jobs and how long they are taking.
    '''

    date_attempted = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True)
    is_error = models.BooleanField()
    response_msg = models.CharField(max_length=255)

    class Meta:
        db_table = 'cache_job'
        ordering = ('-date_attempted',)


class Indicator(models.Model):
    '''
    The type of data that we are tracing, for instance
     - Number of children missed due to religious regions
     - Number of vaccinators paid on time
     - Number of iVDPV cases
     - Percentage of children missed due to religious regions.

    Note that both calculated and raw indicators are stored in this table.  For
    more information on how indicicators are used to calculated data for more
    indicators take a look at the CalculatedIndicatorComponent model.
    '''

    short_name = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,unique=True)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='name',unique=True,max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'indicator'
        ordering = ('name',)


class IndicatorAbstracted(models.Model):
    '''
    An extended version of the Indicator table which uses the bounds and tags
    associated to each indicator ID in order to manage one table with all of the
    information the API needs for each indicator.

    The transformation between Indicator and IndicatorAbstracted is handled in
    datapoints/cache_tasks.py -> cache_indicator_abstracted()
    '''

    description = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    bound_json = JSONField()
    tag_json = JSONField()

    def __unicode__(self):
        return unicode(self.slug)

    class Meta:
        db_table = 'indicator_abstracted'

class UserAbstracted(models.Model):
    '''
    Similar to the IndicatorAbstcated model, this allows us to store and return
    data associated with each user that is not stored directly in the user
    table, but in tables keyed off user_id ( user_to_group, region_permission).

    The transformation between Indicator and IndicatorAbstracted is handled in
    datapoints/cache_tasks.py -> cache_user_abstracted()

    '''

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.BooleanField()
    email = models.CharField(max_length=255)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    group_json = JSONField()
    region_permission_json = JSONField()

    class Meta:
        db_table = 'user_abstracted'



class CalculatedIndicatorComponent(models.Model):
    '''
    The indicator is for example "pct missed due to refusal," the component
    "total missed" and calculation is "denominator"

    A dba can create new calculations by inserting rows here.  The cache_refresh
    job that happens every minute will take these new indicator definitions and
    use these values to calucate data for the new calculated indicators.

    Notice however that calculations are multi layered, for instance certain
    percentage calculations, use an indicator that is calculated from the sum
    of a set of other indicators as it's denominator.  This means, that the
    order in which we calculated datapoitns matters.  For more on how this works
    check out the fn_calc_datapoint() stored procedure.
    '''

    indicator = models.ForeignKey(Indicator, related_name='indicator_master')
    indicator_component = models.ForeignKey(Indicator,related_name='indicator_component')
    calculation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.indicator.name)

    class Meta:
        db_table = 'calculated_indicator_component'

class IndicatorBound(models.Model):
    '''
    If a Low / High reporesents an error, or a particular grouping of values
    i.e. (good, ok, bad) we have how ever many rows for an indicator as their
    are groupings for that indicator's values.
    '''

    indicator = models.ForeignKey(Indicator)
    mn_val = models.FloatField(null=True)
    mx_val = models.FloatField(null=True)
    bound_name = models.CharField(max_length=255)
    direction = models.IntegerField(default=1)


    def __unicode__(self):
        return unicode(self.bound_name.name)

    class Meta:
        db_table = 'indicator_bound'

class IndicatorTag(models.Model):
    '''
    The list of tags that can be associated to an indicator.  For instance:
        - ODK indicators
        - WHO independent monitoring
        - Management Dashbaord Indicators

    These are stored in a heirarchy so we can build a tree on the indicator drop
    down which gives the user a nicer, more organized breakdown of the
    indicators available to the system.
    '''

    tag_name = models.CharField(max_length=255)
    parent_tag = models.ForeignKey("self",null=True)

    class Meta:
        db_table = 'indicator_tag'

class IndicatorToTag(models.Model):
    '''
    Tagging an indicator. One indicator can have many tags.
    '''

    indicator = models.ForeignKey(Indicator)
    indicator_tag = models.ForeignKey(IndicatorTag)

    class Meta:
        db_table = 'indicator_to_tag'
        unique_together = ('indicator','indicator_tag')
        ordering = [('-id')]

class Office(models.Model):
    '''
    Unless there are any other outbreaks of Polio, this list will remain
    Nigeria, Pakistan, and Nigeria.

    Both regions and campaigns are associated with offices.  This is helpful
    because often, bad mappings, or bad data in general lead us having
    datapoints with a campaign/region combination that do not have the same
    office.  Having this ID in both of these tables makes bad data much easier
    to find.
    '''

    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'office'

        permissions = (
            ('view_office', 'View office'),
        )

class RegionType(models.Model):
    '''
    Country, Province, District, Sub-District, Settlement.

    While each country has it's own nomenclature for the different levels of
    the regional heirarchy ( i.e. Nigeria calls Districts LGAs ) the region
    type table allows us to assocaite a region_type key to each region.

    For our purpose the 5 region types are the definitive types of regions that
    the system supports.
    '''

    name = models.CharField(max_length=55, unique=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'region_type'

class Region(models.Model):
    '''
    A point in space with a name, region_code, office_id, lat/lon, and parent
    region id.  The parent region id is used to create the tree used to create
    aggregate statistics based on the information stored at the leaf leve.
    '''


    name = models.CharField(max_length=255,unique=True)
    region_code = models.CharField(max_length=255, unique=True)
    region_type = models.ForeignKey(RegionType)
    office = models.ForeignKey(Office)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    slug = AutoSlugField(populate_from='name',max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now=True)
    parent_region = models.ForeignKey("self",null=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:

        db_table = 'region'
        unique_together = ('name','region_type','office')


class RegionPolygon(models.Model):
    '''
    A shape file when avaiable for a region.
    '''

    region = models.OneToOneField(Region)
    geo_json = JSONField()

    class Meta:
        db_table = 'region_polygon'


class CampaignType(models.Model):
    '''
    Each campaign must have a campaign_type_id.

    Not really in scope as have only been working with data that come from the
    National Immunization Days.
    '''

    name = models.CharField(max_length=55)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'campaign_type'

class Campaign(models.Model):
    '''
    A period in time in wich a campaign was initaited by the country office.
    '''

    office = models.ForeignKey(Office)
    campaign_type = models.ForeignKey(CampaignType)
    start_date = models.DateField()
    end_date = models.DateField()
    slug = AutoSlugField(populate_from='get_full_name',unique=True)
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.slug)

    def get_full_name(self):
        return unicode(self.office.name + '-' + unicode(self.start_date))

    class Meta:
        db_table = 'campaign'
        ordering = ('-start_date',)
        unique_together = ('office','start_date')

class CampaignAbstracted(models.Model):
    '''
    EVErything in campaign plus the "pct_complete" attribute
    '''

    office = models.ForeignKey(Office)
    campaign_type = models.ForeignKey(CampaignType)
    start_date = models.DateField()
    end_date = models.DateField()
    slug = AutoSlugField(populate_from='get_full_name',unique=True)
    pct_complete = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.slug)

    def get_full_name(self):
        return unicode(self.office.name + '-' + unicode(self.start_date))

    class Meta:
        db_table = 'campaign_abstracted'
        ordering = ('-start_date',)
        unique_together = ('office','start_date')

class DataPoint(models.Model):
    '''
    The core table of the application.  This is where the raw data is stored
    and brought together from data entry, ODK and csv upload.

    Note that this table does not store the aggregated or calculated data, only
    the raw data that we get from the source.

    The source_datapoint_id shows the original source of the data in the
    source_datapoint_table.  The source_datapoint_id is -1 in the case of data
    entry.

    The cache_job_id column allows us to find out when and why a particular
    datapoint was refreshed.  New datapoints have a cache_job_id = -1 which
    tells the system that it needs to be refreshed.
    '''

    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    value = models.FloatField(null=True)
    note = models.CharField(max_length=255,null=True,blank=True)
    changed_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now=True)
    source_submission = models.ForeignKey('source_data.SourceSubmission')
    cache_job = models.ForeignKey(CacheJob,default=-1)


    def get_val(self):
        return self.value

    class Meta:
        db_table = 'datapoint'
        unique_together = ('indicator','region','campaign')
        ordering = ['region', 'campaign']
        permissions = (
            ('view_datapoint', 'View datapoint'),
        )

class DataPointEntry(DataPoint):
    """Proxy subclass of DataPoint, for use only in API
    methods used by the manual data entry form. This model
    stores records of all changes in a separate DB table.
    """

    history = HistoricalRecords()

    class Meta:
        proxy = True


class Responsibility(models.Model):

    user = models.ForeignKey('auth.User')
    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)

    class Meta:
        db_table = 'responsibility'
        ordering = ('indicator',)
        unique_together = ('user','indicator','region')


class DataPointAbstracted(models.Model):

    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    indicator_json = JSONField()
    cache_job = models.ForeignKey(CacheJob,default=-1)

    class Meta:
        db_table = 'datapoint_abstracted'
        unique_together = ('region','campaign')

class DataPointComputed(models.Model):

    region_id = models.IntegerField()
    campaign_id = models.IntegerField()
    indicator_id = models.IntegerField()
    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob,default=-1)

    class Meta:
        db_table = 'datapoint_with_computed'
        unique_together = ('region_id','campaign_id','indicator_id')

class AggDataPoint(models.Model):

    region_id = models.IntegerField()
    campaign_id = models.IntegerField()
    indicator_id = models.IntegerField()
    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob,default=-1)

    class Meta:
        db_table = 'agg_datapoint'
        unique_together = ('region_id','campaign_id','indicator_id')


class ExpectedData(models.Model):

    region = models.ForeignKey(Region,related_name='ex_child_region')
    campaign = models.ForeignKey(Campaign)
    parent_region = models.ForeignKey(Region,related_name='ex_parent_region')

    class Meta:
        db_table = 'expected_data'
        unique_together = ('region','campaign')


class ReconData(models.Model):

    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    indicator = models.ForeignKey(Indicator)
    target_value = models.FloatField()

    class Meta:
        db_table = 'recon_data'
        unique_together = ('region','campaign','indicator')


class BadData(models.Model):

    datapoint = models.ForeignKey(DataPoint)
    document = models.ForeignKey('source_data.Document')
    error_type = models.CharField(max_length=55)
    cache_job = models.ForeignKey(CacheJob)

    class Meta:
        db_table = 'bad_data'


class RegionPermission(models.Model):
    '''
    Individual Users must be assigned regional permissions.  If i am assigned
    a region, I will be able to view all of its children recursively.  The
    default for a user

    Regional permissions must also specify the read/write flag.  So for instance
    as a Cluster Supervisor in Sokoto, I should be able to see all of Nigeria's
    data, but i only should be able to insert / edit data for Sokoto. Thus i
    would have two records, one that says "i can read all of NG", and one that
    says, "i can write data in Sokoto."
    '''

    user = models.ForeignKey('auth.User')
    region = models.ForeignKey(Region)
    read_write = models.CharField(max_length=1)

    class Meta:
        db_table = 'region_permission'
        unique_together = ('user','region','read_write')


class IndicatorPermission(models.Model):
    '''
    All users can read all indicators, but permission to update/insert/delete
    are assigned to a group.  For instance, the security_analyst role, will be
    permitted to edit data on the security indicators, but not for instance
    OPV supply indicators.
    '''

    group = models.ForeignKey('auth.Group')
    indicator = models.ForeignKey(Indicator)

    class Meta:
        db_table = 'indicator_permission'
        unique_together = ('group','indicator')


class UserGroup(models.Model):
    '''
    auth_user_groups is how django handels user group membership by default.
    This class simply allows me to interface with that table without going
    through the djanog admin api.

    Notice the managed=False... this means that django will not try to create
    a migration if this class is created or altered.
    '''

    user = models.ForeignKey('auth.User')
    group = models.ForeignKey('auth.Group')

    class Meta:
        db_table = 'auth_user_groups'
        managed = False


class CustomDashboard(models.Model):
    '''
    A table containing all of the custom dashboards in the system.  The data
    in teh dashboard_json field is how the FE is able to draw and render the
    specific vizulaizations.  If inserted via POST the application will
    validate the json, but if you insert directly in the table it will not
    so be careful when testing!
    '''

    title = models.CharField(max_length=255,unique=True)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey('auth.User')
    default_office = models.ForeignKey(Office,null=True)
    dashboard_json = JSONField(null=True)

    class Meta:
        db_table = 'custom_dashboard'
