from datapoints.api.resources.base_model import BaseModelResource
from datapoints.api.exceptions import DatapointsException

from source_data.models import DocumentDetail, Document
from source_data.etl_tasks.sync_odk import OdkSync
from source_data.etl_tasks.sync_odk import OdkJarFileException



class SyncOdkResource(BaseModelResource):
    def get_object_list(self, request):

        required_param = 'odk_form_id'
        odk_form_id = None

        try:
            odk_form_id = request.GET[required_param]
        except KeyError:
            pass

        try:
            document_id = request.GET['document_id']
            odk_form_id = DocumentDetail.objects.get(
                document_id = document_id, doc_detail_type__name = 'odk_form_name'
            ).doc_detail_value
        except KeyError:
            pass

        if not odk_form_id:
            raise DatapointsException('"{0}" is a required parameter for this request'.format(required_param))

        try:
            odk_sync_object = OdkSync(odk_form_id, **{'user_id':request.user.id})
            document_id_list, sync_result_data = odk_sync_object.main()

        except OdkJarFileException as e:
            raise DatapointsException(e.errorMessage)

        return Document.objects.filter(id__in=document_id_list).values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'sync_odk'
