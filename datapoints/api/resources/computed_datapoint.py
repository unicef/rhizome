from datapoints.api.resources.base_model import BaseModelResource
from datapoints.models import DataPointComputed
from source_data.models import SourceObjectMap, DocumentSourceObjectMap

class ComputedDataPointResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'computed_datapoint'

    def get_object_list(self, request):

        try:
            document_id = request.GET['document_id']
        except KeyError:
            document_id = None

        try:
            campaign_id = request.GET['campaign_id']
        except KeyError:
            campaign_id = None

        try:
            location_id = request.GET['location_id']
        except KeyError:
            location_id = None

        som_ids = DocumentSourceObjectMap.objects.filter(
            document_id=document_id,
        ).values_list('source_object_map_id', flat=True)

        indicator_id_list = list(SourceObjectMap.objects.filter(
            id__in=som_ids,
            content_type='indicator',
            master_object_id__gt=0,
        ).values_list('master_object_id', flat=True))

        queryset = DataPointComputed.objects.filter(
            location_id=location_id,
            campaign_id=campaign_id,
            indicator_id__in=indicator_id_list
        ).values('indicator_id', 'indicator__short_name', 'value')

        return queryset

