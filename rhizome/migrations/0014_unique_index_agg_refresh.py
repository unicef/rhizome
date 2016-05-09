from rhizome.agg_tasks import AggRefresh
from django.db import transaction
from django.db.transaction import TransactionManagementError
from django.db import models, migrations
from rhizome.models import DataPoint, Campaign


def run_agg_refresh(apps, schema_editor):
    campaigns = Campaign.objects.all()
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        if DataPoint.objects.filter(campaign_id = campaign.id).exists():
            agg = AggRefresh(campaign.id)

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_datapoint_unique_index'),
    ]

    operations = [

        # update field constraint
        migrations.AlterField(
            model_name='datapoint',
            name='unique_index',
            field=models.CharField(default=-1, max_length=255,unique=True),
        ),
        # run agg_refresh
        migrations.RunPython(run_agg_refresh)
    ]

