from tastypie.resources import ModelResource,Resource, ALL
from tastypie import fields

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from datapoints.api.base import BaseApiResource
from datapoints.models import *

import pprint as pp


class OfficeResource(BaseApiResource):
    '''Office Resource'''


    class Meta(BaseApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'


class RegionResource(ModelResource):
    '''Region Resource'''

    # parent_region = fields.ForeignKey('datapoints.api.meta_data.RegionResource', 'parent_region', full=True, null=True)
    # name = fields.CharField('name')


    class Meta():
        # queryset = Region.objects.raw("Select id, parent_region_id, name from region")
        queryset = SimpleRegion.objects.all()
        resource_name = 'region'
        max_limit = None # return all rows by default ( limit defaults to 20 )
        # paginator_class = CustomPaginator

    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri",None)# = bundle.obj.region.id
        return bundle

class RegionPolygonResource(BaseApiResource):

    region_id = fields.ForeignKey(RegionResource,'region')

    class Meta(BaseApiResource.Meta):
        queryset = RegionPolygon.objects.all()
        resource_name = 'polygon'
        filtering = {
            "region_id": ALL,
        }

    def dehydrate(self, bundle):

        bundle.data['region_id'] = bundle.obj.region.id

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
