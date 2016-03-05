from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DocumentDetail

class DocumentDetailResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_detail'
        filtering = {
            "id": ALL,
            "document": ALL,
        }

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        defaults = {
            'doc_detail_value': post_data['doc_detail_value'],
        }

        chart, created = DocumentDetail.objects.update_or_create(
            document_id=post_data['document_id'],
            doc_detail_type_id=post_data['doc_detail_type_id'],
            defaults=defaults
        )

        bundle.obj = chart
        bundle.data['id'] = chart.id

        return bundle

    def get_object_list(self, request):

        try:
            doc_detail_type = request.GET['doc_detail_type']
            return  DocumentDetail.objects\
                .filter(doc_detail_type__name=doc_detail_type)\
                .values('id','doc_detail_type_id','doc_detail_type__name',\
                    'document_id', 'doc_detail_value')
        except KeyError:
            pass

        try:
            doc_id = request.GET['document_id']
            return  DocumentDetail.objects\
                .filter(document_id=doc_id)\
                .values('id','doc_detail_type_id','doc_detail_type__name',\
                    'document_id', 'doc_detail_value')
        except KeyError:
            return DocumentDetail.objects.all()\
                .values('id','doc_detail_type_id','doc_detail_type__name',\
                'document_id', 'doc_detail_value')

