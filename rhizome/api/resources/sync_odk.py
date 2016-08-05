from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.api.exceptions import RhizomeApiException

from rhizome.models.document_models import Document
from rhizome.simple_models import DocumentDetail, SourceSubmission
from rhizome.etl_tasks.sync_odk import OdkSync
from rhizome.etl_tasks.sync_odk import OdkJarFileException


class SyncOdkResource(BaseNonModelResource):

    class Meta(BaseNonModelResource.Meta):
        resource_name = 'sync_odk'
        queryset = SourceSubmission.objects.all().values()
        default_limit = 10
        GET_params_required = ['odk_form_id']

    def pre_process_data(self, request):
        """
        Specific to interfacing with ODK aggregate deployed on google app
        engine, in which it is necessary to run a java app in order to
        build the connection to the server and pull the data.

        NOTE: if you want to interface with other ODK aggregate backends,
        for instance ONA or formhub, you would build your data interface
        here.
        """

        pass

        # odk_form_id = request.GET.get('odk_form_id', None)
        # document_id = request.GET.get('document_id', None)
        #
        # if not odk_form_id:
        #     try:
        #         odk_form_id = DocumentDetail.objects.get(**{
        #                 'document_id':document_id,
        #                 'doc_detail_type__name':'odk_form_name'
        #             }).doc_detail_value
        #     except DocumentDetail.DoesNotExist:
        #         raise RhizomeApiException(
        #             '"{0}" is a required parameter for this request'\
        #             .format(required_param))
        # try:
        #     odk_sync_object = OdkSync(
        #         odk_form_id, ** {'user_id': request.user.id})
        #     document_id_list, sync_result_data = odk_sync_object.main()
        #
        # except OdkJarFileException as e:
        #     raise RhizomeApiException(e.errorMessage)
