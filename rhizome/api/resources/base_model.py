import json

from django.http import HttpResponse

from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import ModelResource
from tastypie import http

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.exceptions import DatapointsException
from rhizome.api.resources.base import BaseResource
from django.core.exceptions import ObjectDoesNotExist

class BaseModelResource(ModelResource, BaseResource):
    '''
    This applies to only the V1 API.  This method inherits from Tastypie's
    model resource.

    This resource strips down almost all of the tastypie functions which
    drastically slow down the API performance.

    IMPORTANT: if you note, all of the resources use the .values() option for
    each queryset.  That returns the model as JSON, so the idea is that the
    API does not need to serialize or dehydrate the resource.

    The models are set up so that the API does as little transformation as
    possible.  That means however, that a few of our metadata models ( see
    campaign / indicator ) are cached and contain related information making
    the job of the API easy.
    '''

    class Meta:
        authentication = MultiAuthentication(CustomSessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'post', 'delete', 'patch']
        cache = CustomCache()
        serializer = CustomSerializer()

    def dispatch(self, request_type, request, **kwargs):
        '''
        '''
        return super(BaseModelResource, self).dispatch(request_type, request, **kwargs)

    def convert_post_to_patch(request):
        '''
        '''
        return super(BaseModelResource, self).convert_post_to_patch(request)

    def patch_detail(self, request, **kwargs):
        """
        Updates a resource in-place.
        Calls ``obj_update``.
        If the resource is updated, return ``HttpAccepted`` (202 Accepted).
        If the resource did not exist, return ``HttpNotFound`` (404 Not Found).
        """
        # request = self.convert_post_to_patch(request)
        basic_bundle = self.build_bundle(request=request)

        # We want to be able to validate the update, but we can't just pass
        # the partial data into the validator since all data needs to be
        # present. Instead, we basically simulate a PUT by pulling out the
        # original data and updating it in-place.
        # So first pull out the original object. This is essentially
        # ``get_detail``.

        try:
            obj = self._meta.object_class.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)

        # Now update the bundle in-place.
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        self.update_in_place(request, bundle, deserialized)

        if not self._meta.always_return_data:
            return http.HttpAccepted()
        else:
            # Invalidate prefetched_objects_cache for bundled object
            # because we might have changed a prefetched field
            bundle.obj._prefetched_objects_cache = {}
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)
            return self.create_response(request, bundle, response_class=http.HttpAccepted)


    def get_detail(self, request, **kwargs):
        """
        Returns a single serialized resource.
        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.
        Should return a HttpResponse (200 OK).
        """


        try:
            obj = self._meta.object_class.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie..
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        bundles = []

        # this is a temporary hack to get data_entry working ##
        # long term fix is to make DatapointEntryResource a NonModelResource
        # https://trello.com/c/skxxpzYj/327-rp-bug-2005-cannot-load-entry-form-in-enter-data-via-form
        if self.Meta.resource_name == 'datapointentry':
            return super(ModelResource, self).get_list(request, **kwargs)

        if len(objects) > 0:
            # find json_fields ( should be explicit here and check data type)
            # of the field, but for this works..
            json_obj_keys = [k for k, v in objects[0].items() if 'json' in k]

        for obj in objects:

            # serialize json fields ##
            for json_key in json_obj_keys:
                obj[json_key] = json.loads(obj[json_key])

            # hack lvl attribute
            if 'location_type_id' in obj:
                obj['lvl'] = obj['location_type_id'] - 1

            bundles.append(obj)

        response_meta = self.get_response_meta(request, bundles)

        response_data = {
            'objects': bundles,
            'meta': response_meta,  # add paginator info here..
            'error': None,
        }

        return self.create_response(request, response_data)

    def get_response_meta(self, request, objects):

        meta_dict = {
            'top_lvl_location_id': self.top_lvl_location_id,
            'limit': None,  # paginator.get_limit(),
            'offset': None,  # paginator.get_offset(),
            'total_count': len(objects),
        }
        return meta_dict
