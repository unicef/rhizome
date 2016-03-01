from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import Resource

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
        authentication = MultiAuthentication(CustomSessionAuthentication(), ApiKeyAuthentication())
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
