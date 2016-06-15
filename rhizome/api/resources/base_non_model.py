from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.resources.base_resource import BaseResource

class BaseNonModelResource(BaseResource):
    '''
    Needs Documentation
    http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta:
        authentication = MultiAuthentication(
            CustomSessionAuthentication(), ApiKeyAuthentication())
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        always_return_data = True
        cache = CustomCache()
        serializer = CustomSerializer()
        GET_params_required = ['indicator_id']
        default_limit = 1

    def dehydrate(self, bundle):
        bundle.data.pop("resource_uri", None)

        return bundle

    def pre_process_resoruce_data(self, request):
        """
        One of the uses of the base_non_model_resources is that when we have
        an API call that really is meant to process data more than it is to
        GET or POST it.

        In this method, we check to see it the resource being called
        ( transform_upload for example ), has a method named, `pre_process_data`
        and if it does, that method is called.

        Whatever that particular resource should return when it comes to
        a GET request is handled in the `QuerySet` attribute of the Meta class.
        """

        pre_process_resource_data = hasattr(self, "pre_process_data", None)
        if pre_process_data_operation:
            self.pre_process_data(request)

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie.. Very simply, run any necessary preprocssing,
        and then return the queryset that is assigned in the Meta class of
        the resource.
        """

        self.pre_process_resource_data(request)
        objects = list(self._meta.queryset[:self._meta.default_limit])

        response_data = {
            'objects': objects,
            'meta': {'total_count': len(objects)},  # add paginator info here..
            'error': None,
        }

        return self.create_response(request, response_data)
