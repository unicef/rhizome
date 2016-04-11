import string
import random

from django.db import models, migrations
from django.core.exceptions import ObjectDoesNotExist

from rhizome.models import *
from rhizome.cache_meta import LocationTreeCache
from rhizome.etl_tasks.refresh_master import MasterRefresh


def add_regions(apps, schema_editor):

	#increment current location admin levels
	locations_to_increment = LocationType.objects.filter(admin_level__gte =1).order_by('-admin_level')

	if not LocationType.objects.filter(name="Region").exists():
		for location in locations_to_increment:
			location.admin_level = location.admin_level + 1
			location.save()

		# Add Location Type "Region"
		LocationType.objects.create(
			name="Region",
			admin_level = 1)

	regions_dict = {
	'North East':['Baghlan', 'Kunduz', 'Takhar', 'Badakhshan'],
	'South East':['Ghazni', 'Paktya', 'Paktika', 'Khost'],
	'East':['Nangarhar', 'Laghman', 'Kunar', 'Nuristan'],
	'Central':['Kabul', 'Parwan', 'Panjsher', 'Wardak', 'Kapisa', 'Logar'],
	'Central Highlands':['Daykundi', 'Bamyan'],
	'South':['Kandahar (Province)', 'Hilmand', 'Uruzgan', 'Nimroz', 'Zabul'],
	'West':['Badghis', 'Farah', 'Ghor', 'Hirat', ],
	'North':['Balkh', 'Samangan', 'Sari Pul (Province)', 'Sar-E-Pul', 'Jawzjan', 'Faryab']

	}

	# Create the regions in the database
	# add the country as a parent of the regions
	location_type_id = LocationType.objects.get(name="Region").id
	parent_location_id = Location.objects.get(name="Afghanistan").id
	N = 7
	batch =[]
	for region in regions_dict.keys():
		random_location_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
		batch.append(Location(**{
			'name': region,
			'location_code': random_location_code,
			'location_type_id': location_type_id,
			'office_id': 1,
			'parent_location_id': parent_location_id
		}))

	Location.objects.filter(location_type_id = location_type_id).delete()
	Location.objects.bulk_create(batch)
	province_location_type_id = LocationType.objects.get(name = "Province").id

	# Add the provinces to the regions as parent
	for region, province_list in regions_dict.iteritems():
		region_id = Location.objects.get(name = region).id
		for province in province_list:
			try:
				p = Location.objects.get(name = province)
				p.parent_location_id = region_id
				p.save()
			except ObjectDoesNotExist:
				random_location_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
				Location.objects.create(
					name=province,
					location_code = random_location_code,
					location_type_id = province_location_type_id,
					office_id = 1,
					parent_location_id = region_id
				)

	passed_test = test_migration(regions_dict)

	if not passed_test:
		raise Exception('that failed')

def test_migration(regions_dict):

	expected_region_length = len(regions_dict.keys())

	regions = Location.objects.filter(
		location_type__name = 'Region'
	)

	afg_children = Location.objects.filter(
		parent_location__name = 'Afghanistan'
	)

	first_condition = len(regions) == expected_region_length
	second_condition = len(afg_children) == expected_region_length

	test_result = first_condition and second_condition

	return test_result

def run_agg(apps, schema_editor):
	ltr = LocationTreeCache()
	ltr.main()

	# ensure that aggregation works by running the agg refresh in the migration itself.

	campaigns = Campaign.objects.all()
	for campaign in campaigns:
		if DataPoint.objects.filter(campaign_id = campaign.id).exists():
			agg = AggRefresh(campaign.id)
			agg.main()



class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(add_regions),
		migrations.RunPython(run_agg)
    ]

    dependencies = [
        ('rhizome', '0008_indicator_class_map_table'),
    ]
