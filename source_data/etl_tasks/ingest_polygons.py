import os
import json

from django.conf import settings

from source_data.models import *

def main():


    rg_type_map = {0 : 'Country', 1:'Province',2:'District', 3 : 'Ward', 4:'Settlement'}

    json_dir = settings.MEDIA_ROOT + 'geo/'

    for file in os.listdir(json_dir):

        levels = []

        if file.endswith("nga_adm0.geojson"):

            docfile = json_dir + file

            document_id = Document.objects.create(docfile=docfile\
                ,created_by_id=1).id

            with open(docfile) as f:
                data = json.load(f)

            for feature_dict in data['features']:

                properties = feature_dict['properties']
                polygon = feature_dict['geometry']['coordinates']

                # pprint(properties)
                region_level = properties['LVL']
                parent_region_level = str(int(region_level) - 1) if region_level > 0 else 0

                region_string = properties['ADM%s_NAME' % region_level]

                region_type = rg_type_map[region_level]
                country = properties['ADM0_NAME']

                parent_name = properties['ADM%s_NAME' % parent_region_level]
                parent_code = properties['ADM%s_NAME' % parent_region_level]


                source_region_defaults = {
                    'region_code': properties['OBJECTID'],
                    'parent_name': parent_name,
                    'parent_code': parent_code,
                    'lat': properties['CENTER_LAT'],
                    'lon': properties['CENTER_LON'],
                    'source_guid': properties['GUID'].replace('{','')\
                           .replace('}','')
                }

                source_region,created = SourceRegion.objects.get_or_create(
                    document_id = document_id,
                    region_string = region_string,
                    region_type = region_type,
                    country = country,
                    defaults = source_region_defaults
                )

                if created:

                    shape_defaults = {
                        'source_region_id' : source_region.id,
                        'shape_len' : properties[u'SHAPE_Leng'],
                        'shape_area' : properties['SHAPE_Area'],
                        'polygon': polygon
                    }

                    SourceRegionPolygon.objects.create(**shape_defaults)


    return None, 'geo json parsed!!'
