from django.db import models, migrations
from django.core.exceptions import ObjectDoesNotExist
from rhizome.models import *
import string
import random
from rhizome.cache_meta import LocationTreeCache

def add_regions(apps, schema_editor):

	#increment current location admin levels
	locations_to_increment = LocationType.objects.filter(admin_level__gte =1).order_by('-admin_level')

	for location in locations_to_increment:
		location.admin_level = location.admin_level + 1
		location.save()

	# Add Location Type "Region"
	LocationType.objects.create(
		name="Region",
		admin_level = 1)

	regions_dict = {
	'North East':['Baghlan', 'Kunduz', 'Takhar', 'Badakhshan'],
	'South East':['Ghazni', 'Paktia', 'Paktika', 'Khost'],
	'East':['Nangarhar', 'Laghman', 'Kunar', 'Nuristan'],
	'Central':['Kabul', 'Parwan', 'Panjshir', 'Wardak', 'Kapisa', 'Logar'],
	'South':['Kandahar', 'Hilmand', 'Urozgan', 'Nimroz', 'Zabul'],
	'West':['Badghis', 'Farah', 'Ghor', 'Herat', ],
	'North':['Balkh', 'Samangan', 'Sar-e-Pul', 'Jawzjan', 'Faryab']

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
    



class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(add_regions),
    ]

    dependencies = [
        ('rhizome', '0008_auto_20160404_1258'),
    ]

