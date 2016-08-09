from django.db import models
from jsonfield import JSONField


class LocationType(models.Model):
    '''
    Country, Province, District, Sub-District, Settlement.

    While each country has it's own nomenclature for the different levels of
    the locational heirarchy ( i.e. Nigeria calls Districts LGAs ) the location
    type table allows us to assocaite a location_type key to each location.

    For our purpose the 5 location types are the definitive types of locations
    that the system supports.
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
    location id.  The parent location id is used to create the tree used to
    create aggregate statistics based on the information stored at the leaf
    level.
    '''

    name = models.CharField(max_length=255, unique=True)
    location_code = models.CharField(max_length=255, unique=True)
    location_type = models.ForeignKey(LocationType)
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

    Nigeria for instance as a parent location, will have ALL children
    recursively stored with the cooresponding level to indicate its depth
    in the tree.
    '''

    parent_location = models.ForeignKey(
        Location, related_name='ultimate_parent')
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


class LocationPermission(models.Model):
    '''
    This controls what the user sees.  If you have Nigeria as the top lvl
    Location for a user
    '''

    user = models.OneToOneField('auth.User')
    top_lvl_location = models.ForeignKey(Location)

    class Meta:
        db_table = 'location_permission'


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
    # parent_location = models.ForeignKey(Location, related_name='parent')
    geo_json = JSONField()
    # properties = JSONField()

    class Meta:
        db_table = 'min_polygon'
