import json
import datetime

from django.core.serializers import json as djangojson
from django.utils.encoding import force_text
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.core import serializers

from tastypie.utils import format_datetime, make_naive

from datapoints.models import *


class v2Request(object):

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

        qset = list(self.db_obj.objects.all()[:2].filter(**self.kwargs).values())

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

        json_data = self.v2_serializer(data)

        return json_data


    def v2_serializer(self, data):
        """
        For a piece of data, attempts to recognize it and provide a simplified
        form of something complex.
        This brings complex Python data structures down to native types of the
        serialization format(s).
        """

        serialized = []
        for row in data:
            cleaned_dict = {}
            for k,v in row.iteritems():
                if isinstance(v, datetime):

                    cleaned_dict[k] = 1#self.format_datetime(v)
                else:
                    cleaned_dict[k] = (v)
            serialized.append(cleaned_dict)

        return serialized


    def format_datetime(self, data):
        """
        A hook to control how datetimes are formatted.
        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).
        Default is ``iso-8601``, which looks like "2010-12-16T03:02:14".
        """

        print '???'

        return data.isoformat()()


## SAMPLE GET ##
# http://localhost:8000/api/v2/indicator/?name__contains=polio
# http://localhost:8000/api/v2/indicator/?name__startswith=Polio

## SAMPLE POST ##
# http://localhost:8000/api/v2/campaign/?start_date=2016-01-01&end_date=2016-01-01&office_id=1&campaign_type_id=1

## MULTIPLE MODELS ##
# http://localhost:8000/api/v2/post/indicator/?name=test2&source_id=1&mx_val=1&bound_name=juvenile #
