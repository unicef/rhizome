import json

from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import (ModelResource, ALL)
from tastypie import http

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.resources.base_resource import BaseResource
from rhizome.api.exceptions import RhizomeApiException
from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned ##, ValidationError,
)

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
        authentication = MultiAuthentication(
            CustomSessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'post', 'delete', 'patch']
        cache = CustomCache()
        serializer = CustomSerializer()
        filtering = {
            "id": ALL,
        }

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
        deserialized = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
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

    def obj_get(self, bundle, **kwargs):
        """
        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.

        Currently used to find one object from the url api/v1/resource/<pk>/
        """

        try:
            obj = self._meta.object_class.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            error_message = 'that %s does dot exist' % self._meta.object_class
            return RhizomeApiException(message = error_message, code = 500)
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        return obj

    def get_detail(self, request, **kwargs):
        """
        Returns a single serialized resource.
        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.
        Should return a HttpResponse (200 OK).
        """

        obj = self.obj_get(None, **kwargs)
        bundle = self.build_bundle(obj=obj, request=request)
        bundle.data = obj.__dict__
        bundle.data.pop('_state')

        return self.create_response(request, bundle)

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie..
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(
            bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        bundles = []

        # this is a temporary hack to get data_entry working ##
        # long term fix is to make DatapointEntryResource a NonModelResource
        # https://trello.com/c/skxxpzYj/327-rp-bug-2005-cannot-load-entry-form-in-enter-data-via-form
        if self.Meta.resource_name == 'datapointentry':
            return super(ModelResource, self).get_list(request, **kwargs)

        if len(objects) > 0:
            # find json_fields ( should be explicit here and check data type )
            # i.e. find the field datatypes from the model definition
            json_obj_keys = [k for k, v in objects[0].items() if 'json' in k]

        for obj in objects:

            # serialize json fields ##
            for json_key in json_obj_keys:
                obj[json_key] = json.loads(obj[json_key])

            # hack lvl attribute FIXME
            if 'location_type_id' in obj:
                obj['lvl'] = obj['location_type_id'] - 1

            bundles.append(obj)

        response_meta = self.get_response_meta(bundles)

        response_data = {
            'objects': bundles,
            'meta': response_meta,  # add paginator info here..
            'error': None,
        }

        return self.create_response(request, response_data)

    def post_list(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.
        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.
        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.
        """

        deserialized = self.deserialize(\
            request, \
            request.body, \
            format=request.META.get('CONTENT_TYPE', 'application/json')\
        )
        deserialized = self\
            .alter_deserialized_detail_data(request, deserialized)

        bundle = self.build_bundle(data=deserialized, request=request)

        updated_bundle = self.obj_create(bundle, \
            **self.remove_api_resource_names(kwargs))

        location = self.get_resource_uri(updated_bundle)

        return self.create_response(request, updated_bundle, \
            response_class=http.HttpCreated, location=location)

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """

        ## Try to validate / clean the POST before submitting the INSERT ##
        bundle = self.validate_obj_create(bundle, **kwargs)

        ## create the object with the data from the request #
        bundle.obj = self._meta.object_class.objects.create(**bundle.data)

        return bundle

    def validate_obj_create(self, bundle, **kwargs):
        '''
        Custom module that is meant to clean and check the POST request, making
        sure that we catch any errors we can befoer submitting to the database.

        For instance, here, we check that the necessary Keys are there, so that
        we can save a trip to the DB by using the `required_fields_for_post`
        attribute on the Meta class of the base_model resoruce.
        '''

        keys_passed = [unicode(x) for x in bundle.data.keys()]
        keys_req = [unicode(x) for x in self._meta.required_fields_for_post]
        missing_keys = set(keys_req).difference(set(keys_passed))

        if len(missing_keys) > 0:
            raise RhizomeApiException(message = 'missing params %s' %\
                missing_keys)

        return bundle

    def obj_delete(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete``.
        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.

        To Do -- Check 'is_superuser' flag
        """

        obj = self.obj_get(bundle=bundle, **kwargs)
        obj = self._meta.object_class.objects.get(id = obj.id).delete()

    def obj_delete_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete_list``.
        """
        return super(BaseResource, self)\
            .obj_delete_list(bundle, **kwargs)
