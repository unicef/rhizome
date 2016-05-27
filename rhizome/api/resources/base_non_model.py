from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.resources.base import BaseResource

class BaseNonModelResource(BaseResource):
    '''
    NOTE: This applies to only the V1 API.  This is only used for the
    /api/v1/datapoint endpoint.

    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta:
        authentication = MultiAuthentication(
            CustomSessionAuthentication(), ApiKeyAuthentication())
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        always_return_data = True
        cache = CustomCache()
        serializer = CustomSerializer()

    def dehydrate(self, bundle):
        bundle.data.pop("resource_uri", None)

        return bundle

    def dispatch(self, request_type, request, **kwargs):
        '''
        '''

        return super(BaseNonModelResource, self).dispatch(request_type, request, **kwargs)

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie..
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle)
        bundles = [obj.__dict__ for obj in objects]

        to_be_serialized = {
            'objects': bundles,
            'meta': {'total_count': len(objects)},  # add paginator info here..
            'error': None,
        }

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(
            request, to_be_serialized)
        return self.create_response(request, to_be_serialized)
