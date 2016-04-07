from django.db import models, migrations
from django.core.exceptions import ObjectDoesNotExist
from rhizome.models import *
import string
import random
from rhizome.cache_meta import LocationTreeCache

def run_agg(apps, schema_editor):
	ltr = LocationTreeCache()
	ltr.main()

	# ensure that aggregation works by running the agg refresh in the migration itself.
	campaigns = Campaign.objects.all()
	for campaign in campaigns:
		
		agg = AggRefresh(campaign.id)
		agg.main()


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(add_regions),
    ]

    dependencies = [
        ('rhizome', 'add_regions'),
    ]