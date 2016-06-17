from rhizome.models import MinGeo
from rhizome.api.resources.base_model import BaseModelResource
from tastypie import fields
from tastypie.resources import ALL

import json

class GeoResource(BaseModelResource):
    '''
    **GET Request** A non model resource that allows us to query for shapefiles
        based on a colletion of parameters.
        - *Required Parameters:*
            'location_id__in' the location of the shape file that we wish
            to retrieve
        - *Optional Parameters:*
            'location_depth' the recursive depth in relation to the location_id
            parameter. For instance, a depth of 1 would get all children of that
             location. 2 would return all "grandchildren"
            'location_type' return the descendants of the location_id param that
             have the given location_type id.
    '''

    location_id = fields.IntegerField(attribute='location_id')
    parent_location_id = fields.IntegerField(attribute='parent_location_id')

    class Meta(BaseModelResource.Meta):
        object_class = MinGeo
        resource_name = 'geo'
        filtering = {
            "location_id": ALL,
        }
        default_limit = 10000

    def get_object_list(self, request):
        '''
        parse the url, query the polygons table and do some
        ugly data munging to convert the results from the DB into geojson
        '''
        objects = []
        loc_id_list = list(self.get_locations_to_return_from_url(request))
        for p in MinGeo.objects.filter(
            location_id__in=loc_id_list):
            geo_obj = {
            'location_id' : p.location.id,
            'geometry' : p.geo_json['geometry'],
            'type': p.geo_json['type'],
            'properties': {'location_id': p.location.id},
            'parent_location_id' :\
                p.location.id if p.location.parent_location_id is None else p.location.parent_location_id
            }
            objects.append(geo_obj)
        return objects

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''
        return self.get_object_list(bundle.request)
