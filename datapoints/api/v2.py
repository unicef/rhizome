import json
import datetime

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


class v2Request(object):

    def __init__(self, requestpep8, content_type):

        self.request = request
        self.content_type = content_type
        self.user_id = request.user.id

        self.orm_mapping = {
            'indicator': {'orm_obj':Indicator, 'permission_function':None},
            'campaign': {'orm_obj':Campaign , \
                'permission_function':self.apply_campaign_permissions},
            'region': {'orm_obj':Region, \
                'permission_function':self.apply_region_permissions},
            'group': {'orm_obj':Group, 'permission_function':None},
            'user': {'orm_obj':User, 'permission_function':None},
        }

        self.db_obj = self.orm_mapping[content_type]['orm_obj']
        self.db_columns = self.db_obj._meta.get_all_field_names()
        self.permission_function = self.orm_mapping[content_type]\
            ['permission_function']

        self.kwargs = self.clean_kwargs(request.GET)  ## What about POST? ##



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
        db_model_keys = list(set(self.db_columns).intersection(set(k for k in\
            operator_lookup.keys())))

        ## FINALLY CREATE ONE DICT (cleaned_kwargs) WITH THE ORIGINAL K,V ##
        ## IN THE URL, BUT FILTERED ON COLUMNS AVAILABLE TO THE MODEL ##
        for k in db_model_keys:

            query_key = operator_lookup[k]
            query_value = query_dict[operator_lookup[k]]#[]

            if "," in query_value:
                cleaned_kwargs[query_key] = query_value.split(',')
            else:
                cleaned_kwargs[query_key] = query_value

        return cleaned_kwargs



class v2PostRequest(v2Request):


    def main(self):
        '''
        Create an object in accordance to the URL kwargs and return the new ID
        '''

        new_obj = self.db_obj.objects.create(**self.kwargs)

        data = {'new_id':new_obj.id }

        return None, data


class v2MetaRequest(v2Request):

    def main(self):

        self.meta_data = {}
        self.all_field_meta = []
        self.add_model_meta_data()

        ## BUILD METADATA FOR EACH FIELD ##
        for ix,(field) in enumerate(self.db_obj._meta.get_all_field_names()):
            self.build_field_meta_dict(field,ix)

        self.meta_data['fields'] = self.all_field_meta

        return None, self.meta_data

    def build_field_meta_dict(self, field, ix):

        try:
            field_object = self.db_obj._meta.get_field(field)
        except FieldDoesNotExist:
            return None

        ## DICT TO MAP DJANNGO FIELD DEFINITION TO THE TYPES THE FE EXPECTS ##
        field_type_mapper = {'AutoField':'number','FloatField':'number',
            'ForeignKey':'list','CharField':'string','ManyToManyField':'list',
            'DateTimeField':'datetime','DateField':'datetime','BooleanField':
            'boolean','SlugField':'string'}

        ## BUILD A DICTIONARY FOR EACH FIELD ##
        field_object_dict = {
            'name': field_object.name,
            'title': field_object.name,
            'type': field_type_mapper[field_object.get_internal_type()],
            'max_length': field_object.max_length,
            'editable' : field_object.editable,
            'default_value' : str(field_object.get_default()),
                'display' : {
                    'on_table':True,
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


    def add_model_meta_data(self):

        self.meta_data['slug'] = self.content_type
        self.meta_data['name'] = self.content_type
        self.meta_data['primary_key'] = 'id'
        self.meta_data['search_field'] = 'slug'
        self.meta_data['defaultSortField'] = 'id'
        self.meta_data['defaultSortDirection'] = 'asc'


class v2GetRequest(v2Request):


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
            qset = list(self.db_obj.objects.all().filter(**self.kwargs).values())

        err, filtered_data = self.apply_permissions(qset)
        err, data = self.serialize(filtered_data)

        return None, data

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
        When Serializing, everything but Int is converted to string.

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
            else:
                cleaned_row_data[k] = smart_str(v)

        return cleaned_row_data


    def apply_region_permissions(self, list_of_object_ids):
        '''
        This returns a raw queryset, that is the query itself isn't actually
        executed until the data is unpacked in the serialize method.

        For more information on how region permissions work, take a look
        at the definition of the stored proc called below.
        '''

        data = Region.objects.raw("SELECT * FROM\
            fn_get_authorized_regions_by_user(%s,%s)",[self.request.user.id,
            list_of_object_ids])

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
