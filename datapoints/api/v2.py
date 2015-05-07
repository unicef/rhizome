import json
import datetime

from django.core.serializers import json as djangojson
from django.utils.encoding import force_text
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.core import serializers
from tastypie.resources import Resource

from datapoints.models import *


class v2Request(Resource):

    def __init__(self,request, content_type):

        self.request = request
        self.content_type = content_type
        self.user_id = request.user.id

        self.db_obj = self.object_lookup(content_type)
        self.kwargs = self.clean_kwargs(request.GET)  ## CHANGE TO POST ##


    def clean_kwargs(self,query_dict):

        cleaned_kwargs = {}

        for k,v in query_dict.iteritems():

            if "," in v:
                cleaned_kwargs[k] = v.split(',')
            else:
                cleaned_kwargs[k] = v


        ## YOU NEED TO FIND THE COLUMNS OF THE OBJECT AND INTERSECT THAT ##
        # del cleaned_kwargs['format']
        # del cleaned_kwargs['offset']
        # del cleaned_kwargs['uri_display']

        return cleaned_kwargs


    def object_lookup(self,content_type_string):

        orm_mapping = {
            'datapoint': DataPointAbstracted,
            'region': Region,
            'campaign': Campaign,
            'indicator': Indicator,
            'user': User,
            'office': Office,
            'campaign_type': CampaignType,
        }

        db_model = orm_mapping[content_type_string]

        return db_model


class v2PostRequest(v2Request):


    def main(self):
        '''
        Create an object in accordance to the URL kwargs and return the new ID
        '''

        new_obj = self.db_obj.objects.create(**self.kwargs)

        data = {'new_id':new_obj.id }

        return None, data



class v2GetRequest(v2Request):

    def main(self):
        '''
        Get the list of database objects ( ids ) by applying the URL kwargs to
        the filter method of the djanog ORM.
        '''

        qset = list(self.db_obj.objects.all().filter(**self.kwargs).values())

        filtered_data = self.apply_permissions(qset)

        data = self.serialize(filtered_data)

        return None, data

    def apply_permissions(self, queryset):
        '''
        Right now this is only for regions and Datapoints.

        Returns a Raw Queryset
        '''

        if self.content_type == 'region':

            list_of_object_ids = [x['id'] for x in queryset]

            data = Region.objects.raw("SELECT * FROM\
                fn_get_authorized_regions_by_user(%s,%s)",[self.request.user.id,\
                list_of_object_ids])

            ## THIS SHOULD BE ABSTRACTED ##
            list_of_dicts = [{\
                'id' : row.id,
                'name' : row.name,
                'parent_region_id' : row.name,
                'region_type_id' : row.region_type_id,
                } for row in data]

            return list_of_dicts #list_of_dicts

        else:
             return queryset



    def serialize(self, data):


        print type(data)
        json_data = self.to_json(data)

        return data


    def to_json(self, data, options=None):
        """
        Given some Python data, produces JSON output.

        This is taken from tastypie source
        """
        options = options or {}
        data = self.to_simple(data, options)

        return djangojson.json.dumps(data, cls=djangojson.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False)

    def to_simple(self, data, options):
        """
        For a piece of data, attempts to recognize it and provide a simplified
        form of something complex.
        This brings complex Python data structures down to native types of the
        serialization format(s).
        """
        if isinstance(data, (list, tuple)):
            return [self.to_simple(item, options) for item in data]
        if isinstance(data, dict):
            return dict((key, self.to_simple(val, options)) for (key, val) in data.items())
        # elif isinstance(data, Bundle):
        #     return dict((key, self.to_simple(val, options)) for (key, val) in data.data.items())
        elif hasattr(data, 'dehydrated_type'):
            if getattr(data, 'dehydrated_type', None) == 'related' and data.is_m2m == False:
                if data.full:
                    return self.to_simple(data.fk_resource, options)
                else:
                    return self.to_simple(data.value, options)
            elif getattr(data, 'dehydrated_type', None) == 'related' and data.is_m2m == True:
                # if data.full:
                #     return [self.to_simple(bundle, options) for bundle in data.m2m_bundles]
                # else:
                return [self.to_simple(val, options) for val in data.value]
            else:
                return self.to_simple(data.value, options)
        elif isinstance(data, datetime):
            return self.format_datetime(data)
        # elif isinstance(data, datetime.date):
        #     return self.format_date(data)
        # elif isinstance(data, datetime.time):
        #     return self.format_time(data)
        elif isinstance(data, bool):
            return data
        # elif isinstance(data, (six.integer_types, float)):
        #     return data
        elif data is None:
            return None
        else:
            return force_text(data)



## SAMPLE GET ##
# http://localhost:8000/api/v2/get/indicator/?name__contains=polio
# http://localhost:8000/api/v2/get/indicator/?name__startswith=Polio

## SAMPLE POST ##
# http://localhost:8000/api/v2/post/campaign/?start_date=2016-01-01&end_date=2016-01-01&office_id=1&campaign_type_id=1

## MULTIPLE MODELS ##
# http://localhost:8000/api/v2/post/indicator/?name=test2&source_id=1&mx_val=1&bound_name=juvenile #
