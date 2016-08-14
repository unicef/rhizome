from pandas import DataFrame

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models.campaign_models import DataPointComputed
from rhizome.models.document_models import SourceObjectMap, \
    DocumentSourceObjectMap
from rhizome.models.location_models import LocationTree
from rhizome.models.indicator_models import CalculatedIndicatorComponent

class CampaignDocResultResource(BaseModelResource):
    '''
    **GET Request** Returns all doc_detail_type objects
        - *Required Parameters:*
                    None
    '''
    class Meta(BaseModelResource.Meta):
        object_class = DataPointComputed
        resource_name = 'campaign_doc_result'
        GET_fields = ['indicator__id', 'location__name',\
            'indicator__short_name', 'campaign__name', 'value']
        GET_params_required = ['document_id']

    def apply_filters(self, request, applicable_filters):
        """
        """

        document_id = request.GET.get('document_id', None)
        source_object_map_id_list = DocumentSourceObjectMap.objects\
            .filter(document_id = document_id)\
            .values_list('source_object_map_id', flat=True)

        q_columns = ['master_object_id', 'content_type']
        som_df = DataFrame(list(SourceObjectMap.objects\
            .filter(id__in = source_object_map_id_list, master_object_id__gt=0)\
            .values_list(*q_columns)),columns = q_columns)

        campaign_id_list = list(som_df[som_df['content_type'] == \
            'campaign']['master_object_id'].unique())
        indicator_id_list = list(som_df[som_df['content_type'] == \
            'indicator']['master_object_id'].unique())
        raw_location_id_list = som_df[som_df['content_type'] == \
            'location']['master_object_id'].unique()
        ## don't just get the locations from the document, get the parents ##
        all_location_id_list = list(set(LocationTree.objects.filter(
            location_id__in = raw_location_id_list)\
            .values_list('parent_location_id',flat=True)))

        ## don't just get the indicators from the document, get the calculations ##
        calc_indicator_id_list = list(set(CalculatedIndicatorComponent\
            .objects.filter(indicator_component_id__in = indicator_id_list)\
            .values_list('indicator_id',flat=True)))

        indicator_id_list.extend(calc_indicator_id_list)

        ## FIXME need some sort of unique_ix here like we have in datapoints #
        ## FIXME this needs test coverage
        kwargs = {
            'indicator_id__in': indicator_id_list,
            'campaign_id__in': campaign_id_list,
            'location_id__in': all_location_id_list
        }

        return self.get_object_list(request)\
            .filter(**kwargs)
