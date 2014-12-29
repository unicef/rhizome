from tastypie.resources import ModelResource, ALL
from tastypie import fields

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from datapoints.api.base import BaseApiResource
from datapoints.models import *



class OfficeResource(BaseApiResource):
    '''Office Resource'''


    class Meta(BaseApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'



class RegionResource(BaseApiResource):
    '''Region Resource'''

    parent_region = fields.ForeignKey('datapoints.api.meta_data.RegionResource', 'parent_region', full=False, null=True)
    office = fields.ToOneField(OfficeResource, 'office')


    class Meta(BaseApiResource.Meta):
        queryset = Region.objects.all()
        resource_name = 'region'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
            "office": ALL,
            "region_type": ALL,
        }

    def dehydrate(self, bundle):

        bundle.data['office'] = bundle.obj.office.id

        try:
            bundle.data['parent_region'] = bundle.obj.parent_region.id
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass

        return bundle



class IndicatorResource(BaseApiResource):
    '''Indicator Resource'''

    class Meta(BaseApiResource.Meta):
        queryset = Indicator.objects.all()
        resource_name = 'indicator'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
        }

class CampaignResource(BaseApiResource):
    '''Campaign Resource'''

    office = fields.ToOneField(OfficeResource, 'office')


    class Meta(BaseApiResource.Meta):
        queryset = Campaign.objects.all()
        resource_name = 'campaign'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
            "office": ALL,
        }

    def dehydrate(self, bundle):

        bundle.data['office'] = bundle.obj.office.id

        return bundle

class UserResource(BaseApiResource):
    '''User Resource'''

    class Meta(BaseApiResource.Meta):
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'username']
        allowed_methods = ['get']
