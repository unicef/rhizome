from django.db import models


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
