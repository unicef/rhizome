

from django.contrib.auth.models import User

from datapoints.models import Region, Campaign, Indicator, DataPointAbstracted


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

        return cleaned_kwargs


    def object_lookup(self,content_type_string):

        orm_mapping = {
            'datapoint': DataPointAbstracted,
            'region': Region,
            'campaign': Campaign,
            'indicator': Indicator,
            'user': User,
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

        list_of_ids = list(self.db_obj.objects.all().values_list('id',flat=True).\
            filter(**self.kwargs))

        filtered_data = self.apply_permissions(list_of_ids)

        data = self.serialize(filtered_data)

        return None, data

    def apply_permissions(self, data):

        return data

    def serialize(self, data):

        return data



## SAMPLE GET ##
# http://localhost:8000/api/v2/get/indicator/?name__contains=polio
# http://localhost:8000/api/v2/get/indicator/?name__startswith=Polio

## SAMPLE POST ##
# http://localhost:8000/api/v2/post/campaign/?start_date=2016-01-01&end_date=2016-01-01&office_id=1&campaign_type_id=1

## MULTIPLE MODELS ##
# http://localhost:8000/api/v2/post/indicator/?name=test2&source_id=1&mx_val=1&bound_name=juvenile #
