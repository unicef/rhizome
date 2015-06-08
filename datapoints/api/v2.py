import json
import datetime
import traceback
from pprint import pprint
from collections import defaultdict

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

        # Tells the API which models are avail for GET / POST / META requests #
        self.orm_mapping = {
            'campaign': {'orm_obj':Campaign,
                'permission_function':self.apply_campaign_permissions},
            'region': {'orm_obj':Region,
                'permission_function':self.apply_region_permissions},
            'document_review' : {'orm_obj':DocumentDetail,
                'permission_function': self.group_document_metadata},
            'indicator': {'orm_obj':IndicatorAbstracted,
                'permission_function':self.apply_indicator_permissions},
            'group': {'orm_obj':Group,
                'permission_function':None},
            'user': {'orm_obj':User,
                'permission_function':None},
            'region_permission': {'orm_obj':RegionPermission,
                'permission_function':None},
            'user_group': {'orm_obj':UserGroup,
                'permission_function':None},
            'document': {'orm_obj':Document,
                'permission_function':None},
            'office': {'orm_obj':Office,
                'permission_function':None},
            'indicator_map': {'orm_obj':IndicatorMap,
                'permission_function':None},
            'region_map': {'orm_obj':RegionMap,
                'permission_function':None},
            'campaign_map': {'orm_obj':CampaignMap,
                'permission_function':None},
            'indicator_tag': {'orm_obj':IndicatorTag,
                'permission_function':None},
            'campaign_type': {'orm_obj':CampaignType,
                'permission_function':None}
        }


    def main(self):

        response_data = {
            'objects':self.data,
            'meta':self.meta,
            'error':self.err,
        }

        return response_data

    ## permissions functions ##

    def apply_region_permissions(self, list_of_object_ids):
        '''
        This returns a raw queryset, that is the query itself isn't actually
        executed until the data is unpacked in the serialize method.

        For more information on how region permissions work, take a look
        at the definition of the stored proc called below.
        '''

        data = Region.objects.raw("SELECT * FROM\
            fn_get_authorized_regions_by_user(%s,%s,%s,%s)",[self.request.user.id,
            list_of_object_ids,self.read_write,self.depth_level])

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
            SELECT DISTINCT c.* FROM campaign c
            INNER JOIN datapoint_abstracted da
                ON c.id = da.campaign_id
            INNER JOIN region_permission rm
                ON da.region_id = rm.region_id
                AND rm.user_id = %s
            WHERE c.id = ANY(COALESCE(%s,ARRAY[c.id]))
            ORDER BY c.start_date DESC
        """, [self.user_id, list_of_object_ids])

        return None, data

    def apply_indicator_permissions(self, list_of_object_ids):
        '''
        '''

        if self.read_write == 'r':

            data = IndicatorAbstracted.objects.raw("""
                SELECT ia.*
                FROM indicator_abstracted ia
                WHERE 1=1
                AND ia.id = ANY(COALESCE(%s,ARRAY[ia.id]))
            """,[list_of_object_ids])

        else:
            data = IndicatorAbstracted.objects.raw("""
                SELECT ia.*
                FROM indicator_abstracted ia
                WHERE 1=1
                AND ia.id = ANY(COALESCE(%s,ARRAY[ia.id]))
                AND EXISTS (
                	SELECT * FROM auth_user_groups aug
                	INNER JOIN indicator_permission gp
                	ON aug.group_id = gp.group_id
                	AND ia.id = gp.indicator_id
                	AND aug.user_id = %s
                )
            """,[list_of_object_ids,self.user_id])

        return None, data


    def group_document_metadata(self,list_of_object_ids):
        '''
        This function is not actually about permissions, but rather data
        manipulation needed for the front end.  Here i create three nodes
        (region, campaign, indicator) and add all metadata here.
        '''

        raw_data = DocumentDetail.objects.raw("""
            SELECT * FROM
            document_detail dd
            WHERE dd.id = ANY(COALESCE(%s,ARRAY[-1]))
        """,[list_of_object_ids]
        )

        cleaned_data = {
            'region':[],
            'campaign':[],
            'indicator':[],
        }

        for row in raw_data:

            row_dict = dict(row.__dict__)
            del row_dict['_state']

            cleaned_data[row.db_model].append(row_dict)

        return None, cleaned_data


class v2PostRequest(v2Request):


    def __init__(self, request, content_type):

        super(v2PostRequest, self).__init__(request, content_type)

        ## DB obj can be different between GET and POST requests ##
        self.orm_mapping['indicator']['orm_obj'] = Indicator

        ## find the DB obj we want to POST to
        self.db_obj = self.orm_mapping[content_type]['orm_obj']

        ## klean URL parameters
        self.kwargs = self.clean_kwargs(request.POST)

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
        Return error if not implemented

        if method is create:
        Create an object in accordance to the URL kwargs and return the new ID

        if delete:
            query for objects taht match
        '''

        if self.content_type == 'user':

            self.err = 'User POST not implemented in v2 api.'
            return super(v2PostRequest, self).main()

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

        super(v2MetaRequest, self).__init__(request, content_type)
        self.db_obj = self.orm_mapping[content_type]['orm_obj']


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

        ## url_patterns ##
        self.url_patterns = {
            'create': "datapoints/" + self.content_type + "s/create",
            'update': "datapoints/" + self.content_type + "s/update/?<id>/"

        }
        self.data['fields'] = self.all_field_meta
        self.data['url_patterns'] = self.url_patterns

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

        super(v2GetRequest, self).__init__(request, content_type)

        self.db_obj = self.orm_mapping[content_type]['orm_obj']
        self.permission_function = self.orm_mapping[content_type]\
            ['permission_function']

        self.kwargs = self.clean_kwargs(request.GET)


    def main(self):
        '''
        Get the list of database objects ( ids ) by applying the URL kwargs to
        the filter method of the djanog ORM.
        '''

        # for a get request.. dont show an ids < 0 ( see POLIO-856 ) #
        self.kwargs['id__gt'] = 0

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

        try:
            self.data = data[self.offset:self.limit + self.offset]
        except TypeError:
            self.data = data

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


        ## Find the Depth Level param ( see POLIO-839 ) ##

        try:
            self.depth_level = query_dict['depth_level']
        except KeyError:
            self.depth_level = 10

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
        '''
        document_review has a custom serialization in which 'region', 'campaign'
        and 'indicator' are keys and the value is a list of the cooresponding
        mappings.  This needs to be cleaned up, but for now that content
        type skips through the serialization method.

        '''

        if self.content_type != 'document_review':
            serialized = [self.clean_row_result(row) for row in data]

            return None, serialized

        else:
            return None, data



    def clean_row_result(self, row_data):
        '''
        When Serializing, everything but Int and List are converted to string.
        In this case the List (in the case of indicators), is a json array.

        If it is a raw queryset, first convert the row to a dict using the
        built in __dict__ method.

        This just returns a list of dict.  The JsonResponse in the view
        does the actual json conversion.

        Also get rid of the _state attribute ( see POLIO-801)

        '''


        cleaned_row_data = {}

        # if raw queryset, convert to dict
        if isinstance(row_data,Model):
            row_data = dict(row_data.__dict__)
            del row_data['_state']

        for k,v in row_data.iteritems():
            if isinstance(v, int):
                cleaned_row_data[k] = v
            elif not v:
                cleaned_row_data[k] = None
            elif k in ['longitude','latitude']:
                cleaned_row_data[k] = float(v)
            elif 'json' in k: # if k == 'bound_json':
                cleaned_row_data[k] =v  # json.loads(v)
                pass
            else:
                cleaned_row_data[k] = smart_str(v)

        return cleaned_row_data
