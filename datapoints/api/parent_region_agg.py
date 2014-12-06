

class ParentRegionAggResource(SimpleApiResource):

    parent_region = fields.ToOneField(RegionResource, 'parent_region')
    indicator = fields.ToOneField(IndicatorResource, 'indicator')
    campaign = fields.ToOneField(CampaignResource, 'campaign')


    class Meta(SimpleApiResource.Meta):
        queryset = ParentRegionAgg.objects.all()
        resource_name = 'parent_region_agg'
        filtering = {
            "indicator": ALL,
            "parent_region":ALL,
            "campaign":ALL,
        }
        allowed_methods = ['get']
        serializer = CustomSerializer()
        max_limit = None

    # def dehydrate(self, bundle):
    #     ''' overriden from tastypie '''
    #     return bundle

    def obj_get_list(self, bundle, **kwargs):
        ''' overriden from tastypie '''

        return self.get_object_list(bundle.request)

    def get_object_list(self, request):

        query_dict = request.GET
        query_kwargs = self.parse_query_params(query_dict)

        object_list = ParentRegionAgg.objects.filter(**query_kwargs)

        return object_list

    def parse_query_params(self,query_dict):

        query_kwargs = {}

        try:
            indicator__in = query_dict['indicator__in'].split(',')
            query_kwargs['indicator__in'] = indicator__in
        except KeyError:
            pass

        try:
            campaign__in = query_dict['campaign__in'].split(',')
            query_kwargs['campaign__in'] = campaign__in
        except KeyError:
            pass

        try:
            parent_region = query_dict['parent_region']
            query_kwargs['parent_region'] = parent_region
        except KeyError:
            pass


        return query_kwargs

    def dehydrate(self, bundle):
        '''
        # Depending on the <uri_display> parameter, return to the bundle
        # the name, resurce_uri, slug or ID of the resource
        # '''

        fk_columns = {'indicator':bundle.obj.indicator,\
            'campaign':bundle.obj.campaign,\
            'parent_region':bundle.obj.parent_region}


        try: # Default to showing the ID of the resource
            uri_display = bundle.request.GET['uri_display']
        except KeyError:
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj
            return bundle


        if uri_display == 'slug':
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj.slug

        elif uri_display == 'id':
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj.id


        elif uri_display == 'name':
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj.name

        else: # if there is any other uri_display, return the full uri
            pass



        return bundle
