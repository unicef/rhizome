
from datapoints.models import Region, RegionPolygon
from pandas import read_csv

# df = read_csv('/Users/john/Desktop/regions_prod_2_13.csv')
df = read_csv('/home/ubuntu/region_polygons.csv')

for row in df.values:

    try:
        region_id = Region.objects.get(region_code = str(row[0])).id
        new_obj = RegionPolygon.objects.create(region_id = region_id,geo_json = row[1])

        print region_id
    except Exception as err:
        pass
