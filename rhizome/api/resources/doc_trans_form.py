from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import DatapointsException
from rhizome.models import Document, DataPoint, SourceSubmission
# from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform
from rhizome.etl_tasks.transform_upload import ComplexDocTransform, DateDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh
from django.db import transaction
from django.db.transaction import TransactionManagementError

class DocTransFormResource(BaseModelResource):
    '''
    '''
    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

    def get_object_list(self, request):
        '''

        ## when you upload a file, step one is getting data into source submission
            ## --> DocTransform <-- ##

        ## Step two is translating form source_submission into datapoints
            ## --> REfreshMaster <----

        ## step three is aggregation
            ## agg refresh ##

        '''
        try:
            doc_id = request.GET['document_id']
        except KeyError:
            raise DatapointsException(message='Document_id is a required API param')
        # dt = DocTransform(request.user.id, doc_id)

        ran_complex_doc_transform = False

        try:
            dt = ComplexDocTransform(request.user.id, doc_id)
            dt.main()
            ran_complex_doc_transform = True
        except Exception as err:
            try:
                dt = DateDocTransform(request.user.id, doc_id)
                ssids = dt.process_file()

            except Exception as err:
                raise DatapointsException(message=err.message)

        
        mr = MasterRefresh(request.user.id, doc_id)
        mr.main()

        if ran_complex_doc_transform:
            doc_campaign_ids = set(list(DataPoint.objects\
                .filter(source_submission__document_id = doc_id)\
                .values_list('campaign_id',flat=True)))

            for c_id in doc_campaign_ids:
                ar = AggRefresh(c_id)
                # try/except block hack because tests fail otherwise
                try:
                    with transaction.atomic():
                        ar.main()
                except TransactionManagementError as e:
                    pass
        return Document.objects.filter(id=doc_id).values()
