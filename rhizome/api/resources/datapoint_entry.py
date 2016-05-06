import traceback

from tastypie import fields
from tastypie import http
from tastypie.resources import ALL
from tastypie.exceptions import ImmediateHttpResponse

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import InputException
from rhizome.api.serialize import CustomJSONSerializer
from rhizome.models import Campaign, Location, Indicator, DataPointEntry, DataPoint

class DatapointEntryResource(BaseModelResource):
    '''
    **GET Request:**
        - *Required Parameters:*
            'campaign__in' A list of campaign ids
            'indicator__in' A list of indicator ids
        - *Errors:*
            if a campaign or indicator id is invalid, the API will return a 500 status code
    **POST Request:** Create a new datapoint or update an existing one. 
        - *Required Parameters:*
            'campaign_id'
            'location_id'
            'indicator_id'
            'value'
    '''
    required_keys = [
        # 'datapoint_id',
        'indicator_id', 'location_id',
        'campaign_id', 'value',  # 'changed_by_id',
    ]
    # for validating foreign keys
    keys_models = {
        'location_id': Location,
        'campaign_id': Campaign,
        'indicator_id': Indicator
    }
    location = fields.IntegerField(attribute='location_id')
    # campaign = fields.IntegerField(attribute='campaign_id')
    indicator = fields.IntegerField(attribute='indicator_id')

    class Meta():
        # note - auth inherited from parent class #
        queryset = DataPointEntry.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'datapointentry'
        always_return_data = True
        max_limit = None  # no pagination
        filtering = {
            'indicator': ALL,
            'campaign': ALL,
            'location': ALL,
        }
        serializer = CustomJSONSerializer()


    def apply_filters(self, request, applicable_filters):
        """
        An ORM-specific implementation of ``apply_filters``.

        The default simply applies the ``applicable_filters`` as ``**kwargs``,
        but should make it possible to do more advanced things.
        """

        return self.get_object_list(request)#.filter(**applicable_filters)

    def get_object_list(self, request):
        '''
        '''

        campaign_param, indicator_param = request.GET['campaign__in'], \
            request.GET['indicator__in']

        indicator__in = indicator_param.split(',')

        campaign_obj = Campaign.objects.get(id=campaign_param)

        return DataPoint.objects.filter(
                data_date__gte = campaign_obj.start_date,
                data_date__lte = campaign_obj.end_date,
                location_id = campaign_obj.top_lvl_location_id,
                indicator__in = indicator__in
            )


    def save(self, bundle, skip_errors=False):
        '''
        Overriding Tastypie save method here because the
        authorized_update_detail of this resource is failing.  Will need more
        research here, but commenting this out for now as authorization is
        handled separately.
        '''
        self.is_valid(bundle)

        if bundle.errors and not skip_errors:
            raise ImmediateHttpResponse(response=self\
                .error_response(bundle.request, bundle.errors))

        # Check if they're authorized.
        # if bundle.obj.pk:
        #     self.authorized_update_detail(self.get_object_list(bundle.request), bundle)
        # else:
        #     self.authorized_create_detail(self.get_object_list(bundle.request), bundle)

        # Save FKs just in case.
        self.save_related(bundle)

        # Save the main object.
        bundle.obj.save()
        bundle.objects_saved.add(self.create_identifier(bundle.obj))

        # Now pick up the M2M bits.
        m2m_bundle = self.hydrate_m2m(bundle)
        self.save_m2m(m2m_bundle)
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Make sure the data is valid, then save it.
        All POST requests come through here, whether they're truly
        'obj_create' or actually 'obj_update'.
        Also, if a request comes in with value=NULL, that means set the value
        of that obect = 0.
        """

        try:
            print 'here'
            self.validate_object(bundle.data)

            # Determine what kind of request this is: create, update, or delete
            # throw error if can't get a real user id
            user_id = self.get_user_id(bundle)
            if user_id is None:
                raise InputException(0, 'Could not get User ID from cookie')
            existing_datapoint = self.get_existing_datapoint(bundle.data)
            if existing_datapoint is not None:

                bundle.response = self.success_response() ##?
                return self.obj_update(bundle, **{'id': existing_datapoint.id})

            else: # CREATE
                data_to_insert = bundle.data
                # find the campaign object from the parameter
                campaign_obj = Campaign.objects.get(id=int(\
                    data_to_insert['campaign_id']))
                ## create the dictionary used to insert into datapoint ##
                data_to_insert['data_date'] = campaign_obj.start_date
                data_to_insert['source_submission_id'] = -1 # data_entry
                data_to_insert['cache_job_id'] = -1 # to process
                ## insert into datpaoint table ##
                bundle.obj = DataPoint.objects.create(**data_to_insert)
                bundle.data['id'] = bundle.obj.id
                bundle.obj.campaign_id = campaign_obj.id
                return bundle

        except Exception, e:
            e.code = 0
            e.data = traceback.format_exc()
            response = self.create_response(
                bundle.request,
                self.make_error_response(e),
                response_class=http.HttpApplicationError
            )
            raise ImmediateHttpResponse(response=response)

    def obj_update(self, bundle, **kwargs):
        '''
        Overriding this tastypie method so we can explicitly set the value to
        NULL when the value comes in as NaN.  This method is how the system
        handles "deletes" that is we do not remove the row all together, just
        set the value to null so the history can be maintained, and we are
        more easily able to queue up changes for caching.
        '''

        value_to_update = bundle.data['value']

        if value_to_update == 'NaN':
            bundle.data['value'] = None

        dp = DataPoint.objects.get(id=kwargs['id'])
        dp.value = value_to_update
        dp.save()

        dp.campaign_id = bundle.data['campaign_id']

        bundle.obj = dp
        bundle.data['value'] = value_to_update
        bundle.data['id'] = kwargs['id']

        return bundle

    def get_user_id(self, bundle):
        request = bundle.request

        if 'sessionid' in request.COOKIES:
            session = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in session.get_decoded():
                user = User.objects.get(id=session.get_decoded()['_auth_user_id'])
                return user.id

    # def is_delete_request(self, bundle):
    #     if 'value' in bundle.data and bundle.data['value'] is None:
    #         return True
    #     else:
    #         return False

    def obj_delete(self, bundle, **kwargs):
        """This is here to prevent an objects from ever being deleted."""
        pass

    def obj_delete_list(self, bundle, **kwargs):
        """This is here to prevent a list of objects from
        ever being deleted."""
        pass

    def get_existing_datapoint(self, data):
        """
        Assumes data is valid
        (i.e. data should have passed validate_object first)
        """

        campaign = Campaign.objects.get(id=int(data['campaign_id']))

        try:
            obj = DataPointEntry.objects.get(
                location_id=int(data['location_id']),
                data_date=campaign.start_date,
                indicator_id=int(data['indicator_id']),
            )
            return obj
        except ObjectDoesNotExist as err:
            return

    def hydrate(self, bundle):

        if hasattr(bundle, 'obj') \
            and isinstance(bundle.obj, DataPointEntry) \
            and hasattr(bundle.obj, 'location_id') \
            and bundle.obj.location_id is not None \
            and hasattr(bundle.obj, 'campaign_id') \
            and bundle.obj.location_id is not None \
            and hasattr(bundle.obj, 'indicator_id') \
                and bundle.obj.location_id is not None:
            # we get here if there's an existing datapoint being modified
            pass
        else:
            # we get here if we're inserting a brand new datapoint
            bundle.obj = DataPointEntry()
            bundle.obj.location_id = int(bundle.data['location_id'])
            bundle.obj.campaign_id = int(bundle.data['campaign_id'])
            bundle.obj.indicator_id = int(bundle.data['indicator_id'])
            bundle.obj.value = bundle.data['value']

        bundle.obj.cache_job_id = -1
        bundle.obj.source_submission_id = -1

        return bundle

    def dehydrate(self, bundle):
        # hack: bundle will only have a response attr if this is a POST or PUT request
        if hasattr(bundle, 'response'):
            bundle.data = bundle.response
        else:  # otherwise, this is a GET request
            bundle.data['datapoint_id'] = bundle.data['id']
            del bundle.data['id']
            # for key in ['campaign', 'indicator', 'location']:
            for key in ['indicator', 'location']:
                bundle.data['{0}_id'.format(key)] = bundle.data[key]
                del bundle.data[key]
            for key in ['created_at', 'resource_uri']:
                del bundle.data[key]

        return bundle

    def validate_object(self, obj):
        """
        Check that object has all the right fields, yadda yadda yadda.
        """
        for key in self.required_keys:
            if key not in obj:
                raise InputException(2, 'Required metadata missing: {0}'.format(key))

        # ensure that metadata values are valid
        for key, model in self.keys_models.iteritems():
            try:
                key_id = int(obj[key])
            except ValueError:
                raise InputException(4, 'Invalid metadata value: {0}'.format(key))
            try:
                model.objects.get(id=key_id)
            except (ValueError, ObjectDoesNotExist):
                raise InputException(3, 'Could not find record for metadata value: {0}'.format(key))

   # MEP: I commented this out because it doesn't appear to be used anywhere

    # def validate_object_update(self, obj):
    #     """
    #     When updating an object, validate the new data.
    #     """
    #     # what should we do about id, url, created_at ?
    #     # those all get filled in automatically, right?

    #     # TODO uncomment once authorization is in place
    #     # should this be a required key? yeah
    #     # assert obj.has_key('changed_by_id')
    #     # user_id = int(obj['changed_by_id'])
    #     # User.objects.get(id=user_id)

    #     # ensure that location, campaign, and indicator, if present, are valid values
    #     if 'location_id' in obj:
    #         location_id = int(obj['location_id'])
    #         Location.objects.get(id=location_id)

    #     if 'campaign_id' in obj:
    #         campaign_id = int(obj['campaign_id'])
    #         Campaign.objects.get(id=campaign_id)

    #     if 'indicator_id' in obj:
    #         indicator_id = int(obj['indicator_id'])
    #         Indicator.objects.get(id=indicator_id)

    def success_response(self):
        response = {
            'success': 1
        }
        return response

    def make_error_response(self, error):
        response = {
            'success': 0,
            'error': {
                'code': getattr(error, 'code', 0),
                'message': error.message
            }
        }
        if hasattr(error, 'data'):
            response['error']['data'] = error.data
        return response
