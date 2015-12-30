import json

from datapoints.models import MinGeo
from datapoints.api.base import BaseNonModelResource, \
    get_locations_to_return_from_url
from tastypie import fields
from tastypie.resources import ALL

class GeoJsonResult(object):
    location_id = int()
    type = unicode()
    properties = dict()
    geometry = dict()
    parent_location_id = int()


class GeoResource(BaseNonModelResource):
    '''
    A non model resource that allows us to query for shapefiles based on a
    colletion of parameters.
    '''

    location_id = fields.IntegerField(attribute='location_id')
    type = fields.CharField(attribute='type')
    properties = fields.DictField(attribute='properties')
    geometry = fields.DictField(attribute='geometry')
    parent_location_id = fields.IntegerField(attribute='parent_location_id')

    class Meta(BaseNonModelResource.Meta):
        object_class = GeoJsonResult
        resource_name = 'geo'
        filtering = {
            "location_id": ALL,
        }

    def get_object_list(self, request):
        '''
        parse the url, query the polygons table and do some
        ugly data munging to convert the results from the DB into geojson
        '''

        self.err = None
        locations_to_return = self.get_locations_to_return_from_url(request)
        # since this is not a model resource i will filter explicitly #

        if err:
            self.err = err
            return []

        with_parent = None
        try:
            with_parent = request.GET['with_parent']
        except KeyError:
            pass

        features = []

        if with_parent is None:
            polygon_values_list = MinGeo.objects.filter(location_id__in=locations_to_return).values()
            for p in polygon_values_list:
                geo_dict = json.loads(p['geo_json'])
                geo_obj = GeoJsonResult()
                geo_obj.location_id = p['location_id']
                geo_obj.geometry = geo_dict['geometry']
                geo_obj.type = geo_dict['type']
                geo_obj.properties = {'location_id': p['location_id']}
                features.append(geo_obj)
        else:
            polygon_values_list = MinGeo.objects.select_related('location')\
                .filter(location_id__in=locations_to_return).all()
            for p in polygon_values_list:
                geo_obj = GeoJsonResult()
                geo_obj.location_id = p.location.id
                geo_obj.geometry = p.geo_json['geometry']
                geo_obj.type = p.geo_json['type']
                geo_obj.properties = {'location_id': p.location.id}
                geo_obj.parent_location_id =\
                    p.location.id if p.location.parent_location_id is None else p.location.parent_location_id
                features.append(geo_obj)
        return features

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri", None)
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        '''
        If there is an error for this resource, add that to the response.  If
        there is no error, than add this key, but set the value to null.  Also
        add the total_count to the meta object as well
        '''
        # get rid of the meta_dict. i will add my own meta data.
        data['type'] = "FeatureCollection"
        data['features'] = data['objects']
        data['error'] = self.err

        data.pop("objects", None)
        data.pop("meta", None)

        return data
