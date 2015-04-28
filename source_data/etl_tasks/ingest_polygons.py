import os
import json
from pprint import pprint

from django.conf import settings

from source_data.models import *

def main():

    source_id = Source.objects.get(source_name='region_upload').id

    rg_type_map = {0 : 'Country', 1:'Province',2:'District', 3 : 'Ward', 4:'Settlement'}

    json_dir = settings.MEDIA_ROOT + 'geo/'

    for file in os.listdir(json_dir):

        levels = []

        if file.endswith(".geojson"):

            docfile = json_dir + file

            print 'processing %s ' % docfile

            document_id = Document.objects.create(docfile=docfile\
                ,created_by_id=1,source_id=source_id).id

            with open(docfile) as f:
                data = json.load(f)

            for feature_dict in data['features']:

                properties = feature_dict['properties']
                polygon = feature_dict['geometry']['coordinates']

                end_date = properties['ENDDATE']

                if end_date == '9999/12/31':

                    region_level = properties['LVL']
                    parent_region_level = str(int(region_level) - 1) if \
                        region_level > 0 else 0

                    region_string = properties['ADM%s_NAME' % region_level]

                    region_type = rg_type_map[region_level]
                    country = properties['ADM0_NAME']

                    parent_name = properties['ADM%s_NAME' % parent_region_level]
                    parent_code = properties['ADM%s_NAME' % parent_region_level]


                    source_region = SourceRegion.objects.create(
                        document_id = document_id,
                        region_string = region_string,
                        region_type = region_type,
                        country = country,
                        region_code = properties['OBJECTID'],
                        parent_name = parent_name,
                        parent_code = parent_code,
                        lat = properties['CENTER_LAT'],
                        lon = properties['CENTER_LON'],
                        source_guid = properties['GUID'].replace('{','')\
                               .replace('}','')
                    )

                    shape_defaults = {
                        'source_id' : source_region.id,
                        'shape_len' : properties[u'SHAPE_Leng'],
                        'shape_area' : properties['SHAPE_Area'],
                        'polygon': polygon
                    }

                    SourceRegionPolygon.objects.create(**shape_defaults)


    return None, 'geo json parsed!!'
