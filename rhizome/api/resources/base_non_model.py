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
        GET_params_required = []
        default_limit = 1

    def dehydrate(self, bundle):
        bundle.data.pop("resource_uri", None)

        return bundle

    def get_object_list(self, request):
        '''
        Basic GET behavior for the non model resource.

        This line of code applies the queryset

        This is useful becuase for instance, if you want to queue up your data
        in a persistent data structure, you can us `pre_process_data`, and
        then set the `queryset` to be the output of that operation.  In this
        case while you loose some speed of request by writing that data before
        reading it again, as opposed to just feeding it up directly, but if for
        instance that data needs to be persistent for later use ( take for
        example the DocTransform logic, which saves .csv data to a number of
        tables that then the user can interact with.
        '''
        return list(self._meta.queryset[:self._meta.default_limit])

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie.. Very simply, run any necessary preprocssing,
        and then return the queryset that is assigned in the Meta class of
        the resource.

        ===

        One of the uses of the base_non_model_resources is that when we have
        an API call that really is meant to process data more than it is to
        GET or POST it.

        In this method, we check to see it the resource being called
        ( transform_upload for example ), has a method named, `pre_process_data`
        and if it does, that method is called.

        Whatever that particular resource should return when it comes to
        a GET request is handled in the `QuerySet` attribute of the Meta class.
        """

        # first make sure that we have all of the required parameters for teh
        # request as defined by the Meta class of the resource
        filters = self.validate_filters(request)

        if hasattr(self, "pre_process_data"):
            self.pre_process_data(request)

        # potentially pass filters here
        objects = self.get_object_list(request)
        response_data = {
            'objects': objects,
            'meta': {'total_count': len(objects)},  # add paginator info here..
            'error': None,
        }

        return self.create_response(request, response_data)
