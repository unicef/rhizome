from datapoints.api.resources.base_model import BaseModelResource
from datapoints.models import DocDataPoint, DataPoint
from datapoints.agg_tasks import AggRefresh

from source_data.models import DocumentDetail, DocDetailType, SourceSubmission
from source_data.etl_tasks.refresh_master import MasterRefresh

class RefreshMasterResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_master'

    def get_object_list(self, request):
        document_id = request.GET['document_id']

        mr = MasterRefresh(request.user.id, document_id)
        mr.main()

        ar = AggRefresh()

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType.objects.get(name='submission_processed_count').id,
            defaults={
                'doc_detail_value': SourceSubmission.objects.filter(
                    process_status='PROCESSED',
                    document_id=document_id).count()
            },
        )

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType.objects.get(name='doc_datapoint_count').id,
            defaults={
                'doc_detail_value': DocDataPoint.objects.filter(document_id=document_id).count()
            },
        )

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType.objects.get(name='datapoint_count').id,
            defaults={
                'doc_detail_value': DataPoint.objects.filter(
                    source_submission_id__in=SourceSubmission.objects.filter(
                        document_id=document_id).values_list('id', flat=True)).count()
            },
        )

        queryset = DocumentDetail.objects \
            .filter(document_id=document_id).values('id','doc_detail_type_id'\
                ,'doc_detail_type__name','document_id', 'doc_detail_value')

        return queryset
