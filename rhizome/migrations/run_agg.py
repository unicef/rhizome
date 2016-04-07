from django.db import models, migrations
from django.core.exceptions import ObjectDoesNotExist
from rhizome.models import *
import string
import random
from rhizome.cache_meta import LocationTreeCache
from rhizome.agg_tasks import AggRefresh
from rhizome.etl_tasks.refresh_master import MasterRefresh

def run_agg(apps, schema_editor):
	ltr = LocationTreeCache()
	ltr.main()

	# ensure that aggregation works by running the agg refresh in the migration itself.
	for doc in Document.objects.all():
		mr = MasterRefresh(1, doc.id)
		mr.main()

	campaigns = Campaign.objects.all()
	for campaign in campaigns:
		if DataPoint.objects.filter(campaign_id = campaign.id).exists():
			agg = AggRefresh(campaign.id)
			agg.main()


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(run_agg),
    ]

    dependencies = [
        ('rhizome', 'add_regions'),
    ]