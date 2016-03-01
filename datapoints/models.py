from django.db import models

from simple_history.models import HistoricalRecords
from jsonfield import JSONField
from pandas import DataFrame


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
     - Number of children missed due to religious locations
     - Number of vaccinators paid on time
     - Number of iVDPV cases
     - Percentage of children missed due to religious locations.

    Note that both calculated and raw indicators are stored in this table.  For
    more information on how indicicators are used to calculated data for more
    indicators take a look at the CalculatedIndicatorComponent model.
    '''

    short_name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    data_format = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    bound_json = JSONField(default = [])
    tag_json = JSONField(default = [])
    office_id = JSONField(default = [])
    high_bound = models.FloatField(null=True)
    low_bound = models.FloatField(null=True)
    source_name = models.CharField(max_length=25) ## to do: make this a FK

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'indicator'
        ordering = ('name',)


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
    order in which we calculated datapoints matters.  For more on how this works
    check out the fn_calc_datapoint() stored procedure.
    '''

    indicator = models.ForeignKey(Indicator, related_name='indicator_master')
    indicator_component = models.ForeignKey(Indicator, related_name='indicator_component')
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
        return unicode(self.bound_name)

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
    parent_tag = models.ForeignKey("self", null=True)

    def __unicode__(self):
        return unicode(self.tag_name)

    class Meta:
        db_table = 'indicator_tag'

    def get_indicator_ids_for_tag(self):

        df_cols = ['id','parent_tag_id']

        tag_list = list(IndicatorTag.objects.filter(parent_tag_id = self.id)\
            .values_list(*df_cols))

        tag_list.append((self.id, None))

        ind_df = DataFrame(tag_list,columns=df_cols)
        return Indicator.objects.all().values_list('id',flat=True)


class IndicatorToTag(models.Model):
    '''
    Tagging an indicator. One indicator can have many tags.
    '''

    indicator = models.ForeignKey(Indicator)
    indicator_tag = models.ForeignKey(IndicatorTag)

    class Meta:
        db_table = 'indicator_to_tag'
        unique_together = ('indicator', 'indicator_tag')
        ordering = ('-id',)


class Office(models.Model):
    '''
    Unless there are any other outbreaks of Polio, this list will remain
    Nigeria, Pakistan, and Nigeria.

    Both locations and campaigns are associated with offices.  This is helpful
    because often, bad mappings, or bad data in general lead us having
    datapoints with a campaign/location combination that do not have the same
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


class IndicatorToOffice(models.Model):
    '''
    Way to filter indicators in the API without querying the entire DB.  used
    to filter indicators in the chart wizard API so user does not see Indicators
    for which there is no data.
    '''

    indicator = models.ForeignKey(Indicator)
    office = models.ForeignKey(Office)

    class Meta:
        db_table = 'indicator_to_office'


class LocationType(models.Model):
    '''
    Country, Province, District, Sub-District, Settlement.

    While each country has it's own nomenclature for the different levels of
    the locational heirarchy ( i.e. Nigeria calls Districts LGAs ) the location
    type table allows us to assocaite a location_type key to each location.

    For our purpose the 5 location types are the definitive types of locations that
    the system supports.
    '''

    name = models.CharField(max_length=55, unique=True)
    admin_level = models.IntegerField(unique=True)

    def __unicode__(self):
        return unicode(self.name + ' (Admin Level %s)' % self.admin_level)

    class Meta:
        db_table = 'location_type'


class Location(models.Model):
    '''
    A point in space with a name, location_code, office_id, lat/lon, and parent
    location id.  The parent location id is used to create the tree used to create
    aggregate statistics based on the information stored at the leaf leve.
    '''

    name = models.CharField(max_length=255, unique=True)
    location_code = models.CharField(max_length=255, unique=True)
    location_type = models.ForeignKey(LocationType)
    office = models.ForeignKey(Office)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    lpd_status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    parent_location = models.ForeignKey("self", null=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'location'

class LocationTree(models.Model):
    '''
    location tree that is refreshed with "refresh_metadata"

    Nigeria for instance as a parent location, will have ALL children recursively
    stored with the cooresponding level to indicate its depth in the tree.
    '''

    parent_location = models.ForeignKey(Location, related_name='ultimate_parent')
    location = models.ForeignKey(Location)
    lvl = models.IntegerField()

    class Meta:
        db_table = 'location_tree'
        unique_together = ('parent_location', 'location')


class LocationPolygon(models.Model):
    '''
    A shape file when avaiable for a location.
    '''

    location = models.OneToOneField(Location)
    geo_json = JSONField()

    class Meta:
        db_table = 'location_polygon'

class MinGeo(models.Model):
    '''
    Same as above, but with the geo_json minified.  This is a separate table
    ( as opposed to just another column ) so that we can keep this table as
    lightweigght as possible.  This table is populated from the LocationPolygon
    table from the cache_meta process.  We cache this so that we can save
    resources on the request, and still keep the full data of the source shape
    file in LocationPolygon,
    '''

    location = models.OneToOneField(Location)
    geo_json = JSONField()

    class Meta:
        db_table = 'min_polygon'

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
    A grouping of datapoints.  For polio, for we have a "campaign type" of
    "National Immunization Day" or "Mop Up" which means an immeiate response
    to a case by conncentrated vaccination campaigns in that area.

    The campaign thus allows you to model these two things with the model in
    these two instances:

    1. NID - Happens monthly for the Endemics.  We have a certain type of
    Inticators that we want to collect for this.. see "Management Dashboard."

        - indicator_list = Management Dashboard Indicators
        - top_lvl_location = Afghanistan

    2. Mop Up - Could happen anywhere where low immunity, for instance Ukraine.

        - indicator_list = A few select Indicators related to the "mop up"
        effort.  These will be different, put potentially overlapping from the
        NID indicator list.
        - top_lvl_location = Ukraine

    For other efforts, this model can be useful.. For Routine Immunization
    one could imagine a similar setup.

    The campaign model has a method called "get_datapoints", which gets the
    relevant raw and aggregated datapoints for a given campaign.  The data
    is aggregated from the date, indicator_list and location in the AggRefresh.

    The indicator_list, is determined by taking the flatened top lvl indicator
    tree that is for the campaign.
    '''

    name = models.CharField(max_length=255)
    top_lvl_location = models.ForeignKey(Location)
    top_lvl_indicator_tag = models.ForeignKey(IndicatorTag)
    office = models.ForeignKey(Office)
    campaign_type = models.ForeignKey(CampaignType)
    start_date = models.DateField()
    end_date = models.DateField()
    pct_complete = models.FloatField(default=.001)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    def get_datapoints(self):

        return DataPointComputed.objects.filter(campaign_id = self.id).values()

    def get_raw_datapoint_ids(self):

        flat_location_id_list = LocationTree.objects.filter(parent_location_id=\
            self.top_lvl_location_id).values_list('location_id',flat=True)

        # indicator_id_list = CampaignToIndicator.objects.filter(campaign_id = \
        #     self.id).values_list('indicator_id',flat=True)

        qs = DataPoint.objects.filter(
            location_id__in = flat_location_id_list,
            # indicator_id__in = indicator_id_list,
            data_date__lt = self.end_date,
            data_date__gte = self.start_date,
        ).values_list('id',flat=True)

        return qs

    def save(self, **kwargs):

        super(Campaign, self).save(**kwargs)

        top_lvl_tag_obj = IndicatorTag.objects\
            .get(id = self.top_lvl_indicator_tag_id)
        indicator_id_list = top_lvl_tag_obj.get_indicator_ids_for_tag()

        cti_batch = [CampaignToIndicator(**{'campaign_id':self.id,\
            'indicator_id':ind_id}) for ind_id in indicator_id_list ]

        CampaignToIndicator.objects.filter(campaign_id=self.id).delete()
        CampaignToIndicator.objects.bulk_create(cti_batch)

        self.mark_datapoints_as_to_process()

    def mark_datapoints_as_to_process(self):

        dp_ids = self.get_raw_datapoint_ids()
        DataPoint.objects.filter(id__in=dp_ids,cache_job_id = -2
            ).update(cache_job_id = -1)


    class Meta:
        db_table = 'campaign'
        ordering = ('-start_date',)
        unique_together = ('office', 'start_date')


class CampaignToIndicator(models.Model):

    indicator = models.ForeignKey(Indicator)
    campaign = models.ForeignKey(Campaign)

    class Meta:
        db_table = 'campaign_to_indicator'
        unique_together = ('indicator', 'campaign')

class DataPoint(models.Model):
    '''
    The core table of the application.  This is where the raw data is stored
    and brought together from data entry, ODK and csv upload.

    Note that this table does not store the aggregated or calculated data, only
    the raw data that we get from the source.

    The source_submission shows the original source of the data in the
    source_submission.  The source_submission is -1 in the case of data
    entry.

    The cache_job_id column allows us to find out when and why a particular
    datapoint was refreshed.  New datapoints have a cache_job_id = -1 which
    tells the system that it needs to be refreshed.
    '''

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    data_date = models.DateTimeField()
    value = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    source_submission = models.ForeignKey('source_data.SourceSubmission')
    cache_job = models.ForeignKey(CacheJob, default=-1)

    def get_val(self):
        return self.value

    class Meta:
        db_table = 'datapoint'


class DocDataPoint(models.Model):
    '''
    For Validation of upload datapoints.
    '''

    document = models.ForeignKey('source_data.Document')  # redundant
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    data_date = models.DateTimeField()
    value = models.FloatField(null=True)
    source_submission = models.ForeignKey('source_data.SourceSubmission')
    agg_on_location = models.BooleanField()

    class Meta:
        db_table = 'doc_datapoint'


class DataPointEntry(DataPoint):
    """Proxy subclass of DataPoint, for use only in API
    methods used by the manual data entry form. This model
    stores records of all changes in a separate DB table.
    """

    history = HistoricalRecords()

    class Meta:
        proxy = True


class DataPointComputed(models.Model):

    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob, default=-1)
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)

    class Meta:
        db_table = 'datapoint_with_computed'
        unique_together = ('location', 'campaign', 'indicator')


class AggDataPoint(models.Model):

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)
    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob, default=-1)

    class Meta:
        db_table = 'agg_datapoint'
        unique_together = ('location', 'campaign', 'indicator')


class LocationPermission(models.Model):
    '''
    This controls what the user sees.  If you have Nigeria as the top lvl
    Location for a user
    '''

    user = models.OneToOneField('auth.User')
    top_lvl_location = models.ForeignKey(Location)

    class Meta:
        db_table = 'location_permission'


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
    validate the json, but if you insert directly in the table it will not.
    '''

    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000)
    default_office = models.ForeignKey(Office, null=True)
    layout = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'custom_dashboard'


class CustomChart(models.Model):
    '''
    '''

    title = models.CharField(max_length=255, unique=True)
    chart_json = JSONField()

    class Meta:
        db_table = 'custom_chart'
