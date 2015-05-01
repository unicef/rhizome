

from django.contrib.auth.models import User

from datapoints.models import Region, Campaign, Indicator


class v2Request(object):


    def __init__(self,request, content_type):

        self.request = request
        self.content_type = content_type

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
            'region': Region,
            'campaign': Campaign,
            'indicator': Indicator,
            'user': User,
        }

        db_model = orm_mapping[content_type_string]

        return db_model


class v2PostRequest(v2Request):

    def __int__(self):

        return super()


    def main(self):

        db_obj = self.object_lookup(self.content_type)
        kwargs = clean_kwargs(self.request.GET)  ## CHANGE TO POST ##

        new_obj = db_obj.objects.create(**kwargs)

        data = {'new_id':new_obj.id }

        return data

class v2GetRequest(v2Request):


    def main(self):

        db_obj = self.object_lookup(self.content_type)
        kwargs = self.clean_kwargs(self.request.GET)

        qs = db_obj.objects.all().values_list('id',flat=True).filter(**kwargs)

        data = list(qs)

        return data



## SAMPLE GET ##
# http://localhost:8000/api/v2/get/indicator/?name__contains=polio
# http://localhost:8000/api/v2/get/indicator/?name__startswith=Polio

## SAMPLE POST ##
# http://localhost:8000/api/v2/post/campaign/?start_date=2016-01-01&end_date=2016-01-01&office_id=1&campaign_type_id=1

## MULTIPLE MODELS ##
# http://localhost:8000/api/v2/post/indicator/?name=test2&source_id=1&mx_val=1&bound_name=juvenile #
