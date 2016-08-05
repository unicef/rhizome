from django.db import models
from jsonfield import JSONField


class CustomChart(models.Model):
    '''
    '''

    uuid = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=True)
    chart_json = JSONField()

    class Meta:
        db_table = 'custom_chart'


class CustomDashboard(models.Model):
    '''
    A table containing all of the custom dashboards in the system.  The data
    in teh dashboard_json field is how the FE is able to draw and render the
    specific vizulaizations.  If inserted via POST the application will
    validate the json, but if you insert directly in the table it will not.
    '''

    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000)
    layout = models.IntegerField(default=0, null=True)
    rows = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'custom_dashboard'
