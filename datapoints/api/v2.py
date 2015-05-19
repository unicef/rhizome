import json
import datetime
import traceback
from pprint import pprint

from django.core.serializers import json as djangojson
from django.db.models import Model, ManyToManyField
from django.db.models.query import RawQuerySet
from django.db.models.sql.constants import QUERY_TERMS
from django.db.models.options import Options
from django.db.models.fields import AutoField, FieldDoesNotExist
from django.db import connection

from django.forms.models import model_to_dict
from django.utils.encoding import smart_str
from django.contrib.auth.models import User, Group
from django.core import serializers

from datapoints.models import *
from source_data.models import *



class v2Request(object):

    def __init__(self, request, content_type):

        self.request = request
        self.content_type = content_type
        self.user_id = request.user.id
        self.data = None
        self.meta = None
        self.err = None

    def main(self):

        response_data = {
            'objects':self.data,
            'meta':self.meta,
            'error':self.err,
        }

        return response_data


class v2PostRequest(v2Request):


    def __init__(self, request, content_type):

        super(v2PostRequest, self).__init__(request, content_type)

        self.kwargs = self.clean_kwargs(request.POST)
        self.orm_mapping = {
            'campaign': {'orm_obj':Campaign},
            'region': {'orm_obj':Region},
            'indicator': {'orm_obj':Indicator},
            'group': {'orm_obj':Group},
            'user': {'orm_obj':User},
            'region_permission': {'orm_obj':RegionPermission},
            'user_group': {'orm_obj':UserGroup},
            'indicator_map': {'orm_obj':IndicatorMap},
            'region_map': {'orm_obj':RegionMap},
            'campaign_map': {'orm_obj':CampaignMap},

        }

        self.db_obj = self.orm_mapping[content_type]['orm_obj']


    def clean_kwargs(self,query_dict):

        cleaned_kwargs = {}

        for k,v in query_dict.iteritems():
            cleaned_kwargs[k] = v

        ## add mapped_by id for mapping endpoints ##
        if self.content_type in ['region_map','indicator_map','campaign_map']:
            cleaned_kwargs['mapped_by_id'] = self.user_id



        return cleaned_kwargs



    def main(self):
        '''
        if method is create:
        Create an object in accordance to the URL kwargs and return the new ID

        if detlete:
            query for objects taht match
        '''

        ## Create, Update or Delete ##
        request_type = self.determined_request_type()

        try:

            if request_type == 'CREATE':

                new_obj = self.db_obj.objects.create(**self.kwargs)
                self.data = {'new_id':new_obj.id }

            elif request_type == 'DELETE':

                old_obj = self.db_obj.objects.get(**self.kwargs)
                self.data = {'deleted_id': old_obj.id }

                old_obj.delete()

            elif request_type == 'UPDATE':

                obj_to_update = self.db_obj(id=self.id_param, **self.kwargs)
                obj_to_update.save()

                self.data = data = {'updated_id': obj_to_update.id
                , 'updated_values': self.kwargs }

        except Exception, e:
            self.err = traceback.format_exc()

        return super(v2PostRequest, self).main()

    def determined_request_type(self):
        '''
        POST can be create, update, or delete.
        '''

        try:
            self.id_param = self.kwargs['id']
            del self.kwargs['id']

            if self.id_param == '':
                return 'DELETE'
            else:
                return 'UPDATE'

        except KeyError:
            self.id_param = None
            return 'CREATE'



class v2MetaRequest(v2Request):

    def __init__(self, request, content_type):

        return super(v2MetaRequest, self).__init__()


    def main(self):
        '''
        Use information about the django model in order to send meta data
        about the resource to the API.  This is used by the front end to
        dynamically generate table views and forms to interact with these
        models.
        '''

        self.data = {}

        self.all_field_meta = []
        self.meta_data = {
                'slug':self.content_type,
                'name':self.content_type,
                'primary_key':'id',
                'search_field':'slug',
                'defaultSortField':'id',
                'defaultSortDirection':'asc',
        }


        db_table = self.db_obj._meta.db_table
        ca_dct = ColumnAttributes.objects.filter(table_name = \
            db_table).values('column_name','display_name',\
            'display_on_table_flag')

        self.column_lookup = {}
        for row in ca_dct:
            column_name = row['column_name']
            del row['column_name']
            self.column_lookup[column_name] = row


        ## BUILD METADATA FOR EACH FIELD ##
        for ix,(field) in enumerate(self.db_obj._meta.get_all_field_names()):

            try:
                self.build_field_meta_dict(field,ix)
            except KeyError:
                pass


        self.data['fields'] = self.all_field_meta

        return super(v2MetaRequest, self).main()

    def build_field_meta_dict(self, field, ix):
        '''
        Examine model instance to find meta data
        Query the Column Attributes table to find metadata on what django model
        does not store.
        '''
        try:
            field_object = self.db_obj._meta.get_field(field)
        except FieldDoesNotExist:
            return None

        ## DICT TO MAP DJANNGO FIELD DEFINITION TO THE TYPES THE FE EXPECTS ##
        field_type_mapper = {'AutoField':'number','FloatField':'number',
            'ForeignKey':'array','CharField':'string','ManyToManyField':'array',
            'DateTimeField':'datetime','DateField':'datetime','BooleanField':
            'boolean','SlugField':'string','TextField':'string'}

        ## BUILD A DICTIONARY FOR EACH FIELD ##
        field_object_dict = {
            'name': field_object.name,
            'title': self.column_lookup[field_object.name]['display_name'],
            'type': field_type_mapper[field_object.get_internal_type()],
            'max_length': field_object.max_length,
            'editable' : field_object.editable,
            'default_value' : str(field_object.get_default()),
                'display' : {
                    'on_table':self.column_lookup[field_object.name]['display_on_table_flag'],
                    'weightTable':ix,
                    'weightForm':ix,
                },
            'constraints': self.build_field_constraints(field_object)
            }

        self.all_field_meta.append(field_object_dict)


    def build_field_constraints(self,field_object):

        field_constraints = {
            'unique':field_object.unique
            }

        try:
            field_constraints['required'] = field_object.required
        except AttributeError:
            field_constraints['required'] = False

        if field_object.name == 'groups':
        # if isinstance(field_object,ManyToManyField) and field_object.name == 'groups':

            ## HACK FOR USERS ##
            dict_list = [{'value':1,'label':'UNICEF HQ'}]
            field_constraints['items'] = {'oneOf':dict_list}


        return field_constraints


class v2GetRequest(v2Request):


    def __init__(self, request, content_type):

        self.orm_mapping = {
            'campaign': {'orm_obj':Campaign,
                'permission_function':self.apply_campaign_permissions},
            'region': {'orm_obj':Region,
                'permission_function':self.apply_region_permissions},
            'indicator': {'orm_obj':IndicatorAbstracted,
                'permission_function':None},
            'group': {'orm_obj':Group,
                'permission_function':None},
            'user': {'orm_obj':UserAbstracted,
                'permission_function':None},
            'region_permission': {'orm_obj':RegionPermission,
                'permission_function':None},
            'user_group': {'orm_obj':UserGroup,
                'permission_function':None},
            'document': {'orm_obj':Document,
                'permission_function':None},
            'office': {'orm_obj':Office,
                'permission_function':None},
        }

        self.db_obj = self.orm_mapping[content_type]['orm_obj']
        self.permission_function = self.orm_mapping[content_type]\
            ['permission_function']

        self.kwargs = self.clean_kwargs(request.GET)
        return super(v2GetRequest, self).__init__(request, content_type)

    def main(self):
        '''
        Get the list of database objects ( ids ) by applying the URL kwargs to
        the filter method of the djanog ORM.
        '''
        ## IF THERE ARE NO FILTERS, THE API DOES NOT NEED TO ##
        ## QUERY THE DATABASE BEFORE APPLYING PERMISSIONS ##
        if not self.kwargs and self.content_type in ['campaign','region']:
            qset = None
        else:
            qset = list(self.db_obj.objects.filter(**self.kwargs).values())


        err, filtered_data = self.apply_permissions(qset)
        err, data = self.serialize(filtered_data)

        ## apply limit and offset.  Not ideal that this does happen at the
        ## data base level, but applying limit/offset at here and querying for
        ## all the data is fine for now as these endpoints are fast.
        self.data = data[self.offset:self.limit + self.offset]
        self.full_data_length = len(data)
        self.err = err
        self.meta = self.build_meta()

        return super(v2GetRequest, self).main()


    def clean_kwargs(self,query_dict):
        '''
        When passing filters make sure that what is in the URL string is
        actually a field of the model.

        This includes parsing the query terms out of the parameter key.  i.e.
        when the API receives id__gte=50, we need to check to see if "id"
        is a field ,not id__gte=50.
        '''

        cleaned_kwargs = {}
        operator_lookup = {}

        ## MAP THE QUERY PARAMETER WITH ITS OPERATOR, TO THE DB MODEL ##
        for param in query_dict.keys():

            try:
                operator_lookup[param[0:param.index('__')]] = param
            except ValueError:
                operator_lookup[param] = param

        ## ONLY WANT TO CLEAN KWARGS FOR COLUMNS THAT EXISTS FOR THIS MODEL ##
        db_model_keys = list(set(self.db_obj._meta.get_all_field_names()).\
            intersection(set(k for k in operator_lookup.keys())))

        ## FINALLY CREATE ONE DICT (cleaned_kwargs) WITH THE ORIGINAL K,V ##
        ## IN THE URL, BUT FILTERED ON COLUMNS AVAILABLE TO THE MODEL ##
        for k in db_model_keys:

            query_key = operator_lookup[k]
            query_value = query_dict[operator_lookup[k]]#[]

            if "," in query_value:
                cleaned_kwargs[query_key] = query_value.split(',')
            else:
                cleaned_kwargs[query_key] = query_value

        ## FIND THE LIMIT AND OFFSET AND STORE AS CLASS ATTRIBUETS ##
        try:
            self.limit = int(query_dict['limit'])
        except KeyError:
            self.limit = 1000000000

        try:
            self.offset = int(query_dict['offset'])
        except KeyError:
            self.offset = 0

        ## Find the Read/Write param for regions ( see POLIO-779 ) ##

        try:
            self.read_write = query_dict['read_write']
        except KeyError:
            self.read_write = 'r'

        print self.read_write

        return cleaned_kwargs


    def build_meta(self):
        '''
        '''

        meta_dict = {
            'limit': self.limit,
            'offset': self.offset,
            'total_count': self.full_data_length,
        }

        return meta_dict


    def apply_permissions(self, queryset):
        '''
        Right now this is only for regions and Datapoints.

        Returns a Raw Queryset
        '''

        if not self.permission_function:
            return None, queryset

        ## if filters then create that list of IDs, otherwise pass ##
        ## None, and the permissions function wont filter on an ID list ##
        if not queryset:
            list_of_object_ids = None
        else:
            list_of_object_ids = [x['id'] for x in queryset]

        err, data = self.permission_function(list_of_object_ids)

        return err, data


    def serialize(self, data):

        serialized = [self.clean_row_result(row) for row in data]

        return None, serialized

    def clean_row_result(self, row_data):
        '''
        When Serializing, everything but Int and List are converted to string.
        In this case the List (in the case of indicators), is a json array.

        If it is a raw queryset, first convert the row to a dict using the
        built in __dict__ method.

        This just returns a list of dict.  The JsonResponse in the view
        does the actual json conversion.
        '''

        cleaned_row_data = {}

        # if raw queryset, convert to dict
        if isinstance(row_data,Model):
            row_data = dict(row_data.__dict__)

        for k,v in row_data.iteritems():
            if isinstance(v, int):
                cleaned_row_data[k] = v
            if 'json' in k: # if k == 'bound_json':
                cleaned_row_data[k] = json.loads(v)
            else:
                cleaned_row_data[k] = smart_str(v)

        return cleaned_row_data

    ## permissions functions ##

    def apply_region_permissions(self, list_of_object_ids):
        '''
        This returns a raw queryset, that is the query itself isn't actually
        executed until the data is unpacked in the serialize method.

        For more information on how region permissions work, take a look
        at the definition of the stored proc called below.
        '''

        print '==\n' * 5
        print self.request.user.id
        print '==\n' * 5

        data = Region.objects.raw("SELECT * FROM\
            fn_get_authorized_regions_by_user(%s,%s,%s)",[self.request.user.id,
            list_of_object_ids,self.read_write])

        return None, data

    def apply_campaign_permissions(self, list_of_object_ids):
        '''
        As in above, this returns a raw queryset, and will be executed in the
        serialize method.

        The below query reads: "show me all campaigns that have data for
        regions that I am permitted to see."

        No need to do recursion here, because the data is already aggregated
         regionally when ingested into the datapoint_abstracted table.
        '''

        data = Campaign.objects.raw("""
            SELECT c.* FROM campaign c
            INNER JOIN datapoint_abstracted da
                ON c.id = da.campaign_id
            INNER JOIN region_permission rm
                ON da.region_id = rm.region_id
                AND rm.user_id = %s
            WHERE c.id = ANY(COALESCE(%s,ARRAY[c.id]))
        """, [self.user_id, list_of_object_ids])

        return None, data
